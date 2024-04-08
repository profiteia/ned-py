from typing import List, Union, Optional, Dict, Generator
from datetime import datetime, timedelta
import logging
import requests
import pandas as pd
import json
import time
from .helper import generate_loop, is_valid_request

from .metadata import (
    NED_ACTIVITIES,
    NED_CLASSIFICATIONS,
    NED_GRANULARITIES,
    NED_GRANULARITY_TIME_ZONES,
    NED_TYPES,
    NED_POINTS,
    NED_POINTS_NETHERLANDS,
    NED_POINTS_OFFSHORE,
    NED_POINTS_PROVINCES,
)


class NedAPI:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:NedAPI:%(message)s")

    API_URL = "https://api.ned.nl/v1"
    MAX_ITEMS_PER_PAGE = 200

    def __init__(
        self,
        api_key: str,
        log_level: str = "INFO",
        force_invalid_request: bool = False,
        as_dataframe: bool = False,
        pretty_print: bool = False,
        sleep_time: float = 0.5,
    ) -> None:
        self._api_key = api_key
        self._log_level = log_level
        self._force_invalid_request = force_invalid_request
        self._as_dataframe = as_dataframe
        self._pretty_print = pretty_print
        self._sleep_time = sleep_time

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self._log_level)
        self.logger.info("Logging from NedAPI class")

    @property
    def log_level(self) -> str:
        return self._log_level

    @log_level.setter
    def log_level(self, new_log_level) -> None:
        self._log_level = new_log_level
        self.logger.setLevel(self._log_level)

    @property
    def api_key(self) -> str:
        return self._api_key

    @property
    def force_invalid_request(self) -> bool:
        return self._force_invalid_request

    @force_invalid_request.setter
    def force_invalid_request(self, new_value: bool) -> None:
        self._force_invalid_request = new_value

    @property
    def as_dataframe(self) -> bool:
        return self._as_dataframe

    @as_dataframe.setter
    def as_dataframe(self, new_value: bool) -> None:
        self._as_dataframe = new_value

    @property
    def pretty_print(self) -> bool:
        return self._pretty_print

    @pretty_print.setter
    def pretty_print(self, new_value: bool) -> None:
        self._pretty_print = new_value

    @property
    def sleep_time(self) -> float:
        return self._sleep_time

    @sleep_time.setter
    def sleep_time(self, new_value: float) -> None:
        self._sleep_time = new_value

    def _format_results(self, results: dict) -> Union[pd.DataFrame, dict]:
        """
        Function that formats the results from the API request.

        Parameters:
        results (dict): The results from the API request.

        Returns:
        Union[pd.DataFrame, dict]: A DataFrame or dict containing the parsed results.
        """

        if self._as_dataframe:
            return pd.DataFrame(results)
        else:
            return results

    def authorisations(self) -> Union[pd.DataFrame, dict]:
        return self._format_results(self._do_api_request("authorisations"))

    def users(self) -> Union[pd.DataFrame, dict]:
        return self._format_results(self._do_api_request("users"))

    def _do_api_request(
        self, endpoint: str, params: Optional[Dict[str, str]] = None
    ) -> dict:
        """
        Function that does the actual API request.

        Parameters:
        endpoint (str): The endpoint to request.
        params (Dict[str, str], optional): The parameters to pass to the request. Defaults to None.

        Returns:
        Union[pd.DataFrame, dict]: A DataFrame or dict containing the response from request.
        """

        headers = {"X-AUTH-TOKEN": self._api_key, "accept": "application/ld+json"}

        response = requests.get(
            f"{self.API_URL}/{endpoint}", headers=headers, params=params
        )

        self.logger.debug(json.dumps(params, indent=4))

        if "hydra:member" in response.json():
            response = response.json()["hydra:member"]
        else:
            response = response.json()

        # if response is not a list, check for errors
        if not isinstance(response, list) and "hydra:description" in response:
            self.logger.info(
                f"{response['hydra:title']}: {response['hydra:description']}"
            )
            return []

        # Transform the keys in the response to human-readable values
        data = self._convert_api_values(response)

        if self._pretty_print:
            print(json.dumps(data, indent=4))

        return response

    def _convert_api_values(self, response) -> List[dict]:
        """
        Function that converts the values from the API to human-readable values.

        Parameters:
        response (List[dict]): The response from the API.

        Returns:
        List[dict]: A list of dicts containing the transformed response.
        """
        data = []

        for item in response:
            for key, constant in {
                "point": NED_POINTS,
                "type": NED_TYPES,
                "granularity": NED_GRANULARITIES,
                "granularitytimezone": NED_GRANULARITY_TIME_ZONES,
                "classification": NED_CLASSIFICATIONS,
                "activity": NED_ACTIVITIES,
            }.items():
                try:
                    if key not in item:
                        continue

                    # For authorisations the value is a list of dicts
                    if isinstance(item[key], list):
                        continue
                    else:
                        item[key] = constant.inverse.get(int(item[key].split("/")[-1]))
                except:
                    raise ValueError(f"Unknown value for '{key}': '{item[key]}'.")

            data.append(item)
        return data

    def _validate_values_and_get_codes(
        self, values: List[str], constant_type: str
    ) -> List[int]:
        """
        Function that validates the values passed to the request and returns the API codes.

        Parameters:
        values (List[str]): The values to validate.
        constant_type (str): The type of constant to validate against.

        Returns:
        List[int]: A list of the API codes for the validated values.
        """

        if constant_type == "NED_TYPES":
            constant = NED_TYPES
        elif constant_type == "NED_POINTS":
            constant = NED_POINTS
        else:
            raise ValueError(f"Constant type '{constant_type}' not found.")

        validated_codes = []
        for value in values:
            value_code = constant.get(value)
            if value_code is None:
                raise ValueError(f"'{value}' not found in the '{constant_type}'.")
            validated_codes.append(value_code)
        return validated_codes

    def _timed_fetch(
        self,
        granularity: int,
        start_date: datetime,
        end_date: Optional[datetime],
        types: List[int],
        points: List[int],
        classification: int,
        activity: int,
        granularitytimezone: int,
    ) -> Generator[Dict[str, int], None, None]:
        """
        Functions that yields the response from the API request.

        Parameters:
        granularity (int): The granularity of the time.
        start_date (datetime): The start date for the request.
        end_date (datetime, optional): The end date for the request. If not provided, defaults to None.
        types (List[int]): Types to retrieve as list of integers.
        points (List[int]): Points to retrieve as list of integers.
        classification (int): The classification of the data.
        activity (int): The activity type of the data.
        granularitytimezone (int): The timezone for the granularity.

        Returns:
        A list of dicts containing the response from request.
        """

        timed_days = {
            NED_GRANULARITIES["10 minutes"]: 1,
            NED_GRANULARITIES["15 minutes"]: 1,
            NED_GRANULARITIES["Hour"]: 5,
            NED_GRANULARITIES["Day"]: 30,
            NED_GRANULARITIES["Month"]: 365,
            NED_GRANULARITIES["Year"]: 365 * 10,
        }.get(granularity, None)

        if timed_days is None:
            raise ValueError(f"Granularity {granularity} not supported.")

        if end_date is None:
            end_date = start_date + timedelta(days=timed_days)

        for current_date, end_date in generate_loop(start_date, end_date, timed_days):
            for point in points:
                # Check if is valid request
                for type in types:
                    if (
                        not is_valid_request(
                            activity, classification, granularity, point, type
                        )
                        and not self._force_invalid_request
                    ):
                        self.logger.debug(
                            f"Not forcing invalid request for {NED_POINTS.inverse[point]} - {NED_TYPES.inverse[type]}."
                        )
                        continue

                    self.logger.debug(
                        f"Valid request for {NED_POINTS.inverse[point]} - {NED_TYPES.inverse[type]}."
                    )

                    params = {
                        "itemsPerPage": self.MAX_ITEMS_PER_PAGE,
                        "point": point,
                        "type": type,
                        "classification": classification,
                        "granularity": granularity,
                        "granularitytimezone": granularitytimezone,
                        "activity": activity,
                        "validfrom[strictly_before]": end_date.strftime("%Y-%m-%d"),
                        "validfrom[after]": current_date.strftime("%Y-%m-%d"),
                    }

                    response = self._do_api_request("utilizations", params)

                    if response is not None:
                        self.logger.debug(
                            json.dumps(
                                {
                                    "granularity": NED_GRANULARITIES.inverse[
                                        granularity
                                    ],
                                    "number_of_results": len(response),
                                    "activity": NED_ACTIVITIES.inverse[activity],
                                    "classification": NED_CLASSIFICATIONS.inverse[
                                        classification
                                    ],
                                    "point": NED_POINTS.inverse[point],
                                    "type": NED_TYPES.inverse[type],
                                    "from": current_date.strftime("%Y-%m-%d"),
                                    "to": end_date.strftime("%Y-%m-%d"),
                                },
                                indent=4,
                            )
                        )

                    yield response

            # Sleep for self._sleep_time seconds to avoid rate limiting
            self.logger.debug(
                f"Sleeping for {self._sleep_time} seconds to avoid API rate limits."
            )
            time.sleep(self._sleep_time)

    def get_forecast(self):
        """
        Placeholder function for getting forecast data. Currently not implemented.

        Raises:
        NotImplementedError: Always raises this exception since the function is not yet implemented.
        """

        raise NotImplementedError("Forecast is not yet implemented.")

    def get_request(
        self,
        granularity: int,
        classification: str,
        activity: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        granularitytimezone: str = "CET (Central European Time)",
        types: Optional[List[str]] = None,
        points: Optional[List[str]] = None,
    ) -> Union[pd.DataFrame, List[dict]]:
        """
        Function that does the request and parses the response, can be called directly or by its sub functions.

        Parameters:
        granularity (str): Granularity of the time, as a string.
        classification (str): The classification of the data, as a string.
        activity (int): The activity type of the data, as a string.
        start_date (datetime): The start date for the request.
        end_date (datetime, optional): The end date for the request. If not provided, defaults to None.
        granularitytimezone (str, optional): The timezone for the granularity. Defaults to "CET (Central European Time)".
        types (List[str], optional): Types to retrieve as list of strings. If not provided, defaults to None.
        points (List[str], optional): Points to retrieve as list of strings. If not provided, defaults to None.

        Returns:
        Union[pd.DataFrame, List[dict]]: A DataFrame or list of dicts containing the response from request.
        Behaviour is based on as_dataframe attribute.
        """
        data = None

        for response in self._timed_fetch(
            NED_GRANULARITIES[granularity],
            start_date,
            end_date,
            self._validate_values_and_get_codes(types, "NED_TYPES"),
            self._validate_values_and_get_codes(points, "NED_POINTS"),
            NED_CLASSIFICATIONS[classification],
            NED_ACTIVITIES[activity],
            NED_GRANULARITY_TIME_ZONES[granularitytimezone],
        ):
            results = self._format_results(response)

            if isinstance(results, pd.DataFrame):
                data = results.copy() if data is None else pd.concat([data, results])
            elif isinstance(response, list):
                data = results.copy() if data is None else data + results

        return data

    def get_consumption(
        self,
        granularity: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        granularitytimezone: str = "CET (Central European Time)",
        types: Optional[List[str]] = [
            "IndustrialConsumersGasCombination",
            "IndustrialConsumersPowerGasCombination",
            "LocalDistributionCompaniesCombination",
            "AllConsumingGas",
        ],
        points: Optional[List[str]] = ["Nederland"],
    ) -> Union[pd.DataFrame, List[dict]]:

        return self.get_request(
            granularity,
            "Current",
            "Consuming",
            start_date,
            end_date,
            granularitytimezone,
            types,
            points,
        )

    def get_production_provinces(
        self,
        granularity: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        granularitytimezone: str = "CET (Central European Time)",
        types: Optional[List[str]] = ["Wind", "Solar"],
        points: Optional[List[str]] = NED_POINTS_PROVINCES.keys(),  # All provinces
    ) -> Union[pd.DataFrame, List[dict]]:

        return self.get_request(
            granularity,
            "Current",
            "Providing",
            start_date,
            end_date,
            granularitytimezone,
            types,
            points,
        )

    def get_production_offshore(
        self,
        granularity: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        granularitytimezone: str = "CET (Central European Time)",
        types: Optional[List[str]] = ["WindOffshore"],
        points: Optional[
            List[str]
        ] = NED_POINTS_OFFSHORE.keys(),  # All the offshore points
    ) -> Union[pd.DataFrame, List[dict]]:

        return self.get_request(
            granularity,
            "Current",
            "Providing",
            start_date,
            end_date,
            granularitytimezone,
            types,
            points,
        )

    def get_production_netherlands(
        self,
        granularity: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        granularitytimezone: str = "CET (Central European Time)",
        types: Optional[List[str]] = list(NED_TYPES.keys()),
        points: Optional[List[str]] = ["Nederland"],
    ) -> Union[pd.DataFrame, List[dict]]:

        return self.get_request(
            granularity,
            "Current",
            "Providing",
            start_date,
            end_date,
            granularitytimezone,
            types,
            points,
        )
