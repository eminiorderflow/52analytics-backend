from pivots.strategy.data.data_pull import DataPull, SymbolList
from pivots.strategy.indicators.indicator_calculations import Calculations
import datetime
import pandas as pd
from django.conf import settings


class EODData(DataPull):
    """Class used to convert the raw data to format acceptable by indicator class"""

    def __init__(self, _symbol):
        super().__init__(_symbol)

    def full_data(self):
        df = self.fetch_eod_dataframe()[self._symbol]
        df = df.rename(columns={df.columns[0]: 'open', df.columns[1]: 'high', df.columns[2]: 'low',
                                df.columns[3]: 'close', df.columns[4]: 'volume'})
        return df


class EODIndicators(Calculations):
    """Complete methods for indicators calculations"""

    def __init__(self, eod_data):
        super().__init__()
        self.eod_data = eod_data

    def todays_data(self):
        todays_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        return self.eod_data[self.eod_data.index == todays_date]

    def yesterday_data(self):
        yesterday_date = datetime.datetime.strftime(datetime.datetime.now() - pd.tseries.offsets.BDay(1), '%Y-%m-%d')
        return self.eod_data[self.eod_data.index == yesterday_date]

    def week_data(self):
        week_date = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=7), '%Y-%m-%d')
        return self.eod_data[self.eod_data.index >= week_date]

    def month_data(self):
        month_date = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=30), '%Y-%m-%d')
        return self.eod_data[self.eod_data.index >= month_date]

    def year_data(self):
        year_date = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=365), '%Y-%m-%d')
        return self.eod_data[self.eod_data.index >= year_date]

    def ytd_data(self):
        ytd_date = datetime.datetime.strftime(datetime.datetime(datetime.datetime.now().year, 1, 1), '%Y-%m-%d')
        return self.eod_data[self.eod_data.index >= ytd_date]

    def todays_ohlc(self):
        return self.todays_data()

    def yesterday_ohlc(self):
        return self.yesterday_data()

    def week_high_low(self):
        return self.ohlc(self.week_data())

    def month_high_low(self):
        return self.ohlc(self.month_data())

    def year_high_low(self):
        return self.ohlc(self.year_data())

    def ytd_high_low(self):
        return self.ohlc(self.year_data())

    def eod_sma(self):
        return self.sma(df=self.year_data()[['close']].iloc[::-1].astype(float))

    def month_vwap(self):
        return self.vwap(df=self.month_data()[['close', 'volume']].iloc[::-1].astype(float))

    def year_vwap(self):
        return self.vwap(df=self.year_data()[['close', 'volume']].iloc[::-1].astype(float))

    def year_vpoc(self):
        return self.vpoc(df=self.year_data()[['close', 'volume']].iloc[::-1].astype(float))




