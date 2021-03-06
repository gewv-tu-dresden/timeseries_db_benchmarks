from gewv_timeseries_client import TimeseriesClient
from dotenv import load_dotenv
from loguru import logger
import os
import certifi
import time

load_dotenv()

print(certifi.where())

influx_client = TimeseriesClient.from_env_properties()

BUCKET = os.getenv("BUCKET")
TIME_START = "-1y"
TIME_END = ""
DATALOGGER = "PI-OA-F023"
DEVICE = "LA_S_A031"
READING = "temperature"


def main():
    logger.info("Start benchmark")

    logger.info("Query data from db!")

    start = time.time()

    res = influx_client._query_api.query(
        f""" 
        import "profiler"

        option profiler.enabledProfilers = ["query", "operator"]

        from(bucket: "{BUCKET}")
            |> range(start: {TIME_START})
            |> filter(fn: (r) => r["datalogger"] == "{DATALOGGER}")
            |> filter(fn: (r) => r["device"] == "{DEVICE}")
            |> filter(fn: (r) => r["_field"] == "{READING}")
            |> keep(columns: ["_field", "_time", "_value"])
            |> set(key: "_field", value: "{READING}")
    """
    )
    end = time.time()

    logger.info("Finish the query!")
    logger.info(f"Number of tables: {len(res)}")
    logger.info(f"Number of rows: {len(res[0].records)}")
    logger.info(f"Time for request {end-start}s")
    logger.info(
        f"Total Execution time: {res[len(res)-2].records[0].values['TotalDuration']/10e9}s"
    )

    logger.info("Operations:")

    for row in res[len(res) - 1].records:
        logger.info(
            f"Operation: {row.values['Label']} Execution\
            Time: {row.values['MeanDuration']/10e9}s"
        )


if __name__ == "__main__":
    main()
