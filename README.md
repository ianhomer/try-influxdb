# Try influxdb

## Getting started

    brew install influxdb
    brew install influxdb-cli
    influxd

Visit <http://localhost:8086/> and set username **administrator**, password **my-secret**,
organisation **my-organisation** and initial bucket name **my-bucket**.

Click quick start to get to InfluxDB console.

## Set up command-line tool

Get the administrator token from the InfluxDB console and put into the
`INFLUX_TOKEN_ADMIN` environment variable.

    influx config create --config-name my-config \
      --host-url http://localhost:8086           \
      --org my-organisation                      \
      --token $INFLUX_TOKEN_ADMIN                \
      --active

and confirm the config is active

    influx config

See `~/.influxdbv2/configs` for this saved config

## Load data

Get bucket ID and set into `MY_BUCKET` variable and create write token

    influx bucket list --name my-bucket --json | jq -r ".[0].orgID"

Create token to write data and set into `INFLUX_TOKEN_MY_ORGANISATION` variable

    influx auth create --org my-organisation --write-bucket $MY_ORGANISATION_MY_BUCKET

Then install python dependencies

    pip3 install -r requirements.txt

And load some data into InfluxDB

    ./load-data.py
