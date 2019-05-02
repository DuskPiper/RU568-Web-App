'''
@author: Ruiyu Zhang
@create: 2019.04.22
@intro.: Fetches stocks data (瞎糊的)
'''

import json
from typing import List, Union
import datetime

import arrow
import requests
from bson.decimal128 import Decimal128
from bson.errors import BSONError
from bson.int64 import Int64
from env import Env

#from utils import Utils

def get_formated_daily_prices(symbol: Union[str, List[str]], apikey=Env.alpha_vantage_api_key):
    URL = 'https://www.alphavantage.co/query'
    if not symbol:
        return []
    if isinstance(symbol, str):
        symbol = [symbol, ]

    prices = []
    for s in symbol:
        j = requests.get(URL, params={
            'function': 'TIME_SERIES_DAILY',
            'symbol': s,
            'outputsize': 'compact',  # full, compact
            'apikey': apikey
        }).json()

        if 'Time Series (Daily)' in j:
            tz = j['Meta Data']['5. Time Zone']
            for d, info in j['Time Series (Daily)'].items():
                prices.append((
                    float(arrow.get(d).datetime.timestamp()),
                    float(info['1. open']),
                    float(info['2. high']),
                    float(info['3. low']),
                    float(info['4. close'])
                ))
        else:
            print(arrow.utcnow().isoformat())
            print(json.dumps(j, indent=1))
    return prices

def get_realtime_price(symbol: Union[str, List[str]], apikey=Env.alpha_vantage_api_key):
    URL = 'https://www.alphavantage.co/query'
    if not symbol:
        return []
    if isinstance(symbol, str):
        symbol = [symbol, ]

    j = requests.get(URL, params={
        'function': 'BATCH_STOCK_QUOTES',
        'symbols': ','.join(symbol),
        'apikey': apikey
    }).json()

    results = []
    if 'Stock Quotes' in j:
        tz = j['Meta Data']['3. Time Zone']
    for info in j['Stock Quotes']:
        price = {
            'timestamp': arrow.get(info['4. timestamp']).replace(tzinfo=tz).datetime,
            'symbol': info['1. symbol'],
            'price': Decimal128(info['2. price'])
        }
        try:
            price['volume'] = Int64(info['3. volume'])
        except (BSONError, ValueError):
            price['volume'] = Int64(0)

        results.append(price)
    else:
        print(arrow.utcnow().isoformat())
        print(json.dumps(j, indent=1))

    return results



if __name__ == "__main__":
    pass