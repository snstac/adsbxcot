#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ADSBXCOT Class Definitions."""

import aiohttp
import asyncio
import configparser

import urllib

import pytak

import aircot

import adsbxcot


__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2022 Greg Albrecht"
__license__ = "Apache License, Version 2.0"


class ADSBXWorker(pytak.MessageWorker):

    """Reads ADSBExchange.com ADS-B Data, renders to COT, and puts on Queue."""

    def __init__(self, event_queue: asyncio.Queue, opts):
        super().__init__(event_queue)

        self.url: urllib.parse.ParseResult = urllib.parse.urlparse(
            opts.get("ADSBX_URL"))
        self.cot_stale = opts.get("COT_STALE")
        self.poll_interval: int = int(opts.get("POLL_INTERVAL") or
                                      adsbxcot.DEFAULT_POLL_INTERVAL)
        self.api_key: str = opts.get("API_KEY")

        self.include_tisb = bool(opts.get("INCLUDE_TISB")) or False
        self.include_all_craft = bool(opts.get("INCLUDE_ALL_CRAFT")) or False

        self.filters = opts.get("FILTERS")
        self.known_craft = opts.get("KNOWN_CRAFT")
        self.known_craft_key = opts.get("KNOWN_CRAFT_KEY") or "HEX"

        self.filter_type = ""
        self.known_craft_db = None

    async def handle_message(self, aircraft: list) -> None:
        """
        Transforms Aircraft ADS-B data to COT and puts it onto tx queue.
        """
        if not isinstance(aircraft, list):
            self._logger.warning(
                "Invalid aircraft data, should be a Python list.")
            return None

        if not aircraft:
            self._logger.warning("Empty aircraft list")
            return None

        _lac = len(aircraft)
        _acn = 1
        for craft in aircraft:
            icao = craft.get("hex", craft.get("icao")).strip().upper()
            flight = craft.get("flight", "").strip().upper()
            reg = craft.get("r", "").strip().upper()

            if "~" in icao and not self.include_tisb:
                continue

            known_craft = {}

            if self.filter_type:
                if self.filter_type == "HEX":
                    filter_key: str = icao
                elif self.filter_type == "FLIGHT":
                    filter_key: str = flight
                elif self.filter_type == "REG":
                    filter_key: str = reg
                else:
                    filter_key: str = ""

                if self.known_craft_db and filter_key:
                    known_craft = (list(filter(
                        lambda x: x[self.known_craft_key].strip().upper() ==
                                  filter_key, self.known_craft_db)) or
                                   [{}])[0]
                    # self._logger.debug("known_craft='%s'", known_craft)
                elif filter_key:
                    if "include" in self.filters[self.filter_type] and \
                            filter_key not in self.filters.get(self.filter_type,
                                                               "include"):
                        continue
                    if "exclude" in self.filters[self.filter_type] and \
                            filter_key in self.filters.get(self.filter_type,
                                                           "exclude"):
                        continue

            # Skip if we're using known_craft CSV and this Craft isn't found:
            if self.known_craft_db and not known_craft \
                    and not self.include_all_craft:
                continue

            event = adsbxcot.adsbx_to_cot(
                craft,
                stale=self.cot_stale,
                known_craft=known_craft
            )

            if not event:
                self._logger.debug(f"Empty CoT Event for craft={craft}")
                _acn += 1
                continue

            self._logger.debug(
                "Handling %s/%s ICAO: %s Flight: %s Category: %s",
                _acn,
                _lac,
                craft.get("hex"),
                craft.get("flight"),
                craft.get("category")
            )
            await self._put_event_queue(event)
            _acn += 1

    async def _get_adsbx_feed(self) -> None:
        """
        ADSBExchange.com ADS-B Feed API Client wrapper.
        Connects to ADSBX API and passes messages to `self.handle_message()`.
        """
        # Support for either direct ADSBX API, or RapidAPI:
        if "rapidapi" in self.url.geturl():
            headers = {
                "x-rapidapi-key": self.api_key,
                "x-rapidapi-host": "adsbexchange-com1.p.rapidapi.com"
            }
        else:
            headers = {"api-auth": self.api_key}

        async with aiohttp.ClientSession() as session:
            response = await session.request(
                method="GET",
                url=self.url.geturl(),
                headers=headers
            )
            response.raise_for_status()
            json_resp = await response.json()
            aircraft = json_resp.get("ac")

            if aircraft:
                aircraft_len = len(aircraft)
            else:
                aircraft_len = "No"
            self._logger.debug("Retrieved %s aircraft", aircraft_len)

            await self.handle_message(aircraft)

    async def run(self) -> None:
        """Runs this Thread, Reads from Pollers."""
        self._logger.info(
            "Running ADSBXWorker with URL '%s'", self.url.geturl())

        if self.known_craft is not None:
            self._logger.info("Using KNOWN_CRAFT File: '%s'", self.known_craft)
            self.known_craft_db = aircot.read_known_craft(self.known_craft)
            self.filters = configparser.ConfigParser()
            self.filters.add_section(self.known_craft_key)
            self.filters[self.known_craft_key]["include"] = \
                str([x[self.known_craft_key].strip().upper() for x
                     in self.known_craft_db])

        if self.filters or self.known_craft_db:
            filter_src = self.filters or self.known_craft_key
            self._logger.debug("filter_src=%s", filter_src)
            if filter_src:
                if "HEX" in filter_src:
                    self.filter_type = "HEX"
                elif "FLIGHT" in filter_src:
                    self.filter_type = "FLIGHT"
                elif "REG" in filter_src:
                    self.filter_type = "REG"
                self._logger.debug("filter_type=%s", self.filter_type)

        while 1:
            await self._get_adsbx_feed()
            await asyncio.sleep(self.poll_interval)
