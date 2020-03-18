from pivots.strategy.data.data_pull import DataPull, SymbolList, LookbackPeriod, IntradayVWAP
from pivots.strategy.indicators.indicator_calculations import Calculations
import pandas as pd
import datetime
from django.conf import settings


class IntradayData(DataPull):
    """Class used to convert the raw data to format acceptable by indicator class"""

    def __init__(self, _symbol):
        super().__init__(_symbol)

    def full_data(self):
        df = self.fetch_intraday_dataframe()[self._symbol]
        df = df.rename(columns={df.columns[0]: 'open', df.columns[1]: 'high', df.columns[2]: 'low',
                                df.columns[3]: 'close', df.columns[4]: 'volume'})
        df.index = df.index.tz_localize(settings.TIME_ZONE)  # making the df timezone aware
        return df


class IntradayIndicators(Calculations):
    """Complete methods for intraday indicators"""

    def __init__(self, ieod_data):
        super().__init__()
        self.ieod_data = ieod_data

    def todays_data(self):
        intraday_time = datetime.datetime.today().strftime('%Y-%m-%d') + ' 09:31:00'
        return self.ieod_data[self.ieod_data.index >= intraday_time]

    def weeks_data(self):
        today = datetime.datetime.today()
        week_time = (today - datetime.timedelta(days=today.weekday())).strftime('%Y-%m-%d') + ' 09:31:00'
        return self.ieod_data[self.ieod_data.index >= week_time]

    def intraday_initial_balance(self):
        try:
            return self.initial_balance(df=self.todays_data()[['high', 'low']].iloc[::-1].astype(float))
        except ValueError:
            return pd.DataFrame(columns=['ib_high', 'ib_low'])

    def intraday_vwap(self):
        try:
            return self.vwap(df=self.todays_data()[['close', 'volume']].iloc[::-1].astype(float))
        except ValueError:
            return pd.DataFrame(columns=['close', 'volume', 'vwap', 'p_one_sd', 'n_one_sd'])

    def weekly_vwap(self):
        try:
            return self.vwap(df=self.weeks_data()[['close', 'volume']].iloc[::-1].astype(float))
        except ValueError:
            return pd.DataFrame(columns=['close', 'volume', 'vwap', '+1sd', '-1sd'])

    def intraday_vpoc(self):
        try:
            return self.vpoc(df=self.todays_data()[['close', 'volume']].iloc[::-1].astype(float))
        except ValueError:
            return pd.DataFrame(columns=['close', 'volume', 'agrclose', 'vpoc'])

    def intraday_sma(self, max_timestamp):
        lookback_time = max_timestamp - datetime.timedelta(minutes=1400)
        df = self.ieod_data[self.ieod_data.index >= lookback_time][['close']].iloc[::-1]
        try:
            return self.sma(df=df)
        except ValueError:
            pd.DataFrame(columns=['close', 'sma10', 'sma20', 'sma50', 'sma100', 'sma200'])

    def volume_delta(self):
        try:  # cumulative of minute level buying and selling
            return self.delta(df=self.todays_data()[['close', 'volume']].iloc[::-1].astype(float))
        except ValueError:
            return pd.DataFrame(columns=['close', 'volume', 'buyvol', 'sellvol', 'delta', 'cumm_delta'])

    def intraday_delta_divergence_short(self):
        try:
            vol_delta = self.volume_delta()
            return self.divergence(df=vol_delta[['close', 'delta']], series1=vol_delta['close'],
                                   series2=vol_delta['cumm_delta'],
                                   period=LookbackPeriod.objects.all().values_list('delta_divergence_short', flat=True)[0],
                                   filter_val=5)
        except ValueError:
            return pd.DataFrame(columns=['close', 'delta', 'pos_score', 'neg_score', 'net_score'])

    def intraday_delta_divergence_long(self):
        try:
            vol_delta = self.volume_delta()
            return self.divergence(df=vol_delta[['close', 'delta']], series1=vol_delta['close'],
                                   series2=vol_delta['cumm_delta'],
                                   period=LookbackPeriod.objects.all().values_list('delta_divergence_long', flat=True)[0],
                                   filter_val=15)
        except ValueError:
            return pd.DataFrame(columns=['close', 'delta', 'pos_score', 'neg_score', 'net_score'])

    def intraday_rsi_divergence_short(self):
        try:
            lookback = LookbackPeriod.objects.all().values_list('rsi_short', flat=True)[0]
            rsi = self.rsi(close=self.todays_data()[['close']].iloc[::-1].astype(float),
                           period=lookback)
            return self.divergence(df=rsi[['close', 'rsi']], series1=rsi['close'], series2=rsi['rsi'],
                                   period=lookback, filter_val=7)
        except ValueError:
            return pd.DataFrame(columns=['close', 'rsi', 'pos_score', 'neg_score', 'net_score'])

    def intraday_rsi_divergence_long(self):
        try:
            lookback = LookbackPeriod.objects.all().values_list('rsi_long', flat=True)[0]
            rsi = self.rsi(close=self.todays_data()[['close']].iloc[::-1].astype(float),
                           period=lookback)
            return self.divergence(df=rsi[['close', 'rsi']], series1=rsi['close'], series2=rsi['rsi'],
                                   period=lookback, filter_val=15)
        except ValueError:
            return pd.DataFrame(columns=['close', 'rsi', 'pos_score', 'neg_score', 'net_score'])

    def intraday_vol_divergence(self):
        try:
            data = self.todays_data().iloc[::-1].astype(float)
            return self.divergence(df=data[['close', 'volume']], series1=data['close'], series2=data['volume'],
                                   period=LookbackPeriod.objects.all().values_list('vol_divergence', flat=True)[0],
                                   filter_val=5)
        except ValueError:
            return pd.DataFrame(columns=['close', 'volume', 'pos_score', 'neg_score', 'net_score'])

    def intraday_adx_divergence_short(self):
        try:
            data = self.todays_data().iloc[::-1].astype(float)
            lookback = LookbackPeriod.objects.all().values_list('adx_divergence_short', flat=True)[0]
            adx = self.adx(df=data[['high', 'low', 'close']], period=lookback)
            adv_div = self.divergence(df=adx[['close', 'p_di_period']], series1=adx['close'], series2=adx['p_di_period'],
                                      period=lookback, filter_val=5)
            adv_div = adv_div.rename(columns={adv_div.columns[2]: 'p_pos_score', adv_div.columns[3]: 'p_neg_score',
                                              adv_div.columns[4]: 'p_net_score'})
            dec_div = self.divergence(df=adx[['close', 'n_di_period']], series1=adx['close'], series2=adx['n_di_period'],
                                      period=lookback, filter_val=5)
            dec_div = dec_div.rename(columns={dec_div.columns[2]: 'n_pos_score', dec_div.columns[3]: 'n_neg_score',
                                              dec_div.columns[4]: 'n_net_score'})
            dec_div = dec_div.drop(['close'], axis=1)
            adx_div = pd.merge(adv_div, dec_div, left_index=True, right_index=True)
            return adx_div
        except ValueError:
            pass

    def intraday_adx_divergence_long(self):
        try:
            data = self.todays_data().iloc[::-1].astype(float)
            lookback = LookbackPeriod.objects.all().values_list('adx_divergence_long', flat=True)[0]
            adx = self.adx(df=data[['high', 'low', 'close']], period=lookback)
            adv_div = self.divergence(df=adx[['close', 'p_di_period']], series1=adx['close'], series2=adx['p_di_period'],
                                      period=lookback, filter_val=5)
            adv_div = adv_div.rename(columns={adv_div.columns[2]: 'p_pos_score', adv_div.columns[3]: 'p_neg_score',
                                              adv_div.columns[4]: 'p_net_score'})
            dec_div = self.divergence(df=adx[['close', 'n_di_period']], series1=adx['close'], series2=adx['n_di_period'],
                                      period=lookback, filter_val=5)
            dec_div = dec_div.rename(columns={dec_div.columns[2]: 'n_pos_score', dec_div.columns[3]: 'n_neg_score',
                                              dec_div.columns[4]: 'n_net_score'})
            dec_div = dec_div.drop(['close'], axis=1)
            adx_div = pd.merge(adv_div, dec_div, left_index=True, right_index=True)
            return adx_div
        except ValueError:
            pass


def xls_write(df, file_name):
    df.index = df.index.tz_localize(None)
    writer = pd.ExcelWriter(file_name)
    df.to_excel(writer)
    return writer.save()


# inst_1 = SymbolList.objects.all().values_list('symbol', flat=True)[0]
# id = IntradayData(inst_1)
# ieod_data = id.full_data()
# adx_df = IntradayIndicators(ieod_data).intraday_adx_divergence_long()
# print(adx_df.to_string())
# xls_write(adx_df, 'adx_div_14.xls')
