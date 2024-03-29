#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MQTT meter for Water tank level.
Author: Johan Hardy
Email: hardy.johan@gmail.com
"""
import os
import time
import sys
import json
import argparse
import meter
import paho.mqtt.client as mqtt
import config

# Create a MQTT client
CLIENT = mqtt.Client()

def _execute_water_tank_activities():
    ''' Execute water tank activities '''
    payload = {}
    # Get water level
    payload['level'] = meter.measure()
    print("Measure: {} cm".format(payload['level']))
    # Send telemetry to MQTT broker
    CLIENT.publish(config.MQTT_TOPIC_WATER_TANK, json.dumps(payload), 1)
    CLIENT.loop_stop()
    CLIENT.disconnect()

def on_log(client, userdata, level, buf):
    print("log: ",buf)

def main():
    ''' Construct the argument parser and parse the arguments '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action='version',
                        version='%(prog)s 1.0')
    parser.add_argument("--host", required=False, help="MQTT broker host",
                        default=config.MQTT_BROCKER_HOST)
    parser.add_argument("--port", required=False, help="MQTT broker port",
                        default=config.MQTT_BROCKER_PORT)
    parser.add_argument('--keep', required=False, help="MQTT broker keepalive",
                        default=config.MQTT_KEEP_ALIVE)
    args = vars(parser.parse_args())
    # Display a friendly message to the user
    print("Starting MQTT client {}:{} keepalive {}".format(args["host"],
                                                           args["port"],
                                                           args["keep"]))
    CLIENT.connect(args["host"], int(args["port"]), int(args["keep"]))
    #CLIENT.username_pw_set("myusername", "aeNg8aibai0oiloo7xiad1iaju1uch")
    #CLIENT.on_log=on_log
    #CLIENT.loop_start()
    
    # Initialise and start meter activities
    meter.setup()
    _execute_water_tank_activities()
    meter.terminate()
    return 0

if __name__ == "__main__":
    main()
