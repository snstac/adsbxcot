#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright Sensors & Signals LLC https://www.snstac.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""ADSBXCOT Functions."""

import xml.etree.ElementTree as ET

from configparser import ConfigParser
from typing import Union, Set

import pytak
import aircot
import adsbxcot  # pylint: disable=cyclic-import

__author__ = "Greg Albrecht <gba@snstac.com>"
__copyright__ = "Copyright Sensors & Signals LLC https://www.snstac.com"
__license__ = "Apache License, Version 2.0"


def create_tasks(config: ConfigParser, clitool: pytak.CLITool) -> Set[pytak.Worker,]:
    """
    Creates specific coroutine task set for this application.

    Parameters
    ----------
    config : `ConfigParser`
        Configuration options & values.
    clitool : `pytak.CLITool`
        A PyTAK Worker class instance.

    Returns
    -------
    `set`
        Set of PyTAK Worker classes for this application.
    """
    return set([adsbxcot.ADSBXWorker(clitool.tx_queue, config)])


def adsbx_to_cot_xml(  # NOQA pylint: disable=too-many-locals,too-many-branches,too-many-statements
    craft: dict, config: Union[dict, None] = None, known_craft: Union[dict, None] = None
) -> Union[ET.Element, None]:
    """
    Serializes ADS-B Aggregator aircraft objects as Cursor on Target.

    Parameters
    ----------
    craft : `dict`
        Key/Value data struct of decoded ADS-B aircraft data.
    config : `configparser.ConfigParser`
        Configuration options and values.
        Uses config options: UID_KEY, COT_STALE, COT_HOST_ID

    Returns
    -------
    `xml.etree.ElementTree.Element`
        Cursor on Target XML ElementTree object.
    """
    known_craft: dict = known_craft or {}
    config: dict = config or {}

    lat = craft.get("lat")
    lon = craft.get("lon")

    if lat is None or lon is None:
        return None

    remarks_fields = []

    uid_key = config.get("UID_KEY", "ICAO")
    cot_stale = int(config.get("COT_STALE", pytak.DEFAULT_COT_STALE))
    cot_host_id = config.get("COT_HOST_ID", pytak.DEFAULT_HOST_ID)

    aircotx = ET.Element("_aircot_")
    aircotx.set("cot_host_id", cot_host_id)

    icao_hex = craft.get("hex", craft.get("icao", ""))
    reg = craft.get("r", "")
    flight = craft.get("flight", "")
    cat = craft.get("category")
    squawk = craft.get("squawk")
    craft_type = craft.get("t", "")

    if reg:
        reg = reg.strip().upper()
        remarks_fields.append(reg)
        aircotx.set("reg", reg)

    if flight:
        flight = flight.strip().upper()
        remarks_fields.append(flight)
        aircotx.set("flight", flight)

    if squawk:
        squawk = squawk.strip().upper()
        remarks_fields.append(f"Squawk:{squawk}")
        aircotx.set("squawk", squawk)

    if icao_hex:
        icao_hex = icao_hex.strip().upper()
        remarks_fields.append(icao_hex)
        aircotx.set("icao", icao_hex)

    if cat:
        cat = cat.strip().upper()
        remarks_fields.append(f"Cat:{cat}")
        aircotx.set("cat", cat)

    if craft_type:
        craft_type = craft_type.strip().upper()
        remarks_fields.append(f"Type:{craft_type}")
        aircotx.set("type", craft_type)

    if "REG" in uid_key and reg:
        cot_uid = f"REG-{reg}"
    elif "ICAO" in uid_key and icao_hex:
        cot_uid = f"ICAO-{icao_hex}"
    if "FLIGHT" in uid_key and flight:
        cot_uid = f"FLIGHT-{flight}"
    elif icao_hex:
        cot_uid = f"ICAO-{icao_hex}"
    elif flight:
        cot_uid = f"FLIGHT-{flight}"
    else:
        return None

    if flight:
        callsign = flight
    elif reg:
        callsign = reg
    else:
        callsign = icao_hex

    _, callsign = aircot.set_name_callsign(
        icao_hex, reg, craft_type, flight, known_craft
    )
    cat = aircot.set_category(cat, known_craft)
    cot_type = aircot.set_cot_type(icao_hex, cat, flight, known_craft)

    contact = ET.Element("contact")
    contact.set("callsign", str(callsign))

    track = ET.Element("track")
    track.set("course", str(craft.get("track", "9999999.0")))

    track.set("speed", aircot.functions.get_speed(craft.get("gs")))

    detail = ET.Element("detail")
    detail.set("uid", cot_uid)
    detail.append(contact)
    detail.append(track)
    detail.append(aircotx)

    icon = known_craft.get("ICON")
    if icon:
        usericon = ET.Element("usericon")
        usericon.set("iconsetpath", icon)
        detail.append(usericon)

    remarks = ET.Element("remarks")
    remarks_fields.append(f"{cot_host_id}")
    _remarks = " ".join(list(filter(None, remarks_fields)))
    remarks.text = _remarks
    detail.append(remarks)

    cot_d = {
        "lat": str(lat),
        "lon": str(lon),
        "ce": str(craft.get("nac_p", "9999999.0")),
        "le": str(craft.get("nac_v", "9999999.0")),
        "hae": aircot.functions.get_hae(craft.get("alt_geom")),
        "uid": cot_uid,
        "cot_type": cot_type,
        "stale": cot_stale,
    }
    cot = pytak.gen_cot_xml(**cot_d)

    _detail = cot.findall("detail")[0]
    flowtags = _detail.findall("_flow-tags_")
    detail.extend(flowtags)
    cot.remove(_detail)
    cot.append(detail)

    return cot


def adsbx_to_cot(
    craft: dict, config: Union[dict, None] = None, known_craft: Union[dict, None] = None
) -> Union[bytes, None]:
    """Wrapper that returns COT as an XML string."""
    cot: Union[ET.Element, None] = adsbx_to_cot_xml(craft, config, known_craft)
    return (
        b"\n".join([pytak.DEFAULT_XML_DECLARATION, ET.tostring(cot)]) if cot else None
    )
