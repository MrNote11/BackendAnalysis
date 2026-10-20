import pytz
import requests

import os
from dataclasses import dataclass
from typing import Literal
from urllib.parse import urlencode
from datetime import datetime
from decimal import Decimal

from dotenv import load_dotenv

load_dotenv()  # finds .env in this folder or a parent (the repo root)

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Give up instead of waiting forever if Alpha Vantage stops responding
REQUEST_TIMEOUT_SECONDS = 30

def transform_alpha_vantage_result(timestamp_str, result):
    eastern = pytz.timezone("US/Eastern")
    utc = pytz.utc
    if len(timestamp_str) == 10:
        # Daily data has only a date; stamp it at the 4pm US/Eastern market close
        local_time = datetime.strptime(timestamp_str, '%Y-%m-%d').replace(hour=16)
    else:
        local_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
    timestamp = eastern.localize(local_time).astimezone(utc)
    return {
        'open_price': Decimal(result['1. open']),
        'close_price': Decimal(result['4. close']),
        'high_price': Decimal(result['2. high']),
        'low_price': Decimal(result['3. low']),
        'number_of_trades': None,
        'volume': int(result['5. volume']),
        'volume_weighted_average': None,
        'raw_timestamp': timestamp_str,
        'time': timestamp,
    }




@dataclass
class AlphaVantageAPIClient:
    ticker: str = "AAPL"
    # TIME_SERIES_DAILY is free; TIME_SERIES_INTRADAY needs a premium key
    function: Literal["TIME_SERIES_DAILY", "TIME_SERIES_INTRADAY"] = "TIME_SERIES_DAILY"
    interval: Literal["1min", "5min", "15min", "30min", "60min"] = "1min"
    month: str = "2024-01"
    api_key: str = ""

    def get_api_key(self):
        return self.api_key or ALPHA_VANTAGE_API_KEY

    def get_headers(self):
        api_key = self.get_api_key()
        return {}

    def get_params(self):
        params = {
            "apikey": self.get_api_key(),
            "symbol": self.ticker,
            "function": self.function,
        }
        if self.function == "TIME_SERIES_INTRADAY":
            params["interval"] = self.interval
            params["month"] = self.month
        return params
    
    def generate_url(self, pass_auth=False):
        path = "/query"
        url = f"https://www.alphavantage.co{path}"
        params = self.get_params()
        encoded_params = urlencode(params)
        url = f"{url}?{encoded_params}"
        if pass_auth:
            api_key = self.get_api_key()
            url += f"&api_key={api_key}"
        return url

    def fetch_data(self):
        headers = self.get_headers()
        url = self.generate_url()
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status() # not 200/201
        return response.json()

    def get_stock_data(self):
        data = self.fetch_data()
        dataset_keys = [x for x in data.keys() if x.startswith("Time Series")]
        if not dataset_keys:
            # Alpha Vantage answers with HTTP 200 and an 'Information', 'Note' or 'Error Message' text instead of data
            message = data.get("Information") or data.get("Note") or data.get("Error Message") or data
            raise ValueError(f"Alpha Vantage returned no data: {message}")
        results = data[dataset_keys[0]]
        dataset = []
        for timestamp_str in results.keys():
            dataset.append(
                transform_alpha_vantage_result(timestamp_str, results.get(timestamp_str))
            )
        return dataset
        