#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python Team Awareness Kit (PyTAK) Module Tests."""

import asyncio
import urllib

import pytest

import adsbxcot.functions

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2021 Orion Labs, Inc.'
__license__ = 'Apache License, Version 2.0'


@pytest.fixture
def my_filter_csv():
    return "_MASTER AIRCRAFT.csv"


def test_read_filter_csv(my_filter_csv):
    a = adsbxcot.functions.read_filter_csv(my_filter_csv)
    assert isinstance(a, list) == True

def test_get_filtered_csv_regs(my_filter_csv):
    a = adsbxcot.functions.get_filtered_csv_regs(my_filter_csv)
    assert "N236NS" in a

