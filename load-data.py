#!/usr/bin/env python3

import datetime
import os

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

print("loading data into influx")

token = os.environ.get("INFLUX_TOKEN_MY_ORGANISATION", "")
if token == "":
    raise Exception("Please set environment variable INFLUX_TOKEN_MY_ORGANISATION")

organisation = "my-organisation"
bucket = "my-bucket"


def createPoint(i: int):
    return (
        Point("measure")
        .tag("source", "load-data")
        .field("value", i)
        .time(
            datetime.datetime.utcnow() + datetime.timedelta(milliseconds=i * 100),
            WritePrecision.NS,
        )
    )


with InfluxDBClient(
    url="http://localhost:8086", token=token, org=organisation
) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS)

    for i in range(10):
        point = createPoint(i)
        write_api.write(bucket, organisation, point)
        print(f"Loaded {point}")