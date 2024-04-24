import pandas as pd
import datetime as dt

from typing import Generator, Tuple, List
from .metadata import (
    NED_TYPES,
    NED_POINTS_PROVINCES,
    NED_POINTS_OFFSHORE,
    NED_POINTS,
    NED_ACTIVITIES,
    NED_CLASSIFICATIONS,
    NED_GRANULARITIES,
)

WIND_OR_SOLAR: List = [NED_TYPES["Wind"], NED_TYPES["Solar"]]

VALID_GAS_CONSUMPTION_TYPES: List = [
    NED_TYPES["IndustrialConsumersGasCombination"],
    NED_TYPES["IndustrialConsumersPowerGasCombination"],
    NED_TYPES["LocalDistributionCompaniesCombination"],
    NED_TYPES["AllConsumingGas"],
]

VALID_FORECAST_TYPES: List = [
    NED_TYPES["Wind"],
    NED_TYPES["Solar"],
    NED_TYPES["WindOffshore"],
    NED_TYPES["WindOffshoreC"],
]

INVALID_10_MINUTES_TYPES: List = [
    NED_TYPES["FossilGasPower"],
    NED_TYPES["FossilHardCoal"],
    NED_TYPES["Nuclear"],
    NED_TYPES["WastePower"],
    NED_TYPES["WindOffshoreB"],
    NED_TYPES["BiomassPower"],
    NED_TYPES["OtherPower"],
    NED_TYPES["ElectricityMix"],
]


def generate_loop(
    start_date: dt.datetime, end_date: dt.datetime, timed_maximum_days: int
) -> Generator[Tuple[dt.datetime, dt.datetime], None, None]:
    """
    Function that generates a loop that iterates over the given start and end date with a given timed_maximum_days

    Parameters:
    start_date (dt.datetime): The start date
    end_date (dt.datetime): The end date
    timed_maximum_days (int): The maximum days to iterate over

    Yields:
    Tuple[dt.datetime, dt.datetime]: A tuple with the current date and the until date
    """
    current_date = start_date

    while current_date < end_date:
        if current_date + pd.Timedelta(f"{timed_maximum_days} days") > end_date:
            until_date = end_date
        else:
            until_date = current_date + pd.Timedelta(f"{timed_maximum_days} days")

        yield (current_date, until_date)

        current_date += pd.Timedelta(f"{timed_maximum_days} days")


def is_valid_request(
    ned_activity: int,
    ned_classification: int,
    ned_granularity: int,
    ned_point: int,
    ned_type: int,
) -> bool:

    if ned_activity == NED_ACTIVITIES["Consuming"]:
        # Forecast is not (yet?) available for Consuming
        if ned_classification == NED_CLASSIFICATIONS["Forecast"]:
            return False

        # Backcast is not (yet?) available for Consuming
        if ned_classification == NED_CLASSIFICATIONS["Backcast"]:
            return False

        # Only gas consumption for Nederland is available
        return (
            ned_point == NED_POINTS["Nederland"]
            and ned_type in VALID_GAS_CONSUMPTION_TYPES
        )

    if ned_activity == NED_ACTIVITIES["Providing"]:
        # Only consumption is available for VALID_GAS_CONSUMPTION_TYPES
        if ned_type in VALID_GAS_CONSUMPTION_TYPES:
            return False

        # Forecast is available for specific types and points
        if ned_classification == NED_CLASSIFICATIONS["Forecast"]:
            if ned_type in VALID_FORECAST_TYPES:
                if ned_granularity == NED_GRANULARITIES["Year"]:
                    # Not available for a whole year
                    return False

                if (
                    ned_type == NED_TYPES["WindOffshoreC"]
                    and ned_point == NED_POINTS["Nederland"]
                ):
                    # WindOffshoreC only available for the Netherlands
                    return True
                elif ned_type == NED_TYPES["WindOffshore"]:
                    # WindOffShore only available for NED_POINTS_OFFSHORE and the Netherlands
                    if (
                        ned_point in NED_POINTS_OFFSHORE.values()
                        or ned_point == NED_POINTS["Nederland"]
                    ):
                        return True
                elif (
                    ned_point == NED_POINTS["Nederland"]
                    or ned_point in NED_POINTS_PROVINCES.values()
                ):
                    # All VALID_FORECAST_TYPES are available for the Netherlands or the provinces
                    return True

            return False

        # Backcast is not yet available
        if ned_classification == NED_CLASSIFICATIONS["Backcast"]:
            return False

        # Not all types are available for ten minutes granularity
        if (
            ned_granularity == NED_GRANULARITIES["10 minutes"]
            and ned_type in INVALID_10_MINUTES_TYPES
        ):
            return False

        # Otherwise all data is available for the Netherlands
        if ned_point == NED_POINTS["Nederland"]:
            return True

        # Wind and solar types are only available for provinces
        if ned_type in WIND_OR_SOLAR and ned_point in NED_POINTS_PROVINCES.values():
            return True

        # The offshore wind type is only available for offshore points
        if (
            ned_type == NED_TYPES["WindOffshore"]
            and ned_point in NED_POINTS_OFFSHORE.values()
        ):
            return True

    return False
