.. image:: https://adsbxcot.readthedocs.io/en/latest/atak_screenshot_with_pytak_logo-x25.png
   :alt: ATAK screenshot with PyTAK logo.

Display Aircraft in TAK
***********************

ADSBXCOT is a PyTAK gateway for displaying aircraft tracks from ADS-B Aggregators in `TAK Products <https://tak.gov>`_, including ATAK, WinTAK & iTAK.

ADSBXCOT converts ADS-B messages from aircraft into Cursor on Target (CoT), as spoken by TAK. ADS-B messages are read from global ADS-B data aggregators. ADS-B data sent to TAK retains much of the aircraft's track, course & speed parameters, and includes other metadata about the aircraft: Flight, Tail, Category, and et al.

ADSBXCOT runs in any Python 3.6+ environment, on both Windows & Linux.

**N.B.**: Almost all ADS-B Aggreators require pre-authorization before allowing access to ADS-B data. This pre-authorization is often in the form of an API key. Many of these services provide these API keys for free, provided you feed data from your local ADS-B receiver into their cloud-service. Otherwise, they charge a fee for access to ADS-B data. Your organization should reach out to these ADS-B data aggregator services directly to negotiate terms for your use.

`Documentation is available here. <https://adsbxcot.rtfd.io>`_

   Have your own ADS-B receiver? Check out `ADSBCOT <https://adsbcot.rtfd.io>`_.
   
   Want a turn-key ADS-B to TAK Gateway? Check out `AirTAK <https://www.snstac.com/store/p/airtak-v1>`_.

Supported ADS-B Aggregators:

- ADS-B Exchange: https://www.adsbexchange.com/
- adsb.fi: https://adsb.fi/
- ADS-B Hub: https://www.adsbhub.org/
- Airplanes.Live: https://airplanes.live/

License
=======
Copyright Sensors & Signals LLC https://www.snstac.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

