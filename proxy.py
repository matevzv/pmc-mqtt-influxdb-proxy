#!/usr/bin/env python3

import json
import asyncio
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

def on_connect(mqttc, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    mqttc.subscribe("pmc/+")

def on_message(mqttc, userdata, msg):
    data = json.loads(msg.payload.decode('utf-8'))
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

    await influxdb.write_points(influxdb_msg)

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("localhost")

influxdb = InfluxDBClient('localhost', 8086, 'pmc', 'secret', 'pmc')

mqttc.loop_forever()
