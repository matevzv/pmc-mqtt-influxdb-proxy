#!/usr/bin/env python3

import json
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    mqtt.subscribe("pmc/+")

def on_message(mqtt, userdata, msg):
    data = json.loads(msg.payload)
    node_id = data["node_id"]
    ts = data["ts"]
    del data["node_id"]
    del data["ts"]

    for field in data:
        data[field] = float(data[field])

    influxdb_msg = [{"measurement": "pmc_data"}]
    influxdb_msg[0]["timestamp"] = ts
    influxdb_msg[0]["tags"] = {"host": node_id}
    influxdb_msg[0]["fields"] = data

    influxdb.write_points(influxdb_msg)

mqtt = mqtt.Client()
mqtt.on_connect = on_connect
mqtt.on_message = on_message

mqtt.connect("localhost")
influxdb = InfluxDBClient('metrum.ijs.si', 8086, 'pmc', 'PMC.meritve.param', 'pmc')

mqtt.loop_forever()
