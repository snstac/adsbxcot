ADSBExchange.com ADS-B to Cursor-On-Target Gateway.
***************************************************

.. image:: https://raw.githubusercontent.com/ampledata/adsbxcot/main/docs/Screenshot_20201026-142037_ATAK-25p.jpg
   :alt: Screenshot of ADS-B PLI in ATAK.
   :target: https://github.com/ampledata/adsbxcot/blob/main/docs/Screenshot_20201026-142037_ATAK.jpg


The ADSBXCOT ADS-B to Cursor-On-Target Gateway transforms Automatic
Dependent Surveillance-Broadcast (ADS-B) aircraft position information into
Cursor-On-Target (COT) Position Location Information for display on
Situational Awareness applications such as the Android Team Awareness Kit
(ATAK), WinTAK, RaptorX, TAKX, iTAK, et al. ADS-B data is provided by
ADSBExchange.com and requires an `API key <https://www.adsbexchange.com/data/>`_ from that service.

For more information on the TAK suite of tools, see: https://www.tak.gov/


Support Development
===================

**Tech Support**: Email support@undef.net or Signal/WhatsApp: +1-310-621-9598

This tool has been developed for the Disaster Response, Public Safety and
Frontline Healthcare community. This software is currently provided at no-cost
to users. Any contribution you can make to further this project's development
efforts is greatly appreciated.

.. image:: https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png
    :target: https://www.buymeacoffee.com/ampledata
    :alt: Support Development: Buy me a coffee!


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

The `adsbxcot` command-line program has 2 runtime arguments::

    usage: adsbxcot [-h] [-c CONFIG_FILE] 

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG_FILE, --CONFIG_FILE CONFIG_FILE



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
Copyright 2022 Greg Albrecht <oss@undef.net>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

