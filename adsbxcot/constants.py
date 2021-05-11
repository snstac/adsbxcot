#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ADS-B Exchange Cursor-on-Target Constants."""

import logging
import os

__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2021 Orion Labs, Inc."
__license__ = "Apache License, Version 2.0"


if bool(os.environ.get("DEBUG")):
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = logging.Formatter(
        ('%(asctime)s adsbxcot %(levelname)s %(name)s.%(funcName)s:%(lineno)d '
         ' - %(message)s'))
    logging.debug('adsbxcot Debugging Enabled via DEBUG Environment Variable.')
else:
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = logging.Formatter(
        ('%(asctime)s adsbxcot %(levelname)s - %(message)s'))

DEFAULT_POLL_INTERVAL: int = 30
DEFAULT_COT_STALE: int = 120
