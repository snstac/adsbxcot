![ATAK Screenshot with ADSBXCOT aircraft tracks.](atak_screenshot_with_pytak_logo-x25.jpg)

# Display Aircraft in TAK

ADSBXCOT is a PyTAK gateway for displaying aircraft tracks from ADS-B Aggregators (ADSBExchange, adsb.fi, et al.) in [TAK Products](https://tak.gov>) (ATAK, WinTAK, iTAK, TAK Server, TAKX).

ADSBXCOT converts ADS-B messages from aircraft into Cursor on Target (CoT), as spoken by TAK Products like ATAK. ADS-B messages are read from global ADS-B data aggregators, such as ADSBExchange.com or adsb.fi. ADS-B data sent to TAK Products retains many of the aircraft's track, course & speed parameters, but also metadata about the aircraft, including Flight, Tail, Category, and more.

ADSBXCOT runs in any Python 3.6+ environment, on both Windows & Linux.

N.B.: Almost all ADS-B Aggreators require pre-authorization before allowing access to ADS-B data. This pre-authorization is often in the form of an API key. Many of these services provide these API keys for free, provided you feed data from your local ADS-B receiver into their cloud-service. Otherwise, they charge a fee for access to ADS-B data. Your organization should reach out to these ADS-B data aggregator services directly to negotiate terms for your use.

[Documentation is available here.](https://adsbxcot.rtfd.io)

Have your own ADS-B receiver? Check out [ADSBCOT](https://adsbcot.rtfd.io).
