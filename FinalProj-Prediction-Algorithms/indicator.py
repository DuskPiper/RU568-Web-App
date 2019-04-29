'''
@author: Ruiyu Zhang
@create: 2019.04.29
@intro.: Customized stocks indicators calculation
'''

import numpy as np
from alpha_vantage.techindicators import TechIndicators
import json
from env import Env

class Indicator:
    '''
    collection of indictors
    '''

    @staticmethod
    def EMA(val: np.ndarray) -> np.float_:
        '''
        calculates Exponential Moving Average (指数移动平均)
        https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average
        '''

        if val.size < 10: return np.float_(-1)
        ret = sum(val[:10]) / 10
        multiplier = 2 / (10 + 1)
        for v in val[10:]:
            ret = (v - ret) * multiplier + ret
        return ret

    @staticmethod
    def VR(price: np.float_, historical_price: np.ndarray, historical_volume: np.ndarray) -> np.float_:
        '''
        calculates Volatility Ratio (成交量变异率)
        https://www.investopedia.com/terms/v/volatility-ratio.asp
        https://baike.baidu.com/item/VR%E6%8C%87%E6%A0%87
        '''

        A = np.sum(historical_volume[np.where(price > historical_price)])
        D = np.sum(historical_volume[np.where(price < historical_price)])
        U = np.sum(historical_volume[np.where(price == historical_price)])
        return np.float_((A + U / 2) / (A + D + U))

    @staticmethod
    def MACD(val12: np.ndarray, val26: np.ndarray) -> np.float_:
        '''
        calculates Moving Average Convergence / Divergence (指数平滑异同移动平均线)
        https://zh.wikipedia.org/wiki/MACD
        '''

        return Indicator.EMA(val12) - Indicator.EMA(val26)

class AlphaVantageIndicators:
    '''
    enables alpha_vantage for indicator calculation
    '''

    @staticmethod
    def ROC(stock_name):
        ti = TechIndicators(key=Env.alpha_vantage_api_key, output_format='pandas')
        data, meta_data = ti.get_roc(symbol=stock_name, interval='1min', time_period=60, series_type='close')
        #data.to_csv(stock_name + ' - ROC indicator.csv', index=True, sep=',')
        return data.to_json(orient='split')

if __name__ == "__main__":
    print(AlphaVantageIndicators.ROC("GOOG"))


