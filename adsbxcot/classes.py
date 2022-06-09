#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Greg Albrecht <oss@undef.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author:: Greg Albrecht W2GMD <oss@undef.net>
#

"""ADSBXCOT Class Definitions."""

import asyncio

from configparser import ConfigParser

import aiohttp

import pytak
import aircot
import adsbxcot


__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2022 Greg Albrecht"
__license__ = "Apache License, Version 2.0"


class ADSBXWorker(pytak.QueueWorker):

    """Reads ADSBExchange.com ADS-B Data, renders to COT, and puts on Queue."""

    def __init__(self, queue: asyncio.Queue, config: ConfigParser):
        super().__init__(queue, config)
        _ = [x.setFormatter(adsbxcot.LOG_FORMAT) for x in self._logger.handlers]

        self.known_craft = config.get("KNOWN_CRAFT")
        self.known_craft_db = None

    async def handle_data(self, data: list) -> None:
        """
        Transforms Aircraft ADS-B data to COT and puts it onto tx queue.
        """
        if not isinstance(data, list):
            self._logger.warning("Invalid aircraft data, should be a Python list.")
            return None

        if not data:
            self._logger.warning("Empty aircraft list")
            return None

        icao = None
        _lac = len(data)
        _acn = 1
        for craft in data:
            icao = craft.get("hex", craft.get("icao")).strip().upper()

            if "~" in icao and not self.config.getboolean("INCLUDE_TISB"):
                continue

            known_craft = {}

            if self.known_craft_db:
                known_craft = (
                    list(
                        filter(
                            lambda x: x["HEX"].strip().upper() == icao,
                            self.known_craft_db,
                        )
                    )
                    or [{}]
                )[0]
                # self._logger.debug("known_craft='%s'", known_craft)

            # Skip if we're using known_craft CSV and this Craft isn't found:
            if (
                self.known_craft_db
                and not known_craft
                and not self.config.getboolean("INCLUDE_ALL_CRAFT")
            ):
                continue

            event = adsbxcot.adsbx_to_cot(
                craft, config=self.config, known_craft=known_craft
            )

            if not event:
                self._logger.debug("Empty COT for craft=%s", craft)
                _acn += 1
                continue

            self._logger.debug(
                "Handling %s/%s %s %s",
                _acn,
                _lac,
                craft.get("hex"),
                craft.get("flight"),
            )
            await self.put_queue(event)
            _acn += 1

    async def get_adsbx_feed(self, url: str) -> None:
        """
        ADSBExchange.com ADS-B Feed API Client wrapper.
        Connects to ADSBX API and passes messages to `self.handle_message()`.
        """
        api_key: str = self.config.get("API_KEY")

        # Support for either direct ADSBX API, or RapidAPI:
        if "rapidapi" in url:
            headers = {
                "x-rapidapi-key": api_key,
                "x-rapidapi-host": "adsbexchange-com1.p.rapidapi.com",
            }
        else:
            headers = {"api-auth": api_key}

        async with aiohttp.ClientSession() as session:
            response = await session.request(method="GET", url=url, headers=headers)
            response.raise_for_status()
            json_resp = await response.json()
            data = json_resp.get("ac")

            if data:
                aircraft_len = len(data)
            else:
                aircraft_len = "No"
            self._logger.debug("Retrieved %s aircraft", aircraft_len)

            await self.handle_data(data)

    async def run(self, number_of_iterations=-1) -> None:
        """Runs this Thread, Reads from Pollers."""
        self._logger.info("Running %s", self.__class__)

        url: str = self.config.get("ADSBX_URL")
        poll_interval: str = self.config.get(
            "POLL_INTERVAL", adsbxcot.DEFAULT_POLL_INTERVAL
        )

        known_craft = self.config.get("KNOWN_CRAFT")
        if known_craft:
            self._logger.info("Using KNOWN_CRAFT: %s", known_craft)
            self.known_craft_db = aircot.read_known_craft(known_craft)

        while 1:
            self._logger.info("Polling every %ss: %s", poll_interval, url)
            await self.get_adsbx_feed(url)
            await asyncio.sleep(int(poll_interval))
