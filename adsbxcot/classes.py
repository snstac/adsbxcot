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
from typing import Union, Optional

import aiohttp

import pytak
import aircot
import adsbxcot


class ADSBXWorker(pytak.QueueWorker):
    """Reads ADS-B Aggregator Data, renders to COT, and puts on Queue."""

    def __init__(self, queue: asyncio.Queue, config: SectionProxy) -> None:
        super().__init__(queue, config)
        self.known_craft_db: Union[dict, None] = None
        self.session: Union[aiohttp.ClientSession, None] = None
        self.altitudes: dict = {}

    async def process_craft(self, craft: dict) -> Optional[str]:
        """Process individual aircraft data."""
        if not isinstance(craft, dict):
            self._logger.warning("Aircraft list item was not a Python `dict`.")
            return None

        icao: str = craft.get("hex", craft.get("icao", ""))
        if icao:
            icao = icao.strip().upper()
        else:
            self._logger.warning("No ICAO in craft data: %s", craft)
            return None

        if "~" in icao:
            if not self.config.getboolean("INCLUDE_TISB"):
                return None
        else:
            if self.config.getboolean("TISB_ONLY"):
                return None

        known_craft: dict = aircot.get_known_craft(self.known_craft_db, icao, "HEX")

        if (
            self.known_craft_db
            and not known_craft
            and not self.config.getboolean("INCLUDE_ALL_CRAFT")
        ):
            self._logger.debug("Not including unknown craft: %s", icao)
            return None

        ref_alts = self.calc_altitude(craft)
        craft.update(ref_alts)

        if not craft:
            self._logger.debug("No altitude data for craft: %s", icao)
            return None

        event: Optional[bytes] = adsbxcot.adsbx_to_cot(
            craft, config=self.config, known_craft=known_craft
        )

        if not event:
            self._logger.debug("Empty CoT for craft: %s", icao)
            return None

        await self.put_queue(event)
        return icao

    async def handle_data(self, data: list) -> None:
        """Marshal ADS-B data into CoT, and put it onto a TX queue."""
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
            icao = await self.process_craft(craft)
            self._logger.debug("Handling %s/%s ICAO: %s", i, lod, icao)

    def calc_altitude(self, craft: dict) -> dict:
        """Calculate altitude based on barometric and geometric altitude."""
        alt_baro = craft.get("alt_baro", "")
        alt_geom = craft.get("alt_geom", "")

        if not alt_baro:
            return {}

        if alt_baro == "ground":
            return {}

        alt_baro = float(alt_baro)
        if alt_geom:
            self.altitudes["alt_geom"] = float(alt_geom)
            self.altitudes["alt_baro"] = alt_baro
        elif "alt_baro" in self.altitudes and "alt_geom" in self.altitudes:
            ref_alt_baro = float(self.altitudes["alt_baro"])
            alt_baro_offset = alt_baro - ref_alt_baro
            return {
                "x_alt_baro_offset": alt_baro_offset,
                "x_alt_geom": ref_alt_baro + alt_baro_offset,
            }

        return {}

    async def get_feed(self, url: str) -> None:
        """
        ADS-B Aggregator API Client wrapper.
        Connects to API and passes messages to `self.handle_message()`.
        """
        if self.session is None or self.session.closed:
            self._logger.error("Session is closed, cannot proceed.")
            return

        api_key: str = self.config.get("API_KEY")

        # Support for either direct ADSBX API, or RapidAPI:
        if "rapidapi" in url.lower():
            headers = {
                "x-rapidapi-key": api_key,
                "x-rapidapi-host": self.config.get(
                    "RAPIDAPI_HOST", adsbxcot.DEFAULT_RAPIDAPI_HOST
                ),
            }
        else:
            headers = {"api-auth": api_key}

        async with self.session.get(url=url, headers=headers) as resp:
            if resp.status != 200:
                response_content = await resp.text()
                self._logger.warning("Received HTTP Status %s for %s", resp.status, url)
                self._logger.warning(response_content)
                return

            json_resp = await resp.json()
            if json_resp is None:
                self._logger.warning("No JSON response from %s", url)
                return

            data = json_resp.get("ac")
            if data is None:
                self._logger.warning("No 'ac' key in JSON response from %s", url)
                return

            self._logger.info("Retrieved %s aircraft messages.", str(len(data) or "No"))
            await self.handle_data(data)

    async def run(self, _=-1) -> None:
        """Runs this Thread, Reads from Pollers."""
        self._logger.info("Running %s", self.__class__)

        url: Optional[str] = self.config.get("FEED_URL")
        if not url:
            self._logger.error("FEED_URL not set in config, cannot proceed.")
            raise ValueError("FEED_URL not set in config, cannot proceed.")

        poll_interval: Union[int, str, None] = self.config.get("POLL_INTERVAL")
        if poll_interval == "" or poll_interval is None:
            self._logger.info(
                "POLL_INTERVAL not set, using default of %s seconds.",
                adsbxcot.DEFAULT_POLL_INTERVAL,
            )
            poll_interval = adsbxcot.DEFAULT_POLL_INTERVAL

        known_craft = self.config.get("KNOWN_CRAFT")
        if known_craft:
            self._logger.info("Using KNOWN_CRAFT: %s", known_craft)
            self.known_craft_db = aircot.read_known_craft(known_craft)

        async with aiohttp.ClientSession() as self.session:
            while self.session.closed is False:
                self._logger.info(
                    "%s polling every %ss: %s", self.__class__, poll_interval, url
                )
                await self.get_feed(url)
                await asyncio.sleep(int(poll_interval))
