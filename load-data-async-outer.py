#!/usr/bin/env python3

from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync

import asyncio

import helper
from timer import Timer
from config import Config

timer = Timer()
config = Config()

print("loading data into influx")


async def write(write_api, i):
    point = helper.createPoint(i)
    timer.prep()
    await write_api.write(config.bucket, config.organisation, point)
    timer.stop()


async def main():
    async with InfluxDBClientAsync(
        url=config.url, token=config.token, org=config.organisation
    ) as client:
        write_api = client.write_api()
        return await asyncio.gather(*[write(write_api, i) for i in range(config.count)])


asyncio.run(main())
