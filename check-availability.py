#!/usr/bin/env python3

import json
from urllib.request import urlopen
import argparse

parser = argparse.ArgumentParser(description='Check Apple Store product availability.')
parser.add_argument('--file', '-f', dest='file', default='ipad-pro-2021.json',
                    help='product info json file')
parser.add_argument('--zip', dest='zip', default='01803',
                    help='zip code to use for search')
args = parser.parse_args()

with open(args.file) as f:
    data = json.load(f)
zip = args.zip

for part in data['parts']:
    part_no = part['part']
    part_name = f"{data['name']} {part['wireless']} {part['capacity']} - {part['color']}"
    print(f"Checking {part_no} : {part_name}...")

    with urlopen(f"https://www.apple.com/shop/fulfillment-messages?pl=true&parts.0={part_no}&location={zip}") as res:
        json_res = json.loads(res.read())

    stores = json_res['body']['content']['pickupMessage']['stores']
    avail = list(filter(lambda s : s['partsAvailability'][part_no]['pickupDisplay'] == 'available', stores))

    if len(avail) > 0:
        avail_names = list(map(lambda s : f"{s['address']['address']} in {s['city']} - {s['partsAvailability'][part_no]['pickupSearchQuote']}", avail))
        print(part_name, 'available in:')
        print(" ", "\n  ".join(avail_names))
