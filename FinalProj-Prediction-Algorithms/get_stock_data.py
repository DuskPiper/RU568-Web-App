# -*- coding:utf-8 -*-

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


class StocksData(object):
    URL = 'https://www.alphavantage.co/query'
    apikey = ''

    def __init__(self, apikey):
    	self.apikey = apikey

    def getDailyData(self, symbol: Union[str, List[str]]):
        if not symbol: raise ValueError
        if isinstance(symbol, str): symbol = [symbol, ]

        results = []
        for s in symbol:
            res = requests.get(self.URL,
                               params={
                                   'function': 'TIME_SERIES_DAILY',
                                   'symbol': s,
                                   'outputsize': 'compact',  # full, compact
                                   'apikey': self.apikey # Utils.get_env('ALPHAVANTAG_API_KEY')
                               })

            j = res.json()  # type: dict
            if 'Time Series (Daily)' in j:
                tz = j['Meta Data']['5. Time Zone']
                for d, info in j['Time Series (Daily)'].items():
                    tmpDict = {'timestamp': arrow.get(d).datetime,
                                'symbol': s,
                                'open': Decimal128(info['1. open']),
                                'high': Decimal128(info['2. high']),
                                'low': Decimal128(info['3. low']),
                                'close': Decimal128(info['4. close'])}
                    try:
                        tmpDict['volume'] = Int64(info['5. volume'])
                    except (BSONError, ValueError):
                        tmpDict['volume'] = Int64(0)
                    results.append(tmpDict)
            else:
                print(arrow.utcnow().isoformat())
                print(json.dumps(j, indent=1))
        return results

    def getRealtimePrice(self, symbol: Union[str, List[str]] = None):
        if symbol is None:
            return []
        if isinstance(symbol, str):
            symbol = [symbol, ]

        res = requests.get(self.URL,
                           params={
                               'function': 'BATCH_STOCK_QUOTES',
                               'symbols': ','.join(symbol),
                                   'apikey': self.apikey # Utils.get_env('ALPHAVANTAG_API_KEY')
                           })
        j = res.json()  #type: dict
        results = []
        if 'Stock Quotes' in j:
            tz = j['Meta Data']['3. Time Zone']

            for info in j['Stock Quotes']:
                tmpDict = {'timestamp': arrow.get(info['4. timestamp']).replace(tzinfo=tz).datetime,
                            'symbol': info['1. symbol'],
                            'price': Decimal128(info['2. price'])}
                try:
                    tmpDict['volume'] = Int64(info['3. volume'])
                except (BSONError, ValueError):
                    tmpDict['volume'] = Int64(0)
                results.append(tmpDict)
        else:
            print(arrow.utcnow().isoformat())
            print(json.dumps(j, indent=1))
        return results


def get_formated_daily_prices(symbol, apikey=Env.alpha_vantage_api_key):
    URL = 'https://www.alphavantage.co/query'
    if not symbol: raise ValueError
    if isinstance(symbol, str): symbol = [symbol, ]

    prices = []

    for s in symbol:
        res = requests.get(URL,
                           params={
                               'function': 'TIME_SERIES_DAILY',
                               'symbol': s,
                               'outputsize': 'compact',  # full, compact
                               'apikey': apikey
                           })

        j = res.json()  # type: dict
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


if __name__ == '__main__':
    cirno = StocksData(Env.alpha_vantage_api_key)
    # print(cirno.getRealtimePrice('GOOG'))
    daily = cirno.getDailyData('GOOG')
    for row in daily:
        print(row)