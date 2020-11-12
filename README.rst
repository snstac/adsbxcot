adsbxcot - ADS-B Exchange Cursor-on-Target Gateway.
***************************************************

.. image:: https://raw.githubusercontent.com/ampledata/adsbxcot/main/docs/screenshot-1604561447-25.png
   :alt: Screenshot of ADS-B PLI in ATAK.
   :target: https://github.com/ampledata/adsbxcot/blob/main/docs/screenshot-1604561447.png


The adsbxcot ADS-B Exchange Cursor on Target Gateway transforms Automatic
Dependent Surveillance-Broadcast (ADS-B) aircraft position information into
Cursor on Target (CoT) Position Location Information (PLI) for display on
Situational Awareness (SA) applications such as the Android Team Awareness Kit
(ATAK), WinTAK, RaptorX, et al.

For more information on the TAK suite of tools, see: https://www.civtak.org/

Installation
============

The ADS-B to Cursor on Target Gateway is provided by a command-line tool called
`adsbxcot`, which can be installed either from the Python Package Index, or
directly from this source tree.

Install from the Python Package Index (PyPI)::

    $ pip install adsbxcot


Install from this source tree::

    $ git clone https://github.com/ampledata/adsbxcot.git
    $ cd adsbxcot/
    $ python setup.py install


Usage
=====

The `adsbxcot` command-line program has several runtime arguments::

  usage: adsbxcot [-h] -U COT_URL [-K FTS_TOKEN] -A ADSBX_URL -X API_KEY
                  [-I POLL_INTERVAL] [-S COT_STALE]

  optional arguments:
    -h, --help            show this help message and exit
    -U COT_URL, --cot_url COT_URL
                          URL to CoT Destination.
    -K FTS_TOKEN, --fts_token FTS_TOKEN
                          FreeTAKServer REST API Token.
    -A ADSBX_URL, --adsbx_url ADSBX_URL
                          ADS-B Exchange API URL.
    -X API_KEY, --api_key API_KEY
                          ADS-B Exchange API Key
    -I POLL_INTERVAL, --poll_interval POLL_INTERVAL
                          ADS-B Exchange API Polling Interval
    -S COT_STALE, --cot_stale COT_STALE
                          CoT Stale period, in seconds

Troubleshooting
===============

To report bugs, please set the DEBUG=1 environment variable to collect logs.

Unit Test/Build Status
======================

adsbxcot's current unit test and build status is available via Travis CI:

.. image:: https://travis-ci.com/ampledata/adsbxcot.svg?branch=master
    :target: https://travis-ci.com/ampledata/adsbxcot

Source
======
The source for adsbxcot can be found on Github: https://github.com/ampledata/adsbxcot

Author
======
adsbxcot is written and maintained by Greg Albrecht W2GMD oss@undef.net

https://ampledata.org/

Copyright
=========
adsbxcot is Copyright 2020 Orion Labs, Inc. https://www.orionlabs.io

License
=======
adsbxcot is licensed under the Apache License, Version 2.0. See LICENSE for details.

Running as a Daemon
===================
First, install supervisor::

    $ sudo yum install supervisor
    $ sudo service supervisord start

Create /etc/supervisor.d/adsbxcot.ini with the following content::

    [program:adsbxcot]
    command=adsbxcot -U https://adsbexchange.com/api/aircraft/v2/lat/36.7783/lon/-119.4179/dist/400/ -X xxx -I 5 -C 127.0.0.1 -P 8087

And update supervisor::

    $ sudo supervisorctl update
