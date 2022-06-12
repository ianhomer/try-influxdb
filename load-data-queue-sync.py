#!/usr/bin/env python3

from influxdb_client import InfluxDBClient, WriteOptions
from influxdb_client.client.write_api import WriteType

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
        write_api = client.write_api(
            write_options=WriteOptions(write_type=WriteType.synchronous)
        )

        point = helper.createPoint(i)
        timer.send()
        write_api.write(config.bucket, config.organisation, point)
        timer.stop()


async def createConsumer(queue):
    while True:
        i = await queue.get()
        await asyncio.to_thread(lambda: write(i))
        queue.task_done()


async def createProducer(queue):
    for i in range(config.count):
        await queue.put(i)
        timer.prep()
        # throttle
        if i % 10000 == 0:
            await asyncio.sleep(1)


async def main():
    queue = asyncio.Queue()

    consumers = [asyncio.create_task(createConsumer(queue)) for _ in range(1000)]
    producer = asyncio.create_task(createProducer(queue))
    await producer
    print("producer complete")
    await queue.join()
    print("messages consumed")
    for consumer in consumers:
        consumer.cancel()


asyncio.run(main())
