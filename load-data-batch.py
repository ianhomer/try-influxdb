#!/usr/bin/env python3


from influxdb_client import InfluxDBClient, WriteOptions
from influxdb_client.client.write_api import WriteType

import helper
import time
from timer import Timer
from config import Config

timer = Timer()
config = Config()

print("loading data into influx")
with InfluxDBClient(
    url=config.url, token=config.token, org=config.organisation
) as client:
    write_api = client.write_api(
        write_options=WriteOptions(
            batch_size=10000, flush_interval=10
        )
    )

    for i in range(config.count):
        point = helper.createPoint(i)
        timer.prep()
        write_api.write(config.bucket, config.organisation, point)
        timer.stop()

    time.sleep(5)
    write_api.close()
    timer.finish()
