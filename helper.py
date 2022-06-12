from influxdb_client import Point, WritePrecision
import datetime

start = datetime.datetime.now()


def createPoint(i: int):
    time = int((start - datetime.timedelta(milliseconds=i * 100)).timestamp() * 1_000)
    print(time)
    return (
        Point("measure")
        .tag("source", "load-data")
        .field("value", i + 0.123)
        .time(time, WritePrecision.MS)
    )
