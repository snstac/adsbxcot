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

"""
Display Aircraft in TAK.

:author: Greg Albrecht <gba@snstac.com>
:copyright: Copyright Sensors & Signals LLC https://www.snstac.com
:license: Apache License, Version 2.0
:source: <https://github.com/snstac/adsbxcot>
"""

# Python 3.6 test/build work-around:
try:
    from .constants import DEFAULT_POLL_INTERVAL, DEFAULT_LIGHT_COT  # NOQA
    from .functions import adsbx_to_cot, create_tasks  # NOQA
    from .classes import ADSBXWorker  # NOQA
except ImportError:
    import warnings

    warnings.warn(
        "Unable to import required modules, ignoring (Python 3.6 build work-around)."
    )

__version__ = "6.0.1"
__author__ = "Greg Albrecht <gba@snstac.com>"
__copyright__ = "Copyright Sensors & Signals LLC https://www.snstac.com"
__license__ = "Apache License, Version 2.0"
