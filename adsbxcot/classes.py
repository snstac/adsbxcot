#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ADS-B Exchange Cursor-on-Target Class Definitions."""

import concurrent

import aiohttp
import asyncio
import configparser
import json
import logging
import os
import queue
import random
import threading
import time
import urllib

import pytak
import requests

import adsbxcot


__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2021 Orion Labs, Inc."
__license__ = "Apache License, Version 2.0"


class ADSBXWorker(pytak.MessageWorker):

    """Reads ADS-B Exchange Data, renders to CoT, and puts on queue."""

    def __init__(self, event_queue: asyncio.Queue, opts):
        super().__init__(event_queue)

        self.url: urllib.parse.ParseResult = urllib.parse.urlparse(opts.get("ADSBX_URL"))
        self.cot_stale = opts.get("COT_STALE")
        self.poll_interval: int = int(opts.get("POLL_INTERVAL") or adsbxcot.DEFAULT_POLL_INTERVAL)
        self.api_key: str = opts.get("API_KEY")
        self.filters = opts.get("FILTERS")
        self.known_craft = opts.get("KNOWN_CRAFT")
        self.known_craft_key = opts.get("KNOWN_CRAFT_KEY") or "HEX"

        self.cot_renderer = adsbxcot.adsbx_to_cot
        self.cot_classifier = pytak.adsb_to_cot_type

        self.known_craft_db = None

    async def handle_message(self, aircraft: list) -> None:
        """
        Transforms Aircraft ADS-B data to CoT and puts it onto tx queue.
        """
        if not isinstance(aircraft, list):
            self._logger.warning(
                "Invalid aircraft data, should be a Python list.")
            return False

        if not aircraft:
            self._logger.warning("Empty aircraft list")
            return False

        _lac = len(aircraft)
        _acn = 1
        for craft in aircraft:
            # self._logger.debug("craft=%s", craft)
            icao = craft.get("hex", craft.get("icao")).strip().upper()
            flight = craft.get("flight", "").strip().upper()
            reg = craft.get("r", "").strip().upper()

            if "~" in icao:
                continue

            filter_type = ''
            filter_key = ''
            filter_src = ''
            known_craft = {}

            if self.filters or self.known_craft_db:
                filter_src = self.filters or self.known_craft_key

            if filter_src:
                if "HEX" in filter_src:
                    filter_type = "HEX"
                    filter_key = icao
                elif "FLIGHT" in filter_src:
                    filter_type = "FLIGHT"
                    filter_key = flight
                elif "REG" in filter_src:
                    filter_type = "REG"
                    filter_key = reg

                if filter_type and filter_key and not self.known_craft_db:
                    if "include" in self.filters[filter_type] and filter_key not in self.filters.get(filter_type,
                                                                                                     "include"):
                        continue
                    if "exclude" in self.filters[filter_type] and filter_key in self.filters.get(filter_type,
                                                                                                 "exclude"):
                        continue
                elif self.known_craft_db:
                    for a_known_craft in self.known_craft_db:
                        if filter_key and filter_key in a_known_craft[self.known_craft_key].strip().upper():
                            known_craft = a_known_craft

            # If we're using a known_craft csv and this craft wasn't found, skip:
            if self.known_craft_db and not known_craft:
                continue

            event = adsbxcot.adsbx_to_cot(
                craft,
                stale=self.cot_stale,
                classifier=self.cot_classifier,
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

    async def _get_adsbx_feed(self):

        # Support for either direct ADSBX API, or RapidAPI
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
            self._logger.debug("Retrieved %s aircraft", len(aircraft))
            await self.handle_message(aircraft)

    async def run(self):
        """Runs this Thread, Reads from Pollers."""
        self._logger.info(
            "Running ADSBXWorker with URL '%s'", self.url.geturl())

        if self.known_craft is not None:
            self._logger.info("Using KNOWN_CRAFT File: '%s'", self.known_craft)
            self.known_craft_db = adsbxcot.read_known_craft(self.known_craft)
            self.filters = configparser.ConfigParser()
            self.filters.add_section(self.known_craft_key)
            self.filters[self.known_craft_key]["include"] = \
                str([x[self.known_craft_key].strip().upper() for x in self.known_craft_db])

        while 1:
            await self._get_adsbx_feed()
            await asyncio.sleep(self.poll_interval)

