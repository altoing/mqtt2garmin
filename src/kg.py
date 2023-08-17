#!/usr/bin/env python3
import argparse
import time
import sys
import os
import logging
import json
import ast
from fit import FitEncoder_Weight
from datetime import date, datetime
from garmin import GarminConnect

with open('config.json') as config_file:
	cfg = json.load(config_file)
	garmin_username = cfg["garmin_username"]
	garmin_password = cfg["garmin_password"]

values = ast.literal_eval(sys.argv[1])
print (values)
try:
    values['timestamp'] = datetime.strptime(timestamp, '%Y-%m-%d-%H-%M')
except:
    try:
        values['timestamp'] = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
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
