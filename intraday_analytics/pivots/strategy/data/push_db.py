from pivots.strategy.indicators.intraday.intraday_indicators import IntradayIndicators, IntradayData
from pivots.strategy.indicators.eod.eod_indicators import EODIndicators, EODData
from pivots.strategy.data.data_pull import SymbolList, IntradaySMA, MetaTable, IntradayVWAP, WeeklyVWAP, IntradayVPOC, \
    IntradayIB, IntradayDelDivShort, IntradayDelDivLong, IntradayRSIDivShort, IntradayRSIDivLong, IntradayADXDivShort, \
    IntradayADXDivLong, IntradayVolDiv, EodTodayOHLC, EodYestOHLC, EodWeekHL, EodMonthHL, EodYearHL, EodYtdHL, EodSMA, \
    EodMonthVWAP, EODYearVWAP, EODYearVPOC, IntradayMinuteData
from django.utils import timezone
from intraday_analytics._celery import app
import logging
import datetime
import threading
import multiprocessing


logger = logging.getLogger('intraday_analytics.tasks')
inst_1 = SymbolList.objects.all().values_list('symbol', flat=True)[0]


# noinspection PyUnresolvedReferences
class IntradayStrategy:

    def __init__(self, symbol, ieod_data):
        self.symbol = symbol
        self.ieod_data = ieod_data
        self.ii = IntradayIndicators(ieod_data)

    def run_intraday_data(self):
        logger.info(f"intraday data starts {timezone.now()}")
        try:
            max_timestamp = MetaTable.objects.filter(table_name='IntradayMinuteData').values_list('max_timestamp')[0][0]
            intra_data = self.ii.ieod_data[self.ii.ieod_data.index >= max_timestamp]
        except Exception as exc:
            logger.exception(exc)
            intra_data = self.ii.ieod_data
        for data in intra_data.itertuples():
            IntradayMinuteData.objects.get_or_create(symbol=self.symbol, timestamp=data.Index,
                                                     defaults={"open": data.open, "high": data.high, "low": data.low,
                                                               "close": data.close, "volume": data.volume,
                                                               "last_fetch": timezone.now()})
            MetaTable(table_name='IntradayMinuteData',
                      max_timestamp=IntradayMinuteData.objects.values_list('timestamp').order_by('-timestamp')[0][0],
                      last_fetch=timezone.now()).save()
        logger.info(f"intraday data ends {timezone.now()}")

    def run_intraday_sma(self):
        logger.info(f"intraday sma starts {timezone.now()}")
        try:
            max_timestamp = MetaTable.objects.filter(table_name='IntradaySMA').values_list('max_timestamp')[0][0]
        except Exception as exc:
            logger.exception(exc)
            max_timestamp = timezone.now() - timezone.timedelta(days=100)
        for sma in self.ii.intraday_sma(max_timestamp).itertuples():
            IntradaySMA.objects.get_or_create(symbol=self.symbol, timestamp=sma.Index,
                                              defaults={"close": sma.close, "sma10": sma.sma10, "sma20": sma.sma20,
                                                        "sma50": sma.sma50, "sma100": sma.sma100,
                                                        "sma200": sma.sma200, "last_fetch": timezone.now()})
        MetaTable(table_name='IntradaySMA',
                  max_timestamp=IntradaySMA.objects.values_list('timestamp').order_by('-timestamp')[0][0],
                  last_fetch=timezone.now()).save()
        logger.info(f"intraday sma ends {timezone.now()}")

    def run_intraday_vwap(self):
        logger.info(f"vwap starts {timezone.now()}")
        for vwap in self.ii.intraday_vwap().itertuples():
            IntradayVWAP.objects.get_or_create(symbol=self.symbol, timestamp=vwap.Index,
                                               defaults={"close": vwap.close, "volume": vwap.volume,
                                                         "vwap": vwap.vwap, "p_one_sd": vwap.p_one_sd,
                                                         "n_one_sd": vwap.n_one_sd, "last_fetch": timezone.now()})
        logger.info(f"vwap ends {timezone.now()}")

    def run_weekly_vwap(self):
        logger.info(f"weekly vwap starts {timezone.now()}")
        for vwap in self.ii.weekly_vwap().itertuples():
            WeeklyVWAP.objects.get_or_create(symbol=self.symbol, timestamp=vwap.Index,
                                             defaults={"close": vwap.close, "volume": vwap.volume, "vwap": vwap.vwap,
                                                       "p_one_sd": vwap.p_one_sd, "n_one_sd": vwap.n_one_sd,
                                                       "last_fetch": timezone.now()})
        logger.info(f"weekly vwap ends {timezone.now()}")

    def run_intraday_vpoc(self):
        logger.info(f"intraday vpoc starts {timezone.now()}")
        for vpoc in self.ii.intraday_vpoc().itertuples():
            IntradayVPOC.objects.get_or_create(symbol=self.symbol, timestamp=vpoc.Index,
                                               defaults={"close": vpoc.close, "volume": vpoc.volume,
                                                         "agrclose": vpoc.agrclose, "vpoc": vpoc.vpoc,
                                                         "last_fetch": timezone.now()})
        logger.info(f"intraday vpoc ends {timezone.now()}")

    def run_intraday_ib(self):
        logger.info(f"intraday ib starts {timezone.now()}")
        for ib in self.ii.intraday_initial_balance().itertuples():
            IntradayIB.objects.get_or_create(symbol=self.symbol, timestamp=ib.Index,
                                             defaults={"ib_high": ib.ib_high, "ib_low": ib.ib_low,
                                                       "last_fetch": timezone.now()})
        logger.info(f"intraday ib ends {timezone.now()}")

    def run_intraday_deldiv(self):
        logger.info(f"intraday del div starts {timezone.now()}")
        for div in self.ii.intraday_delta_divergence_short().itertuples():
            IntradayDelDivShort.objects.get_or_create(symbol=self.symbol, timestamp=div.Index,
                                                      defaults={"close": div.close, "delta": div.delta,
                                                                "pos_score": div.pos_score, "neg_score": div.neg_score,
                                                                "net_score": div.net_score, "last_fetch": timezone.now()})
        for div in self.ii.intraday_delta_divergence_long().itertuples():
            IntradayDelDivLong.objects.get_or_create(symbol=self.symbol, timestamp=div.Index,
                                                     defaults={"close": div.close, "delta": div.delta,
                                                               "pos_score": div.pos_score, "neg_score": div.neg_score,
                                                               "net_score": div.net_score, "last_fetch": timezone.now()})
        logger.info(f"intraday del div ends {timezone.now()}")

    def run_intraday_rsidiv(self):
        logger.info(f"intraday rsi div starts {timezone.now()}")
        for div in self.ii.intraday_rsi_divergence_short().itertuples():
            IntradayRSIDivShort.objects.get_or_create(symbol=self.symbol, timestamp=div.Index,
                                                      defaults={"close": div.close, "rsi": div.rsi,
                                                                "pos_score": div.pos_score, "neg_score": div.neg_score,
                                                                "net_score": div.net_score, "last_fetch": timezone.now()})
        for div in self.ii.intraday_rsi_divergence_long().itertuples():
            IntradayRSIDivLong.objects.get_or_create(symbol=self.symbol, timestamp=div.Index,
                                                     defaults={"close": div.close, "rsi": div.rsi,
                                                               "pos_score": div.pos_score, "neg_score": div.neg_score,
                                                               "net_score": div.net_score, "last_fetch": timezone.now()})
        logger.info(f"intraday rsi div ends {timezone.now()}")

    def run_intraday_adxdiv(self):
        logger.info(f"intraday adx div starts {timezone.now()}")
        for div in self.ii.intraday_adx_divergence_short().itertuples():
            IntradayADXDivShort.objects.get_or_create(symbol=self.symbol, timestamp=div.Index,
                                                      defaults={"close": div.close, "p_di_period": div.p_di_period,
                                                                "p_pos_score": div.p_pos_score,
                                                                "p_neg_score": div.p_neg_score,
                                                                "p_net_score": div.p_net_score,
                                                                "n_di_period": div.n_di_period,
                                                                "n_pos_score": div.n_pos_score,
                                                                "n_neg_score": div.n_neg_score,
                                                                "n_net_score": div.n_net_score,
                                                                "last_fetch": timezone.now()})
        for div in self.ii.intraday_adx_divergence_long().itertuples():
            IntradayADXDivLong.objects.get_or_create(symbol=self.symbol, timestamp=div.Index,
                                                     defaults={"close": div.close, "p_di_period": div.p_di_period,
                                                               "p_pos_score": div.p_pos_score,
                                                               "p_neg_score": div.p_neg_score,
                                                               "p_net_score": div.p_net_score,
                                                               "n_di_period": div.n_di_period,
                                                               "n_pos_score": div.n_pos_score,
                                                               "n_neg_score": div.n_neg_score,
                                                               "n_net_score": div.n_net_score,
                                                               "last_fetch": timezone.now()})
        logger.info(f"intraday adx div ends {timezone.now()}")

    def run_intraday_voldiv(self):
        logger.info(f"intraday vol div starts {timezone.now()}")
        for div in self.ii.intraday_vol_divergence().itertuples():
            IntradayVolDiv.objects.get_or_create(symbol=self.symbol, timestamp=div.Index,
                                                 defaults={"close": div.close, "volume": div.volume,
                                                           "pos_score": div.pos_score, "neg_score": div.neg_score,
                                                           "net_score": div.net_score, "last_fetch": timezone.now()})
        logger.info(f"intraday vol div ends {timezone.now()}")


class EODStrategy:

    def __init__(self, symbol, eod_data):
        self.symbol = symbol
        self.eod_data = eod_data
        self.ei = EODIndicators(eod_data)

    def run_eod_today_ohlc(self):
        logger.info(f"EOD today ohlc starts {timezone.now()}")
        for lvl in self.ei.todays_ohlc().itertuples():
            EodTodayOHLC.objects.update_or_create(symbol=self.symbol, date=lvl.Index,
                                                  defaults={"open": lvl.open, "high": lvl.high, "low": lvl.low,
                                                            "close": lvl.close, "volume": lvl.volume,
                                                            "last_fetch": timezone.now()})
        logger.info(f"EOD today ohlc ends {timezone.now()}")

    def run_eod_yest_ohlc(self):
        logger.info(f"EOD yesterday ohlc starts {timezone.now()}")
        for lvl in self.ei.yesterday_ohlc().itertuples():
            EodYestOHLC.objects.update_or_create(symbol=self.symbol, date= datetime.datetime.today(),  #date=lvl.Index,
                                                 defaults={"open": lvl.open, "high": lvl.high, "low": lvl.low,
                                                           "close": lvl.close, "volume": lvl.volume,
                                                           "last_fetch": timezone.now()})
        logger.info(f"EOD yesterday ohlc ends {timezone.now()}")

    def run_eod_week_ohlc(self):
        logger.info(f"EOD week ohlc starts {timezone.now()}")
        for lvl in self.ei.week_high_low().itertuples():
            EodWeekHL.objects.update_or_create(symbol=self.symbol, date=lvl.Index,
                                               defaults={"high": lvl.high, "low": lvl.low,
                                                         "last_fetch": timezone.now()})
        logger.info(f"EOD week ohlc ends {timezone.now()}")

    def run_eod_month_ohlc(self):
        logger.info(f"EOD month ohlc starts {timezone.now()}")
        for lvl in self.ei.month_high_low().itertuples():
            EodMonthHL.objects.update_or_create(symbol=self.symbol, date=lvl.Index,
                                                defaults={"high": lvl.high, "low": lvl.low,
                                                          "last_fetch": timezone.now()})
        logger.info(f"EOD month ohlc ends {timezone.now()}")

    def run_eod_year_ohlc(self):
        logger.info(f"EOD year ohlc starts {timezone.now()}")
        for lvl in self.ei.year_high_low().itertuples():
            EodYearHL.objects.update_or_create(symbol=self.symbol, date=lvl.Index,
                                               defaults={"high": lvl.high, "low": lvl.low,
                                                         "last_fetch": timezone.now()})
        logger.info(f"EOD year ohlc ends {timezone.now()}")

    def run_eod_ytd_ohlc(self):
        logger.info(f"EOD ytd ohlc starts {timezone.now()}")
        for lvl in self.ei.ytd_high_low().itertuples():
            EodYtdHL.objects.update_or_create(symbol=self.symbol, date=lvl.Index,
                                              defaults={"high": lvl.high, "low": lvl.low,
                                                        "last_fetch": timezone.now()})
        logger.info(f"EOD ytd ohlc ends {timezone.now()}")

    def run_eod_sma(self):
        logger.info(f"eod sma starts {timezone.now()}")
        for sma in self.ei.eod_sma().itertuples():
            EodSMA.objects.update_or_create(symbol=self.symbol, date=sma.Index,
                                            defaults={"close": sma.close, "sma10": sma.sma10, "sma20": sma.sma20,
                                                      "sma50": sma.sma50, "sma100": sma.sma100, "sma200": sma.sma200,
                                                      "last_fetch": timezone.now()})
        logger.info(f"eod sma ends {timezone.now()}")

    def run_eod_month_vwap(self):
        logger.info(f"eod month vwap starts {timezone.now()}")
        for vwap in self.ei.month_vwap().itertuples():
            EodMonthVWAP.objects.update_or_create(symbol=self.symbol, date=vwap.Index,
                                                  defaults={"close": vwap.close, "volume": vwap.volume, "vwap": vwap.vwap,
                                                            "p_one_sd": vwap.p_one_sd, "n_one_sd": vwap.p_one_sd,
                                                            "last_fetch": timezone.now()})
        logger.info(f"eod month vwap ends {timezone.now()}")

    def run_eod_year_vwap(self):
        logger.info(f"eod year vwap starts {timezone.now()}")
        for vwap in self.ei.year_vwap().itertuples():
            EODYearVWAP.objects.update_or_create(symbol=self.symbol, date=vwap.Index,
                                                 defaults={"close": vwap.close, "volume": vwap.volume, "vwap": vwap.vwap,
                                                           "p_one_sd": vwap.p_one_sd, "n_one_sd": vwap.p_one_sd,
                                                           "last_fetch": timezone.now()})
        logger.info(f"eod year vwap ends {timezone.now()}")

    def run_eod_year_vpoc(self):
        logger.info(f"eod year vpoc starts {timezone.now()}")
        for vpoc in self.ei.year_vpoc().itertuples():
            EODYearVPOC.objects.update_or_create(symbol=self.symbol, date=vpoc.Index,
                                                 defaults={"close": vpoc.close, "volume": vpoc.volume,
                                                           "agrclose": vpoc.agrclose, "vpoc": vpoc.vpoc,
                                                           "last_fetch": timezone.now()})
        logger.info(f"eod year vpoc ends {timezone.now()}")


@app.task
def intraday_tasks():
    id = IntradayData(inst_1)
    ieod_data = id.full_data()
    intraday_strategy = IntradayStrategy(inst_1, ieod_data)
    intraday_strategy.run_intraday_data()
    intraday_strategy.run_intraday_sma()
    intraday_strategy.run_weekly_vwap()
    intraday_strategy.run_intraday_vwap()
    intraday_strategy.run_intraday_vpoc()
    intraday_strategy.run_intraday_ib()
    intraday_strategy.run_intraday_rsidiv()
    intraday_strategy.run_intraday_adxdiv()
    intraday_strategy.run_intraday_voldiv()
    intraday_strategy.run_intraday_deldiv()


@app.task
def eod_tasks():
    ed = EODData(inst_1)
    eod_data = ed.full_data()
    eod_strategy = EODStrategy(inst_1, eod_data)
    eod_strategy.run_eod_today_ohlc()
    eod_strategy.run_eod_yest_ohlc()
    eod_strategy.run_eod_week_ohlc()
    eod_strategy.run_eod_month_ohlc()
    eod_strategy.run_eod_year_ohlc()
    eod_strategy.run_eod_ytd_ohlc()
    eod_strategy.run_eod_sma()
    eod_strategy.run_eod_month_vwap()
    eod_strategy.run_eod_year_vwap()
    eod_strategy.run_eod_year_vpoc()


# eod_tasks()
# p1 = multiprocessing.Process(target=strategy.run_intraday_sma)
# p2 = multiprocessing.Process(target=strategy.run_intraday_vwap)
# p3 = multiprocessing.Process(target=strategy.run_weekly_vwap)
# p4 = multiprocessing.Process(target=strategy.run_intraday_vpoc)
# p5 = multiprocessing.Process(target=strategy.run_intraday_ib)
# p6 = multiprocessing.Process(target=strategy.run_intraday_deldiv)
# p1.start()
# p2.start()
# p3.start()
# p4.start()
# p5.start()
# p6.start()




