#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ADS-B Exchange Cursor-on-Target Gateway Functions."""

import csv
import datetime
import os
import platform
import xml.etree.ElementTree

import pytak

import adsbxcot.constants

__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2021 Orion Labs, Inc."
__license__ = "Apache License, Version 2.0"


def adsbx_to_cot(craft: dict, stale: int = None, classifier=None, known_craft: dict = {}) -> str:
    """
    Transforms an ADS-B Exchange Aircraft Object to a Cursor-on-Target PLI.
    """
    time = datetime.datetime.now(datetime.timezone.utc)
    cot_stale = stale or adsbxcot.constants.DEFAULT_STALE

    lat = craft.get("lat")
    lon = craft.get("lon")
    if lat is None or lon is None:
        return None

    icao_hex: str = craft.get("hex", craft.get("icao")).strip().upper()
    flight: str = craft.get("flight", "").strip().upper()
    craft_type: str = craft.get("t", "").strip().upper()
    reg: str = craft.get("r", "").strip().upper()

    name: str = known_craft.get("CALLSIGN")
    if name:
        callsign = name
    else:
        name = f"ICAO-{icao_hex}"
        if flight:
            callsign = "-".join([flight.strip().upper(), reg, craft_type])
        else:
            callsign = "-".join([reg, craft_type])

    category = craft.get("category")
    cot_type = known_craft.get("COT")
    if not cot_type:
        known_type = known_craft.get("TYPE", "").strip().upper()
        if known_type:
            if known_type in "FIXED WING":
                category = "1"
            elif known_type in "HELICOPTER":
                category = "7"
            elif known_type in "UAS":
                category = "14"
            else:
                category = known_type
        cot_type = classifier(icao_hex, category, flight)

    point = xml.etree.ElementTree.Element("point")
    point.set("lat", str(lat))
    point.set("lon", str(lon))
    point.set("ce", str(craft.get("nac_p", "9999999.0")))
    point.set("le", str(craft.get("nac_v", "9999999.0")))

    # alt_geom: geometric (GNSS / INS) altitude in feet referenced to the
    #           WGS84 ellipsoid
    alt_geom = int(craft.get("alt_geom", 0))
    if alt_geom:
        point.set("hae", str(alt_geom * 0.3048))
    else:
        point.set("hae", str("9999999.0"))

    uid = xml.etree.ElementTree.Element("UID")
    uid.set("Droid", name)

    contact = xml.etree.ElementTree.Element("contact")
    contact.set("callsign", str(callsign))

    track = xml.etree.ElementTree.Element("track")
    track.set("course", str(craft.get("track", "9999999.0")))

    # gs: ground speed in knots
    gs = int(craft.get("gs", 0))
    if gs:
        track.set("speed", str(gs * 0.514444))
    else:
        track.set("speed", str("9999999.0"))

    detail = xml.etree.ElementTree.Element("detail")
    detail.set("uid", name)
    detail.append(uid)
    detail.append(contact)
    detail.append(track)

    remarks = xml.etree.ElementTree.Element("remarks")

    _remarks = (
        f"{callsign} ICAO: {icao_hex} REG: {reg} Flight: {flight} Type: {craft_type} Squawk: {craft.get('Squawk')} "
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
    root.set("stale", (time + datetime.timedelta(seconds=int(cot_stale))).strftime(pytak.ISO_8601_UTC))
    root.append(point)
    root.append(detail)

    return xml.etree.ElementTree.tostring(root)


def read_known_craft(csv_file: str) -> list:
    """Reads the FILTER_CSV file into a `list`"""
    all_rows = []
    with open(csv_file) as csv_fd:
        reader = csv.DictReader(csv_fd)
        for row in reader:
            all_rows.append(row)
    return all_rows


def get_filtered_csv_regs(csv_file: str) -> list:
    filtered_csv = read_filter_csv(csv_file)
    regs = [x["REG"] for x in filtered_csv]
    return regs
