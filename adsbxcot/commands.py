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
    loop = asyncio.get_running_loop()
    tx_queue: asyncio.Queue = asyncio.Queue()
    rx_queue: asyncio.Queue = asyncio.Queue()
    cot_url: urllib.parse.ParseResult = urllib.parse.urlparse(opts.cot_url)

    # Create our CoT Event Queue Worker
    reader, writer = await pytak.protocol_factory(cot_url)
    write_worker = pytak.EventTransmitter(tx_queue, writer)
    read_worker = pytak.EventReceiver(rx_queue, reader)

    adsbx_url: urllib.parse.ParseResult = urllib.parse.urlparse(opts.adsbx_url)

    message_worker = adsbxcot.ADSBXWorker(
        event_queue=tx_queue,
        url=adsbx_url,
        api_key=opts.api_key,
        poll_interval=opts.poll_interval,
        cot_stale=opts.cot_stale
    )

    await tx_queue.put(adsbxcot.hello_event())

    done, pending = await asyncio.wait(
        set([message_worker.run(), read_worker.run(), write_worker.run()]),
        return_when=asyncio.FIRST_COMPLETED)

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
        '-S', '--cot_stale', help='CoT Stale period, in seconds',
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
