# Collection of benchmarks for the new Influx DB

## How to use

Install deps with poetry

`poetry install`

And run scripts with

`poetry run python ./benchmarks/script.py`

Don't forget to create a `.env` file to store your credentials. Here an example:

```
BUCKET=KUEHA
INFLUXDB_V2_URL=https://influx.db.url:443
INFLUXDB_V2_ORG=organisation-id
INFLUXDB_V2_TOKEN=**************
```
