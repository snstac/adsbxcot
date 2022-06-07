#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ADS-B Exchange Cursor-on-Target Gateway.

"""
ADS-B Exchange Cursor-on-Target Gateway.
~~~~


:author: Greg Albrecht W2GMD <oss@undef.net>
:copyright: Copyright 2022 Greg Albrecht
:license: Apache License, Version 2.0
:source: <https://github.com/ampledata/adsbxcot>

"""

from .constants import LOG_FORMAT, LOG_LEVEL, DEFAULT_POLL_INTERVAL  # NOQA

from .functions import adsbx_to_cot, create_tasks  # NOQA

from .classes import ADSBXWorker  # NOQA

__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2022 Greg Albrecht"
__license__ = "Apache License, Version 2.0"
