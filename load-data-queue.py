#!/usr/bin/env python3

from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
import asyncio

import helper
from timer import Timer
from config import Config

timer = Timer()
config = Config()

print("loading data into influx")


async def write(i):
    point = helper.createPoint(i)
    async with InfluxDBClientAsync(
        url=config.url, token=config.token, org=config.organisation
    ) as client:
        write_api = client.write_api()
        await write_api.write(config.bucket, config.organisation, point)
        timer.stop()


async def createConsumer(queue):
    while True:
        i = await queue.get()
        await write(i)
        queue.task_done()


async def createProducer(queue):
    for i in range(config.count):
        await queue.put(i)
        timer.prep()
        if i % 500 == 0:
            await asyncio.sleep(1)


async def main():
    queue = asyncio.Queue()

    consumers = [asyncio.create_task(createConsumer(queue)) for _ in range(10)]
    producer = asyncio.create_task(createProducer(queue))
    await producer
    print("producer complete")
    await queue.join()
    print("messages consumed")
    for consumer in consumers:
        consumer.cancel()


asyncio.run(main())