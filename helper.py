from influxdb_client import InfluxDBClient, Point, WritePrecision
import datetime

from config import Config

start = datetime.datetime.now()


def createPoint(i: int):
    time = int(
        (start - datetime.timedelta(milliseconds=i * 100)).timestamp() * 1_000_000_000
    )
    return (
        Point("measure")
        .tag("source", "load-data")
        .field("value", i + 0.123)
        .time(time, WritePrecision.NS)
    )


def showBucketInfo():
    config = Config()
    with InfluxDBClient(
        url=config.url, token=config.token, org=config.organisation
    ) as client:
        tables = client.query_api().query(
            f'from(bucket:"{config.bucket}") '
            + "|> range(start: -1d) "
            + '|> filter(fn: (r) => r["_measurement"] == "measure") '
            + "|> count()"
        )
        print(f'point count = {tables[0].records[0]["_value"]}')
