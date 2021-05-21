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

Support ADSBXCoT Development
============================

ADSBXCoT has been developed for the Disaster Response, Public Safety and Frontline community at-large. This software
is currently provided at no-cost to our end-users. All development is self-funded and all time-spent is entirely
voluntary. Any contribution you can make to further these software development efforts, and the mission of ADSBXCoT
to provide ongoing SA capabilities to our end-users, is greatly appreciated:

.. image:: https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png
    :target: https://www.buymeacoffee.com/ampledata
    :alt: Support ADSBXCoT development: Buy me a coffee!

Installation
============

The ADS-B Exchange to Cursor on Target Gateway is provided by a command-line tool called
`adsbxcot`:

Installing as a Debian/Ubuntu Package::

    $ wget https://github.com/ampledata/aircot/releases/latest/download/python3-aircot_latest_all.deb
    $ sudo apt install -f ./python3-aircot_latest_all.deb
    $ wget https://github.com/ampledata/pytak/releases/latest/download/python3-pytak_latest_all.deb
    $ sudo apt install -f ./python3-pytak_latest_all.deb
    $ wget https://github.com/ampledata/adsbxcot/releases/latest/download/python3-adsbxcot_latest_all.deb
    $ sudo apt install -f ./python3-adsbxcot_latest_all.deb


Install from the Python Package Index (PyPI)::

    $ pip install adsbxcot


Install from this source tree::

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


Filtering
=========

New in the latest version of adsbxcot is the concept of filtering. Filters can be specified in a configuration file
or with a csv 'known craft' file.

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

