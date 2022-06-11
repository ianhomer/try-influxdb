#!/usr/bin/env python3


from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS


import helper
from timer import Timer
from config import Config

timer = Timer()
config = Config()

print("loading data into influx")
with InfluxDBClient(
    url=config.url, token=config.token, org=config.organisation
) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS)

    for i in range(config.count):
        point = helper.createPoint(i)
        timer.start()
        write_api.write(config.bucket, config.organisation, point)
        timer.stop()
