#!/usr/bin/env python3

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import asyncio

import helper
from timer import Timer
from config import Config

timer = Timer()
config = Config()

print("loading data into influx")


def write(i):
    with InfluxDBClient(
        url=config.url, token=config.token, org=config.organisation
    ) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        point = helper.createPoint(i)
        write_api.write(config.bucket, config.organisation, point)
        timer.stop()


async def process(i):
    timer.prep()
    await asyncio.to_thread(lambda: write(i))


async def main():
    await asyncio.gather(*[process(i) for i in range(config.count)])


asyncio.run(main())
