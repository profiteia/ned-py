import datetime
import os
import ned
import pandas as pd


# Create a new instance of the NED class
def get_api_key():
    api_key = os.environ.get("NED_API_KEY")

    if api_key is None:
        raise ValueError("API key not found. Set the environment variable NED_API_KEY")

    return api_key


nedapi = ned.NedAPI(get_api_key())
nedapi.pretty_print = True
nedapi.authorisations()  # Get authorisations

nedapi.as_dataframe = True
nedapi.pretty_print = False
nedapi.force_invalid_request = False
nedapi.log_level = "DEBUG"
nedapi.sleep_time = 5

df = nedapi.get_production_offshore(
    granularity="15 minutes",
    start_date=datetime.datetime(2021, 1, 1),
    end_date=datetime.datetime(2021, 1, 30),
)
