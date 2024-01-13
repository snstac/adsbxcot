#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright Sensors & Signals LLC https://www.snstac.com
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

"""ADSBXCOT Class Definitions."""

import asyncio

from configparser import SectionProxy
from typing import Union

import aiohttp

import pytak
import aircot
import adsbxcot


__author__ = "Greg Albrecht <gba@snstac.com>"
__copyright__ = "Copyright Sensors & Signals LLC https://www.snstac.com"
__license__ = "Apache License, Version 2.0"


class ADSBXWorker(pytak.QueueWorker):

    """Reads ADS-B Aggregator Data, renders to COT, and puts on Queue."""

    def __init__(self, queue: asyncio.Queue, config: SectionProxy) -> None:
        super().__init__(queue, config)
        self.known_craft_db: Union[dict, None] = None
        self.session: Union[aiohttp.ClientSession, None] = None

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

        lod = len(data)
        i = 1
        for craft in data:
            i += 1
            if not isinstance(craft, dict):
                self._logger.warning("Aircraft list item was not a Python `dict`.")
                continue

            icao: str = craft.get("hex", craft.get("icao", ""))
            if icao:
                icao = icao.strip().upper()
            else:
                continue

            if "~" in icao:
                if not self.config.getboolean("INCLUDE_TISB"):
                    continue
            else:
                if self.config.getboolean("TISB_ONLY"):
                    continue

            known_craft: dict = aircot.get_known_craft(self.known_craft_db, icao, "HEX")

            # Skip if we're using known_craft CSV and this Craft isn't found:
            if (
                self.known_craft_db
                and not known_craft
                and not self.config.getboolean("INCLUDE_ALL_CRAFT")
            ):
                continue

            event: Union[str, None] = adsbxcot.adsbx_to_cot(
                craft, config=self.config, known_craft=known_craft
            )

            if not event:
                self._logger.debug("Empty COT for craft=%s", craft)
                continue

            self._logger.debug("Handling %s/%s ICAO: %s", i, lod, icao)
            await self.put_queue(event)

    async def get_adsbx_feed(self, url: str) -> None:
        """
        ADS-B Aggregator API Client wrapper.
        Connects to API and passes messages to `self.handle_message()`.
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

        async with self.session.get(url=url, headers=headers) as resp:
            if resp.status != 200:
                response_content = await resp.text()
                self._logger.error("Received HTTP Status %s for %s", resp.status, url)
                self._logger.error(response_content)
                return

            json_resp = await resp.json()
            if json_resp is None:
                return

            data = json_resp.get("ac")
            if data is None:
                return

            self._logger.info("Retrieved %s aircraft messages.", str(len(data) or "No"))
            await self.handle_data(data)

    async def run(self, number_of_iterations=-1) -> None:
        """Runs this Thread, Reads from Pollers."""
        self._logger.info("Running %s", self.__class__)

        url: str = self.config.get("FEED_URL", self.config.get("ADSBX_URL"))
        poll_interval: str = self.config.get(
            "POLL_INTERVAL", adsbxcot.DEFAULT_POLL_INTERVAL
        )

        known_craft = self.config.get("KNOWN_CRAFT")
        if known_craft:
            self._logger.info("Using KNOWN_CRAFT: %s", known_craft)
            self.known_craft_db = aircot.read_known_craft(known_craft)

        async with aiohttp.ClientSession() as self.session:
            while 1:
                self._logger.info(
                    "%s polling every %ss: %s", self.__class__, poll_interval, url
                )
                await self.get_adsbx_feed(url)
                await asyncio.sleep(int(poll_interval))
