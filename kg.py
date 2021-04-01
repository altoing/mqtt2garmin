#!/usr/bin/env python3
import argparse
import time
import sys
import os
import logging
import json
from fit import FitEncoder_Weight

from datetime import date, datetime

from garmin import GarminConnect
from withings_sync.fit import FitEncoder_Weight

with open('config.json') as config_file:
	cfg = json.load(config_file)
	garmin_username = cfg["garmin_username"]
	garmin_password = cfg["garmin_password"]

values = {
     'weight': float(sys.argv[1]),
#    'percent_fat': None,
#    'muscle_mass': None,
#    'bone_mass': None,
#    'percent_hydration': None,
#    'active_met': None,
#    'metabolic_age': None,
#    'basal_met': None,
#    'visceral_fat_mass': None,
#    'visceral_fat_rating': None,
#    'physique_rating': None,
}

if len(sys.argv) > 2:
    timestamp = sys.argv[2]
else:
    values['timestamp'] = datetime.now()
try:
        values['timestamp'] = datetime.strptime(timestamp, '%Y-%m-%d-%H-%M')
except:
        print('- Date not recognized, defaulting to now')
        values['timestamp'] = datetime.now()

fit = FitEncoder_Weight()
fit.write_file_info()
fit.write_file_creator()
fit.write_weight_scale(**values)
fit.finish()

if garmin_username:
    garmin = GarminConnect()
    session = garmin.login(garmin_username, garmin_password)
    print(session)
    print('attempting to upload fit file...')
    r = garmin.upload_file(fit.getvalue(), session)
    print(r)
    if r:
        print('Fit file uploaded to Garmin Connect')
    else:
        print('error')
else:
    print('No Garmin username - skipping sync')
