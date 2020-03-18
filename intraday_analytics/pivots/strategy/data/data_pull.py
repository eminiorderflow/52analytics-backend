# from 3rd path library
import requests
import pandas as pd
from decouple import config

# from project module

from django.conf import settings
import intraday_analytics.settings as project_settings
import django

# settings.configure(INSTALLED_APPS=project_settings.INSTALLED_APPS, DATABASES=project_settings.DATABASES)

django.setup()
from pivots.models import SymbolList, LookbackPeriod, IntradaySMA, MetaTable, IntradayVWAP, WeeklyVWAP, IntradayVPOC, \
IntradayIB, IntradayDelDivShort, IntradayDelDivLong, IntradayRSIDivShort, IntradayRSIDivLong, IntradayADXDivShort, \
IntradayADXDivLong, IntradayVolDiv, EodTodayOHLC, EodYestOHLC, EodWeekHL, EodMonthHL, EodYearHL, EodYtdHL, EodSMA, \
EodMonthVWAP, EODYearVWAP, EODYearVPOC, IntradayMinuteData


class DataPull:
    """Alpha Vantage API Parsing the json output"""

    API_KEY = config("API_KEY")

    def __init__(self, symbol):
        self._symbol = symbol
        self.intra_dict = {}
        self.eod_dict = {}

    def get_intraday_json(self, symbol):
        intraday_client = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}" \
                            f"&interval=1min&outputsize=full&apikey={self.API_KEY}"
        return requests.get(intraday_client).json()

    def get_eod_json(self, symbol):
        eod_client = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}" \
                        f"&outputsize=full&apikey={self.API_KEY}"
        return requests.get(eod_client).json()

    def intraday_data(self):
        return self.get_intraday_json(self._symbol)

    def eod_data(self):
            return self.get_eod_json(self._symbol)

    def intraday_dataframe(self):
        df = pd.DataFrame(self.intraday_data()['Time Series (1min)']).transpose()
        df.index = pd.to_datetime(df.index)
        return df

    def eod_dataframe(self):
        return pd.DataFrame(self.eod_data()['Time Series (Daily)']).transpose()

    def fetch_intraday_dataframe(self):
        self.intra_dict[self._symbol] = self.intraday_dataframe()
        return self.intra_dict

    def fetch_eod_dataframe(self):
        self.eod_dict[self._symbol] = self.eod_dataframe()
        return self.eod_dict









