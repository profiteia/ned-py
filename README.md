# NED-py

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description

Python plugin to query the API of the Nationaal Energie Dashboard. 

## Table of Contents

- [Installation](#installation)
- [Functions](#functions)
- [Usage](#usage)
- [Disclaimer](#disclaimer)
- [License](#license)
- [Contact](#contact)

## Installation

```
git clone https://github.com/profiteia/ned-py
cd ned-py
pip install . 
```

test functionality by:

```
pip install pytest
export NED_API_KEY='YOUR_API_KEY'
pytest
```

## Functions

```
authorisations()
users()
get_consumption()
get_production_provinces()
get_production_offshore()
get_production_netherlands()
```

The API lacks clear documentation. Not all datapoints are available and forecast and backcast are not yet implemented. Checkout ned/helper.py for `is_valid_request` to see which requests are valid. 
This package will be updated when more information becomes available.

## Usage

``` 
import ned

API_KEY = 'YOUR_API_KEY'

nedapi = ned.NedAPI(API_KEY)
nedapi.as_dataframe = True
nedapi.pretty_print = False
nedapi.force_invalid_request = False
nedapi.log_level = "DEBUG"
nedapi.sleep_time = 5

df = nedapi.get_production_offshore(granularity='15 minutes', start_date=datetime.datetime(2021, 1, 1), end_date=datetime.datetime(2021, 1, 30))
```

## Disclaimer

This project is not affiliated, created or maintained by Nationaal Energie Dashboard. 

## License

This project is licensed under the [MIT License](LICENSE). 

## Contact

- Email: victor@profiteia.io
- GitHub: [Profiteia](https://github.com/profiteia)