from influxdb_client import InfluxDBClient, Point, WritePrecision
import datetime


def createPoint(i: int):
    return (
        Point("measure")
        .tag("source", "load-data")
        .field("value", i)
        .time(
            datetime.datetime.utcnow() + datetime.timedelta(milliseconds=-i * 10),
            WritePrecision.MS,
        )
    )
