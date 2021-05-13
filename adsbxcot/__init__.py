#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ADS-B Exchange Cursor-on-Target Gateway.

"""
ADS-B Exchange Cursor-on-Target Gateway.
~~~~


:author: Greg Albrecht W2GMD <oss@undef.net>
:copyright: Copyright 2020 Orion Labs, Inc.
:license: Apache License, Version 2.0
:source: <https://github.com/ampledata/adsbxcot>

"""

from .constants import (LOG_FORMAT, LOG_LEVEL,  # NOQA
                        DEFAULT_POLL_INTERVAL, DEFAULT_COT_STALE)

from .functions import adsbx_to_cot, read_known_craft  # NOQA

from .classes import ADSBXWorker  # NOQA

__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2020 Orion Labs, Inc."
__license__ = "Apache License, Version 2.0"
