#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ADSBXCOT Functions."""

import datetime
import platform
import xml.etree.ElementTree

import pytak
import aircot

import adsbxcot.constants

__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2022 Greg Albrecht"
__license__ = "Apache License, Version 2.0"


def adsbx_to_cot_raw(craft: dict, stale: int = None,
                     known_craft: dict = {}) -> xml.etree.ElementTree.Element:
    """
    Transforms an ADS-B Exchange Aircraft Object to a Cursor-on-Target PLI.
    """
    time = datetime.datetime.now(datetime.timezone.utc)
    cot_stale = stale or adsbxcot.constants.DEFAULT_COT_STALE

    icao_hex: str = craft.get("hex", craft.get("icao")).strip().upper()
    flight: str = craft.get("flight", "").strip().upper()
    craft_type: str = craft.get("t", "").strip().upper()
    reg: str = craft.get("r", "").strip().upper()

    name, callsign = aircot.set_name_callsign(
        icao_hex, reg, craft_type, flight, known_craft)
    category = aircot.set_category(craft.get("category"), known_craft)
    cot_type = aircot.set_cot_type(icao_hex, category, flight, known_craft)

    point = xml.etree.ElementTree.Element("point")
    point.set("lat", str(craft.get("lat")))
    point.set("lon", str(craft.get("lon")))

    point.set("ce", str(craft.get("nac_p", "9999999.0")))
    point.set("le", str(craft.get("nac_v", "9999999.0")))

    point.set("hae", aircot.functions.get_hae(craft.get("alt_geom")))

    uid = xml.etree.ElementTree.Element("UID")
    uid.set("Droid", name)

    contact = xml.etree.ElementTree.Element("contact")
    contact.set("callsign", str(callsign))

    track = xml.etree.ElementTree.Element("track")
    track.set("course", str(craft.get("track", "9999999.0")))

    track.set("speed", aircot.functions.get_speed(craft.get("gs")))

    detail = xml.etree.ElementTree.Element("detail")
    detail.set("uid", name)
    detail.append(uid)
    detail.append(contact)
    detail.append(track)

    icon = known_craft.get("ICON")
    if icon:
        usericon = xml.etree.ElementTree.Element("usericon")
        usericon.set("iconsetpath", icon)
        detail.append(usericon)

    remarks = xml.etree.ElementTree.Element("remarks")

    _remarks = (
        f"{callsign} ICAO: {icao_hex} REG: {reg} Flight: {flight} "
        f"Type: {craft_type} Squawk: {craft.get('squawk')} "
        f"Category: {craft.get('category')} (via adsbxcot@{platform.node()})")

    detail.set("remarks", _remarks)
    remarks.text = _remarks
    detail.append(remarks)

    root = xml.etree.ElementTree.Element("event")
    root.set("version", "2.0")
    root.set("type", cot_type)
    root.set("uid", f"ICAO-{icao_hex}")
    root.set("how", "m-g")
    root.set("time", time.strftime(pytak.ISO_8601_UTC))
    root.set("start", time.strftime(pytak.ISO_8601_UTC))
    root.set("stale", (time + datetime.timedelta(
        seconds=int(cot_stale))).strftime(pytak.ISO_8601_UTC))
    root.append(point)
    root.append(detail)

    return root


def adsbx_to_cot(craft: dict, stale: int = None,
                 known_craft: dict = {}) -> bytes:
    lat = craft.get("lat")
    lon = craft.get("lon")
    if lat is None or lon is None:
        return ''

    return xml.etree.ElementTree.tostring(
        adsbx_to_cot_raw(craft, stale, known_craft))
