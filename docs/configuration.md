ADSBXCOT's configuration parameters can be set two ways:

1. In an INI-style configuration file. ``adsbxcot -c config.ini``
2. As environment variables. ``export DEBUG=1;adsbcot``

ADSBXCOT has the following built-in configuration parameters:


* **`FEED_URL`**
    * Default: TK

    ADS-B Aggregator API URL.

* **`POLL_INTERVAL`**
    * Default: ``30``

    Period, in seconds, to poll API URL.

* **`KNOWN_CRAFT`**:
    * Default: unset

    CSV-style aircraft hints file for overriding callsign, icon, COT Type, etc.

* **`INCLUDE_TISB`**:
    * Default: ``False``

    If ``True``, includes TIS-B tracks.

* **`INCLUDE_ALL_CRAFT`**:
    * Default: ``False``

    If ``True`` and ``KNOWN_CRAFT`` is set, will forward all aircraft, including those transformed by the ``KNOWN_CRAFT`` database.

* **`TISB_ONLY`**:
    * Default: ``False``

    If ``True``, only passes TIS-B tracks.

Additional configuration parameters, including TAK Server configuration, are included in the [PyTAK Configuration](https://pytak.readthedocs.io/en/latest/configuration/) documentation.

