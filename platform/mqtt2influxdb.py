#!/bin/python3
import paho.mqtt.client as mqtt
import datetime
import time
from influxdb import InfluxDBClient

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc), flush=True)
    client.subscribe("home/#")

def on_message(client, userdata, msg):
    # Use utc as timestamp
    receiveTime=datetime.datetime.utcnow()
    message=msg.payload.decode("utf-8")
    isfloatValue=False
    try:
        # Convert the string to a float so that it is stored as a number and not a string in the database
        val = float(message)
        isfloatValue=True
    except:
        isfloatValue=False

    if isfloatValue:
        print(str(receiveTime) + ": " + msg.topic + " " + str(val), flush=True)

        json_body = [
            {
                "measurement": msg.topic,
                "time": receiveTime,
                "fields": {
                    "value": val
                }
            }
        ]
		
        dbclient.write_points(json_body)
        print("Finished writing to InfluxDB", flush=True)

# Set up a client for InfluxDB
dbclient = InfluxDBClient('192.168.1.25', 8086, 'root', 'root', 'test')

# Initialize the MQTT client that should connect to the Mosquitto broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
connOK=False
while(connOK == False):
    try:
        client.connect("192.168.1.14", 1883, 60)
        connOK = True
    except:
        connOK = False
    time.sleep(2)

# Blocking loop to the Mosquitto broker
client.loop_forever()
