import bidict
import os
import ned
import pandas as pd
import logging
import time
import pytest


@pytest.fixture(autouse=True)
def sleep_before_test():
    # Sleep before each test
    time.sleep(5)


def get_api_key():
    api_key = os.environ.get("NED_API_KEY")

    if api_key is None:
        raise ValueError("API key not found. Set the environment variable NED_API_KEY")

    return api_key


def test_api_key():
    get_api_key()
    assert True


nedapi = ned.NedAPI(get_api_key())
nedapi.log_level = "DEBUG"
nedapi.sleep_time = 5
nedapi.pretty_print = False
nedapi.force_invalid_request = False


def test_metadata_types():
    from ned import metadata

    assert type(metadata.NED_ACTIVITIES == bidict) and len(metadata.NED_ACTIVITIES) > 0
    assert (
        type(metadata.NED_CLASSIFICATIONS == bidict)
        and len(metadata.NED_CLASSIFICATIONS) > 0
    )
    assert (
        type(metadata.NED_GRANULARITIES == bidict)
        and len(metadata.NED_GRANULARITIES) > 0
    )
    assert (
        type(metadata.NED_GRANULARITY_TIME_ZONES == bidict)
        and len(metadata.NED_GRANULARITY_TIME_ZONES) > 0
    )
    assert (
        type(metadata.NED_POINTS_NETHERLANDS == bidict)
        and len(metadata.NED_POINTS_NETHERLANDS) > 0
    )
    assert (
        type(metadata.NED_POINTS_PROVINCES == bidict)
        and len(metadata.NED_POINTS_PROVINCES) > 0
    )
    assert (
        type(metadata.NED_POINTS_OFFSHORE == bidict)
        and len(metadata.NED_POINTS_OFFSHORE) > 0
    )
    assert type(metadata.NED_POINTS == bidict) and len(metadata.NED_POINTS) > 0
    assert type(metadata.NED_TYPES == bidict) and len(metadata.NED_TYPES) > 0


def test_authorisations():
    nedapi.as_dataframe = False

    result = nedapi.authorisations()
    assert type(result) == list and len(result) > 0


def test_authorisations_df():
    nedapi.as_dataframe = True

    result = nedapi.authorisations()
    assert type(result) == pd.DataFrame and not result.empty


def test_users():
    nedapi.as_dataframe = False

    result = nedapi.users()
    assert type(result) == list and len(result) > 0


def test_users_df():
    nedapi.as_dataframe = True

    result = nedapi.users()
    assert type(result) == pd.DataFrame and not result.empty


def test_production():
    nedapi.as_dataframe = False

    result = nedapi.get_production(
        "15 minutes", pd.Timestamp(2024, 1, 1), pd.Timestamp(2024, 1, 2)
    )
    assert type(result) == list and len(result) > 0


def test_production_df():
    nedapi.as_dataframe = True

    result = nedapi.get_production(
        "15 minutes", pd.Timestamp(2024, 1, 1), pd.Timestamp(2024, 1, 2)
    )
    assert type(result) == pd.DataFrame and not result.empty


def test_production_netherlands():
    nedapi.as_dataframe = False

    result = nedapi.get_production_netherlands(
        "15 minutes", pd.Timestamp(2024, 1, 1), pd.Timestamp(2024, 1, 2)
    )
    assert type(result) == list and len(result) > 0


def test_production_netherlands_df():
    nedapi.as_dataframe = True

    result = nedapi.get_production_netherlands(
        "15 minutes", pd.Timestamp(2024, 1, 1), pd.Timestamp(2024, 1, 2)
    )
    assert type(result) == pd.DataFrame and not result.empty


def test_production_offshore():
    nedapi.as_dataframe = False

    result = nedapi.get_production_offshore(
        "15 minutes", pd.Timestamp(2024, 1, 1), pd.Timestamp(2024, 1, 2)
    )
    assert type(result) == list and len(result) > 0


def test_production_offshore_df():
    nedapi.as_dataframe = True

    result = nedapi.get_production_offshore(
        "15 minutes", pd.Timestamp(2024, 1, 1), pd.Timestamp(2024, 1, 2)
    )
    assert type(result) == pd.DataFrame and not result.empty


def test_consumption():
    nedapi.as_dataframe = False

    result = nedapi.get_consumption(
        "15 minutes", pd.Timestamp(2024, 1, 1), pd.Timestamp(2024, 1, 2)
    )
    assert type(result) == list and len(result) > 0


def test_consumption_df():
    nedapi.as_dataframe = True

    result = nedapi.get_consumption(
        "15 minutes", pd.Timestamp(2024, 1, 1), pd.Timestamp(2024, 1, 2)
    )
    assert type(result) == pd.DataFrame and not result.empty


def test_forecast():
    nedapi.as_dataframe = False

    nedapi.sleep_time = 5
    result = nedapi.get_forecast(
        "15 minutes", pd.Timestamp(2024, 1, 1), pd.Timestamp(2024, 1, 2)
    )
    assert type(result) == list and len(result) > 0


def test_forecast_df():
    nedapi.as_dataframe = True

    result = nedapi.get_forecast(
        "15 minutes", pd.Timestamp(2024, 1, 1), pd.Timestamp(2024, 1, 2)
    )
    assert type(result) == pd.DataFrame and not result.empty
