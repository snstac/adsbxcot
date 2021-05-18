#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for the ADS-B Exchange Cursor-on-Target Gateway.

Source:: https://github.com/ampledata/adsbxcot
"""

import os
import sys

import setuptools

__title__ = "adsbxcot"
__version__ = "1.3.1"
__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2021 Orion Labs, Inc."
__license__ = "Apache License, Version 2.0"


def publish():
    """Function for publishing package to pypi."""
    if sys.argv[-1] == 'publish':
        os.system('python setup.py sdist')
        os.system('twine upload dist/*')
        sys.exit()


publish()


setuptools.setup(
    version=__version__,
    name=__title__,
    packages=[__title__],
    package_dir={__title__: __title__},
    url=f'https://github.com/ampledata/{__title__}',
    description='ADS-B Exchange Cursor-on-Target Gateway.',
    author='Greg Albrecht',
    author_email='oss@undef.net',
    package_data={'': ['LICENSE']},
    license="Apache License, Version 2.0",
    long_description=open('README.rst').read(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'pytak >= 3.0.0',
        'requests',
        'aiohttp',
    ],
    classifiers=[
        'Topic :: Communications :: Ham Radio',
        'Programming Language :: Python',
        'License :: OSI Approved :: Apache Software License'
    ],
    keywords=[
        'ADS-B', 'ADSB', 'Cursor on Target', 'ATAK', 'TAK', 'CoT'
    ],
    entry_points={'console_scripts': ['adsbxcot = adsbxcot.commands:cli']}
)
