#!/usr/bin/python3
import paho.mqtt.publish as publish
from subprocess import check_output
from re import findall

def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    return(findall("\d+\.\d+",temp)[0])

def publish_message(topic, message):
        print("Publishing to MQTT topic: " + topic)
        print("Message: " + message)
        publish.single(topic, message, hostname="192.168.1.14")

temp = get_temp()
publish_message("home/RPI2/Temp", temp)
