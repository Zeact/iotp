#!/usr/bin/python3
import subprocess
import re
import datetime
from influxdb import InfluxDBClient

receiveTime=datetime.datetime.utcnow()
apc_status = {}

ups = subprocess.check_output("/sbin/apcaccess").decode("utf-8").rstrip('\n')

for line in ups.split('\n'):
	(key,spl,val) = line.partition(': ')
	key = key.rstrip().lower()
	val = val.split()[0]
	apc_status[key] = val
#	print("K: {0} V: {1}".format(key, val))

linev = float(apc_status['linev'])
loadpct = float(apc_status['loadpct'])
bcharge = float(apc_status['bcharge'])
timeleft = float(apc_status['timeleft'])
battv = float(apc_status['battv'])
tonbatt = float(apc_status['tonbatt'])
cumonbatt = float(apc_status['cumonbatt'])

json_body = [
            {
                "measurement": "UPS",
                "time": receiveTime,
                "fields": {
					"linev": linev,
					"loadpct": loadpct,
					"bcharge": bcharge,
					"timeleft": timeleft,
					"battv": battv,
					"tonbatt": tonbatt,
					"cumonbatt": cumonbatt
                }
            }
        ]
		
dbclient = InfluxDBClient('192.168.1.25', 8086, 'root', 'root', 'test')
dbclient.write_points(json_body)
