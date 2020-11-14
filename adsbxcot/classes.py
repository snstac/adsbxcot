#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ADS-B Exchange Cursor-on-Target Class Definitions."""

import concurrent

import aiohttp
import asyncio
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
__copyright__ = "Copyright 2020 Orion Labs, Inc."
__license__ = "Apache License, Version 2.0"


class ADSBXWorker(pytak.MessageWorker):

    """Reads ADS-B Exchange Data, renders to CoT, and puts on queue."""

    def __init__(self, event_queue: asyncio.Queue, url: str, api_key: str,
                 cot_stale: int = None, poll_interval: int = None):
        super().__init__(event_queue)
        self.url = url
        self.cot_stale = cot_stale
        self.poll_interval: int = int(poll_interval or
                                      adsbxcot.DEFAULT_POLL_INTERVAL)
        self.api_key: str = api_key
        self.cot_renderer = adsbxcot.adsbx_to_cot
        self.cot_classifier = pytak.faa_to_cot_type

    async def handle_message(self, aircraft: list) -> None:
        if not aircraft:
            self._logger.warning("Empty aircraft list")
            return False

        _lac = len(aircraft)
        _acn = 1
        for craft in aircraft:
            event = adsbxcot.adsbx_to_cot(
                craft,
                stale=self.cot_stale,
                classifier=self.cot_classifier
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

        while 1:
            await self._get_adsbx_feed()
            await asyncio.sleep(self.poll_interval)

