#!/usr/bin/env python3

import os
import json
import queue
import signal
import multiprocessing
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

def on_connect(mqttc, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    mqttc.subscribe("pmc/+")

def on_message(mqttc, userdata, msg):
    try:
        q.put_nowait(msg.payload)
    except queue.Full:
        os.kill(pid, signal.SIGTERM)

def fwd_data(q, pid):
    influxdb = InfluxDBClient('localhost', 8086, 'pmc', 'secret', 'pmc')

    while True:
        try:
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

            influxdb.write_points(influxdb_msg)
        except:
            print("InfluxDB client error, restarting ...")
            os.kill(pid, signal.SIGTERM)

pid = os.getpid()

q = multiprocessing.Queue(10000)
p = multiprocessing.Process(target=fwd_data, args=(q, pid,))
p.daemon == True
p.start()

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("localhost")

mqttc.loop_forever()
