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

    def __init__(self, event_queue: asyncio.Queue, url: str, api_key: str,
                 cot_stale: int = None, poll_interval: int = None, filters: dict = None, filter_csv: str = None):
        super().__init__(event_queue)
        self.url = url
        self.cot_stale = cot_stale
        self.poll_interval: int = int(poll_interval or
                                      adsbxcot.DEFAULT_POLL_INTERVAL)
        self.api_key: str = api_key
        self.cot_renderer = adsbxcot.adsbx_to_cot
        self.cot_classifier = pytak.faa_to_cot_type
        self.filters = filters
        self.filter_csv = filter_csv
        self.csv_filters = None

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
            icao = craft.get("hex", "").strip().upper()
            if "~" in icao:
                continue

            if self.filters:
                if "ICAO" in self.filters:
                    if icao not in self.filters.get("ICAO", "include").split(','):
                        continue
                    if icao in self.filters.get("ICAO", "exclude"):
                        continue
                elif "FLIGHT" in self.filters:
                    flight = craft.get("flight", "").strip().upper()
                    if flight not in self.filters.get("FLIGHT", "include"):
                        continue
                    if flight in self.filters.get("FLIGHT", "exclude"):
                        continue
                elif "REG" in self.filters:
                    reg = craft.get("r", "").strip().upper()
                    if "include" in self.filters["REG"] and reg not in self.filters.get("REG", "include"):
                        continue
                    if "exclude" in self.filters["REG"] and reg in self.filters.get("REG", "exclude"):
                        continue

            known_craft = {}
            if self.csv_filters:
                reg = craft.get("r", "").strip().upper()
                for all_craft in self.csv_filters:
                    if reg in all_craft["REG"].strip().upper():
                        known_craft = all_craft

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

        if self.filter_csv is not None:
            self._logger.info("Using Filter CSV File: '%s'", self.filter_csv)
            self.csv_filters = adsbxcot.read_filter_csv(self.filter_csv)
            self.filters = configparser.ConfigParser()
            self.filters.add_section("REG")
            self.filters["REG"]["include"] = str([x["REG"].strip().upper() for x in self.csv_filters])

        while 1:
            await self._get_adsbx_feed()
            await asyncio.sleep(self.poll_interval)

