ADSBExchange.com ADS-B to Cursor-On-Target Gateway.
***************************************************

.. image:: https://raw.githubusercontent.com/ampledata/adsbxcot/main/docs/Screenshot_20201026-142037_ATAK-25p.jpg
   :alt: Screenshot of ADS-B PLI in ATAK.
   :target: https://github.com/ampledata/adsbxcot/blob/main/docs/Screenshot_20201026-142037_ATAK.jpg


The ADSBXCOT ADS-B to Cursor-On-Target Gateway transforms Automatic
Dependent Surveillance-Broadcast (ADS-B) aircraft position information into
Cursor-On-Target (COT) Position Location Information (PLI) for display on
Situational Awareness (SA) applications such as the Android Team Awareness Kit
(ATAK), WinTAK, RaptorX, TAKX, iTAK, et al. ADS-B data is provided by
ADSBExchange.com and requires an `API key <https://www.adsbexchange.com/data/>`_ from that service.

For more information on the TAK suite of tools, see: https://www.tak.gov/

Support ADSBXCOT Development
============================

ADSBXCOT has been developed for the Disaster Response, Public Safety and
Frontline Healthcare community. This software is currently provided at no-cost
to users. Any contribution you can make to further this project's development
efforts is greatly appreciated.

.. image:: https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png
    :target: https://www.buymeacoffee.com/ampledata
    :alt: Support ADSBXCOT development: Buy me a coffee!

Installation
============

ADSBXCOT's functionality provided by a command-line program called `adsbxcot`.

Installing as a Debian / Ubuntu Package [Recommended]::

    $ sudo apt update
    $ wget https://github.com/ampledata/aircot/releases/latest/download/python3-aircot_latest_all.deb
    $ sudo apt install -f ./python3-aircot_latest_all.deb
    $ wget https://github.com/ampledata/pytak/releases/latest/download/python3-pytak_latest_all.deb
    $ sudo apt install -f ./python3-pytak_latest_all.deb
    $ wget https://github.com/ampledata/adsbxcot/releases/latest/download/python3-adsbxcot_latest_all.deb
    $ sudo apt install -f ./python3-adsbxcot_latest_all.deb


Install from the Python Package Index (PyPI) [Advanced Users]::

    $ pip install adsbxcot


Install from this source tree [Developers]::

    $ git clone https://github.com/ampledata/adsbxcot.git
    $ cd adsbxcot/
    $ python setup.py install


Usage
=====

The `adsbxcot` command-line program has several runtime arguments::

    usage: adsbxcot [-h] [-c CONFIG_FILE] [-d] [-U COT_URL] [-S COT_STALE] [-A ADSBX_URL] [-X API_KEY] [-I POLL_INTERVAL] [-F FILTER_FILE]

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG_FILE, --CONFIG_FILE CONFIG_FILE
      -d, --DEBUG           Enable DEBUG logging
      -U COT_URL, --COT_URL COT_URL
                            URL to CoT Destination. Must be a URL, e.g. tcp:1.2.3.4:1234 or tls:...:1234, etc.
      -S COT_STALE, --COT_STALE COT_STALE
                            CoT Stale period, in seconds
      -A ADSBX_URL, --ADSBX_URL ADSBX_URL
                            ADS-B Exchange API URL.
      -X API_KEY, --API_KEY API_KEY
                            ADS-B Exchange API Key
      -I POLL_INTERVAL, --POLL_INTERVAL POLL_INTERVAL
                            For JSON API: Polling Interval
      -F FILTER_FILE, --FILTER_FILE FILTER_FILE
                            FILTER_FILE

Troubleshooting
===============

To report bugs, please set the DEBUG=1 environment variable to collect logs.

Source
======
ADSBXCOT source can be found on Github: https://github.com/ampledata/adsbxcot

Author
======
ADSBXCOT is written and maintained by Greg Albrecht W2GMD oss@undef.net

https://ampledata.org/

Copyright
=========
ADSBXCOT is Copyright 2022 Greg Albrecht

License
=======
ADSBXCOT is licensed under the Apache License, Version 2.0. See LICENSE for
details.

Filtering
=========

Filters and transforms can be specified in two ways:

1. Known Craft CSV file [Preferred].
2. Configuration file [Basic].

Using the filter configuration file:

Either:

A) On the command line specify the filter configuration with the '-F filter.ini' flag, where 'filter.ini' is the name
of your filter configuration file.

B) In the config.ini file, specify the filter configuration with FILTER_CONFIG=filter.ini, again, where filter.ini is
the name of your filter configuration file.

In either case, the filter configuration file is laid out as follows::

    [FLIGHT]
    include = xxx
    exclude = yyy

    [ICAO]
    include = xxx
    exclude = yyy

    [REG]
    include = xxx
    exclude = yyy

Please note that each section is mutually exclusive. You can only use one filter method at a time and you should only
specify one filter type at a time.

For example, to filter only ICAOs 1234 and 4567, create a filter.ini as follows::

    [ICAO]
    include = 1234, 4567

Then start adsbxcot with '-F filter.ini' or add FILTER_CONFIG=filter.ini to the config.ini file.

Another example, to exclude all United Flight 1010 from your feed::

    [FLIGHT]
    exclude = UAL1010

