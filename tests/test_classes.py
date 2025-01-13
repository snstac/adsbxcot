#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ADSBXCOT Class Tests."""

import pytest
from adsbxcot.classes import ADSBXWorker
from configparser import ConfigParser, SectionProxy
import asyncio
import logging

from unittest.mock import patch, MagicMock


@pytest.fixture
def config():
    config_parser = ConfigParser()
    config_parser.read_dict(
        {
            "DEFAULT": {
                "INCLUDE_TISB": "false",
                "TISB_ONLY": "false",
                "INCLUDE_ALL_CRAFT": "true",
            }
        }
    )
    return config_parser["DEFAULT"]


@pytest.fixture
def worker(config):
    queue = asyncio.Queue()
    return ADSBXWorker(queue, config)


def test_calc_altitude(worker):
    craft_with_both_altitudes = {"alt_baro": 37000, "alt_geom": 37500}
    # Test with both altitudes
    result = worker.calc_altitude(craft_with_both_altitudes)
    assert result == {}


def test_calc_altitude_no_alt_geom(worker):
    craft_with_only_baro = {"alt_baro": 37000}
    craft_with_ground_altitude = {"alt_baro": "ground"}
    craft_with_no_altitude = {}

    # Test with only barometric altitude
    result = worker.calc_altitude(craft_with_only_baro)
    assert result == {}

    # Test with ground altitude
    result = worker.calc_altitude(craft_with_ground_altitude)
    assert result == {}

    # Test with no altitude
    result = worker.calc_altitude(craft_with_no_altitude)
    assert result == {}


def test_calc_altitude_with_cache(worker):
    craft_with_both_altitudes = {"alt_baro": 37000, "alt_geom": 37500}
    craft_with_only_baro = {"alt_baro": 37000}

    # Test with both altitudes
    result = worker.calc_altitude(craft_with_both_altitudes)
    assert result == {}

    # Test with only barometric altitude
    result = worker.calc_altitude(craft_with_only_baro)
    assert result == {"x_alt_baro_offset": 0.0, "x_alt_geom": 37000.0}


def _test_handle_data_empty_list(worker, capsys):
    data = []
    asyncio.run(worker.handle_data(data))
    captured = capsys.readouterr()
    assert "Empty aircraft list" in captured.err


def _test_handle_data_invalid_data(worker, capsys):
    data = "invalid_data"
    asyncio.run(worker.handle_data(data))
    captured = capsys.readouterr()
    print(captured)
    assert "Invalid aircraft data, should be a Python list." in captured.err


def test_handle_data_valid_data(worker):
    data = [{"hex": "ABC123"}, {"hex": "DEF456"}]
    with patch.object(
        worker, "process_craft", return_value="ABC123"
    ) as mock_process_craft:
        asyncio.run(worker.handle_data(data))
        assert mock_process_craft.call_count == 2
