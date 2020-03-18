import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime


class Calculations:

    @staticmethod
    def initial_balance(df):
        df = df.rename(columns={df.columns[0]: 'high', df.columns[1]: 'low'})
        df = df.reindex(columns=df.columns.tolist() + ['ib_high', 'ib_low'])
        df['ib_high'] = max(df.head(60)['high'])  # 60 points for one hour
        df['ib_low'] = min(df.head(60)['low'])
        df.fillna(0, inplace=True)
        return df[['ib_high', 'ib_low']]

    @staticmethod
    def vwap(df):
        df = df.rename(columns={df.columns[0]: 'close', df.columns[1]: 'volume'})
        df = df.reindex(columns=df.columns.tolist() + ['pv', 'vwap'])
        df['pv'] = df.apply(lambda x: x['close']*x['volume'], axis=1)
        df['vwap'] = df['pv'].expanding().sum()/df['volume'].expanding().sum()
        df['sd'] = df[['vwap']].expanding().std()
        df['p_one_sd'] = df.apply(lambda x: x['vwap'] + x['sd'], axis=1)
        df['n_one_sd'] = df.apply(lambda x: x['vwap'] - x['sd'], axis=1)
        df.fillna(0, inplace=True)
        return df[['close', 'volume', 'vwap', 'p_one_sd', 'n_one_sd']]

    @staticmethod
    def vpoc(df):
        df = df.rename(columns={df.columns[0]: 'close', df.columns[1]: 'volume'})
        df = df.reindex(columns=df.columns.tolist() + ['agrclose', 'vpoc'])
        cal = 0 if df['close'].max() > 500 else 1  # price > 500 is calibrated with 0
        df['agrclose'] = round(df['close'], cal)
        for i in range(len(df)):
            try:
                new_df = df[['agrclose', 'volume']][1:i].groupby(['agrclose']).sum()  # omit 1st row as it is high vol
                df['vpoc'].iloc[i] = new_df['volume'].idxmax()  # i aggregates the volume on the current row
            except ValueError:
                pass
        df.fillna(0, inplace=True)
        return df

    @staticmethod
    def sma(df):
        df = df.rename(columns={df.columns[0]: 'close'})
        df = df.reindex(columns=df.columns.tolist() + ['sma10', 'sma20', 'sma50', 'sma100', 'sma200'])
        df['sma10'] = df['close'].rolling(window=10).sum()/10
        df['sma20'] = df['close'].rolling(window=20).sum() / 20
        df['sma50'] = df['close'].rolling(window=50).sum() / 50
        df['sma100'] = df['close'].rolling(window=100).sum() / 100
        df['sma200'] = df['close'].rolling(window=200).sum() / 200
        df.fillna(0, inplace=True)
        return df

    @staticmethod
    def buysellvol2(close, volume):
        buyvol = []
        sellvol = []
        for index, closing in enumerate(close):
            try:
                if closing >= close[index - 1]:
                    buyvol.append(volume[index])
                else:
                    sellvol.append(volume[index])
            except IndexError:
                pass
        return sum(buyvol), sum(sellvol)

    @staticmethod
    def delta(df):
        df = df.rename(columns={df.columns[0]: 'close', df.columns[1]: 'volume'})
        df = df.reindex(columns=df.columns.tolist() + ['buyvol', 'sellvol', 'aggbuy', 'aggsell', 'delta'])
        df['buyvol'] = np.where(df['close'] >= df['close'].shift(), df['volume'], 0)
        df['sellvol'] = np.where(df['close'] < df['close'].shift(), df['volume'], 0)
        df['delta'] = df['buyvol'] - df['sellvol']
        df['cumm_delta'] = df['delta'].expanding().sum()
        pd.set_option('display.max_columns', 50)
        return df

    @staticmethod
    def rsi(close, period):
        """Add a decorator function to keep the close variable global and only run on new data"""
        close = close.rename(columns={close.columns[0]: 'close'})
        close = close.reindex(columns=close.columns.tolist() + ['change', 'gain', 'loss', 'avg_gain',
                                                                'avg_loss', 'rs', 'result'])
        close['change'] = close['close'] - close['close'].shift()
        close['gain'] = close.apply(lambda x: x['change'] if x['change'] > 0 else 0, axis=1)
        close['loss'] = close.apply(lambda x: abs(x['change']) if x['change'] < 0 else 0, axis=1)
        for i in range(len(close.index)):
            if i < period:
                close['avg_gain'].iloc[i] = 0
                close['avg_loss'].iloc[i] = 0
            elif i == period:
                close['avg_gain'].iloc[i] = close['gain'].iloc[1:i + 1].sum() / period
                close['avg_loss'].iloc[i] = close['loss'].iloc[1:i + 1].sum() / period
            else:
                close['avg_gain'].iloc[i] = (close['avg_gain'].iloc[i - 1] * (period - 1) + close['gain'].iloc[
                    i])/period
                close['avg_loss'].iloc[i] = (close['avg_loss'].iloc[i - 1] * (period - 1) + close['loss'].iloc[
                    i]) / period
        close['rs'] = close.apply(lambda x: x['avg_gain']/x['avg_loss'] if x['avg_loss'] != 0 else 100, axis=1)
        close['rsi'] = close.apply(lambda x: 100-(100/(1 + x['rs'])) if x['avg_loss'] != 0 else 100, axis=1)
        pd.set_option('display.max_columns', 50)
        return close

    @staticmethod
    def adx(df, period):
        df = df.rename(columns={df.columns[0]: 'high', df.columns[1]: 'low', df.columns[2]: 'close'})
        df = df.reindex(columns=df.columns.tolist() + ['prev_high', 'prev_low', 'prev_close', 'tr', 'p_dm1', 'n_dm1',
                                                       'tr_period', 'p_dm_period', 'n_dm_period', 'p_di_period',
                                                       'n_di_period', 'di_period_diff', 'di_period_sum', 'dx', 'adx'])
        df['prev_high'] = df['high'].shift()
        df['prev_low'] = df['low'].shift()
        df['prev_close'] = df['close'].shift()
        df['tr'] = df.apply(lambda x: max(x['high'] - x['low'], abs(x['high'] - x['prev_close']),
                                          abs(x['low'] - x['prev_close'])), axis=1)
        df['p_dm1'] = df.apply(lambda x: max(x['low'] - x['prev_low'], 0)
                               if x['low'] - x['prev_low'] > x['prev_high'] - x['high'] else 0, axis=1)
        df['n_dm1'] = df.apply(lambda x: max(x['prev_high'] - x['high'], 0)
                               if x['prev_high'] - x['high'] > x['low'] - x['prev_low'] else 0, axis=1)
        for i in range(len(df.index)):
            if i < period:
                df['tr_period'].iloc[i] = 0
                df['p_dm_period'].iloc[i] = 0
                df['n_dm_period'].iloc[i] = 0
                df['p_di_period'].iloc[i] = 0
                df['n_di_period'].iloc[i] = 0
                df['di_period_diff'].iloc[i] = 0
            elif i == period:
                df['tr_period'].iloc[i] = df['tr'].iloc[1:i + 1].sum()
                df['p_dm_period'].iloc[i] = df['p_dm1'].iloc[1:i + 1].sum()
                df['n_dm_period'].iloc[i] = df['n_dm1'].iloc[1:i + 1].sum()
                df['p_di_period'].iloc[i] = (df['p_dm_period'].iloc[i] / df['tr_period'].iloc[i]) * 100
                df['n_di_period'].iloc[i] = (df['n_dm_period'].iloc[i] / df['tr_period'].iloc[i]) * 100
                df['di_period_diff'].iloc[i] = abs(df['p_di_period'].iloc[i] - df['n_di_period'].iloc[i])
                df['di_period_sum'].iloc[i] = df['p_di_period'].iloc[i] + df['n_di_period'].iloc[i]
                df['dx'].iloc[i] = (df['di_period_diff'].iloc[i] / df['di_period_sum'].iloc[i]) * 100
            else:
                df['tr_period'].iloc[i] = df['tr_period'].iloc[i - 1] - df['tr_period'].iloc[i - 1]/period + \
                                          df['tr'].iloc[i]
                df['p_dm_period'].iloc[i] = df['p_dm_period'].iloc[i - 1] - df['p_dm_period'].iloc[i - 1] / period + \
                                            df['p_dm1'].iloc[i]
                df['n_dm_period'].iloc[i] = df['n_dm_period'].iloc[i - 1] - df['n_dm_period'].iloc[i - 1] / period + \
                                            df['n_dm1'].iloc[i]
                df['p_di_period'].iloc[i] = (df['p_dm_period'].iloc[i] / df['tr_period'].iloc[i]) * 100
                df['n_di_period'].iloc[i] = (df['n_dm_period'].iloc[i] / df['tr_period'].iloc[i]) * 100
                df['di_period_diff'].iloc[i] = abs(df['p_di_period'].iloc[i] - df['n_di_period'].iloc[i])
                df['di_period_sum'].iloc[i] = df['p_di_period'].iloc[i] + df['n_di_period'].iloc[i]
                df['dx'].iloc[i] = (df['di_period_diff'].iloc[i] / df['di_period_sum'].iloc[i]) * 100
        df['adx'] = df['dx'].rolling(window=period).sum()/period
        df.fillna(0, inplace=True)
        return df

    @staticmethod
    def divergence(df, series1, series2, period, filter_val):
        """
        Method calculates the continuous iterative divergence
        :param df: Input dataframe with which results need to be appended
        :param series1: series on which divergence needs to be spotted
        :param series2: Indicator with which series1 is diverging
        :param period: lookback period to calculate the div
        :param filter_val: filter out the values smaller than period minus this value
        :return: dataframe with the inputs, positive & negative score and net score (divergence)
        """
        output = []
        for i in range(0, len(series1), 1):
            pos_score = 0
            neg_score = 0
            for j in range(min(i, period), 1, -1):
                try:
                    if (series2[i] - series2[i-j] >= 0) and (series1[i] - series1[i-j] < 0):
                        pos_score += 1
                    if (series2[i] - series2[i-j]) < 0 and (series1[i] - series1[i-j] >= 0):
                        neg_score += 1
                except IndexError:
                    pass
                continue
            output.append([pos_score, neg_score, neg_score - pos_score])
        dv_score = pd.DataFrame(output, columns=['pos_score', 'neg_score', 'net_score'])
        dv_score = pd.concat([df, dv_score.set_index(df.index)], axis=1)
        dv_score['net_score'] = dv_score.apply(
            lambda x: 0 if abs(x['net_score']) < period - filter_val else x['net_score'], axis=1)
        return dv_score

    @staticmethod
    def ohlc(df):
        new_df = pd.DataFrame({}, index=[datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')])
        new_df['high'] = max(df['high'])
        new_df['low'] = min(df['low'])
        return new_df

    @staticmethod
    def plot(df):
        df.plot(y=['close'])
        sec = df['delta'].plot(secondary_y=True)
        sec.set_ylabel('delta')
        return plt.show()
