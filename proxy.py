#!/usr/bin/env python3

import json
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from multiprocessing import Process, Queue

def on_connect(mqttc, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    mqttc.subscribe("pmc/+")

def on_message(mqttc, userdata, msg):
    q.put_nowait(msg.payload)

def fwd_data(q):
    influxdb = InfluxDBClient('localhost', 8086, 'pmc', 'secret', 'pmc')

    while True:
        msg = q.get()
        data = json.loads(msg.decode('utf-8'))
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

        try:
            influxdb.write_points(influxdb_msg)
        except:
            influxdb = InfluxDBClient('localhost', 8086, 'pmc', 'secret', 'pmc')
            pass

q = Queue()
Process(target=fwd_data, args=(q,)).start()

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("localhost")

mqttc.loop_forever()
