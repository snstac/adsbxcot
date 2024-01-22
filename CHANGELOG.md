## ADSBXCOT 6.0.2

- Fixes #26: Missing 'adsbxcot' command.

## ADSBXCOT 6.0.1

- Fixes #25: Missing PyTAK version requirement, should be 6.2.0.

## ADSBXCOT 6.0.0

- New for 2024!
- Removed 'light' mode for CoT.
- Documentation Updates.
- Fixes #17. Added ReadTheDocs site.
- Fixes #18: Deprecate ADSBX_URL in favor of FEED_URL akin to adsbcot.
- Fixes #19: Add support for Python 3.10, 3.11, 3.12
- Fixes #15: Add config parameter for 'only show TIS-B': TISB_ONLY
- Fixes #20: Make _aircot_ a sub-element of detail.
- Fixes #21: Use PyTAK's gen_cot_xml()
- Fixes #22: Move setup.py metadata to setup.cfg
- Fixes #23: Python 3.6 tests failing.
- Fixes #24: Pin Github actions to Ubuntu 20.04

## ADSBXCOT 5.1.0
- Added XML Declaration header to output CoT XML.
- Bumpted PyTAK dependency to >= 5.4.0
- Documentation updates.

## ADSBXCOT 5.0.4
- Added 'light' mode, to reduce size of CoT messages. [DEPRECATED 2024]

## ADSBXCOT 5.0.3
- Refactored handle_data.
- Pinned aircot dependency to >= 1.2.0

## ADSBXCOT 5.0.2
- Removed Travis CI.
- Examples updated.
- Refactored commands.py to match other PyTAK-based programs.

## ADSBXCOT 5.0.1
- Fixes for test suite.
- Examples updated.

## ADSBXCOT 5.0.0
Rewrite of ADSBXCOT to support new features of PyTAK 5.0.0