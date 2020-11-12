#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ADS-B Cursor-on-Target Gateway Commands."""

import aiohttp
import argparse
import asyncio
import concurrent
import os
import sys
import urllib

import pytak

import adsbxcot


# Python 3.6 support:
if sys.version_info[:2] >= (3, 7):
    from asyncio import get_running_loop
else:
    from asyncio import _get_running_loop as get_running_loop

__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2020 Orion Labs, Inc."
__license__ = "Apache License, Version 2.0"


async def main(opts):
    loop = get_running_loop()

    tasks: set = set()
    event_queue: asyncio.Queue = asyncio.Queue(loop=loop)

    cot_url: urllib.parse.ParseResult = urllib.parse.urlparse(opts.cot_url)
    adsbx_url: urllib.parse.ParseResult = urllib.parse.urlparse(opts.adsbx_url)

    eventworker = await pytak.eventworker_factory(
        cot_url, event_queue, opts.fts_token)

    adsbxworker = adsbxcot.ADSBXWorker(
        event_queue=event_queue,
        url=adsbx_url,
        api_key=opts.api_key,
        poll_interval=opts.poll_interval,
        cot_stale=opts.cot_stale
    )

    tasks.add(asyncio.ensure_future(adsbxworker.run()))
    tasks.add(asyncio.ensure_future(eventworker.run()))

    done, pending = await asyncio.wait(
        tasks, return_when=asyncio.FIRST_COMPLETED)

    for task in done:
        print(f"Task completed: {task}")


def cli():
    """Command Line interface for ADS-B Cursor-on-Target Gateway."""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-U', '--cot_url', help='URL to CoT Destination.',
        required=True
    )
    parser.add_argument(
        '-K', '--fts_token', help='FreeTAKServer REST API Token.'
    )

    parser.add_argument(
        '-A', '--adsbx_url', help='ADS-B Exchange API URL.',
        required=True
    )
    parser.add_argument(
        '-X', '--api_key', help='ADS-B Exchange API Key',
        required=True
    )
    parser.add_argument(
        '-I', '--poll_interval', help='ADS-B Exchange API Polling Interval',
    )
    parser.add_argument(
        '-S', '--cot_stale', help='CoT Stale period, in seconds',
    )
    opts = parser.parse_args()

    if sys.version_info[:2] >= (3, 7):
        asyncio.run(main(opts), debug=bool(os.environ.get('DEBUG')))
    else:
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(main(opts))
        finally:
            loop.close()


if __name__ == '__main__':
    cli()
