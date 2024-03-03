#!/usr/bin/env python3
import sys
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
    values['timestamp'] = datetime.strptime(values['timestamp'], '%Y-%m-%d-%H-%M')
except:
    try:
        values['timestamp'] = datetime.strptime(values['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
    except:
        print('- Date not recognized, defaulting to now')
        values['timestamp'] = datetime.now()

fit = FitEncoder_Weight()
fit.write_file_info()
fit.write_file_creator()
fit.write_weight_scale(**values)
fit.finish()

garmin = GarminConnect()
garmin.login(garmin_username, garmin_password)
garmin.upload_file(fit)

