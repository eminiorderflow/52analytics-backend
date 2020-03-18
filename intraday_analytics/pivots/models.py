from django.db import models
import datetime

# Create your models here.


class SymbolList(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)

    def __str__(self):
        return self.symbol


class LookbackPeriod(models.Model):
    rsi_short = models.IntegerField(blank=False, null=False, default=0)
    rsi_long = models.IntegerField(blank=False, null=False, default=0)
    volume_aggregation = models.IntegerField(blank=False, null=False, default=0)
    rsi_divergence_short = models.IntegerField(blank=False, null=False, default=0)
    rsi_divergence_long = models.IntegerField(blank=False, null=False, default=0)
    vol_divergence = models.IntegerField(blank=False, null=False, default=0)
    delta_divergence_short = models.IntegerField(blank=False, null=False, default=0)
    delta_divergence_long = models.IntegerField(blank=False, null=False, default=0)
    adx_divergence_short = models.IntegerField(blank=False, null=False, default=0)
    adx_divergence_long = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return "Periods"


class IntradayMinuteData(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    timestamp = models.DateTimeField(auto_now_add=False, blank=True)
    open = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    high = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    low = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    close = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        order_with_respect_to = 'timestamp'
        verbose_name_plural = 'Intraday Data'
        unique_together = [['symbol', 'timestamp']]
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return self.symbol


class IntradaySMA(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    timestamp = models.DateTimeField(auto_now_add=False, blank=True)
    close = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    sma10 = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    sma20 = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    sma50 = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    sma100 = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    sma200 = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        order_with_respect_to = 'timestamp'
        verbose_name_plural = 'Intraday SMA'
        unique_together = [['symbol', 'timestamp']]
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return self.symbol


class IntradayVWAP(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    timestamp = models.DateTimeField(auto_now_add=False, blank=True)
    close = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    vwap = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    p_one_sd = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    n_one_sd = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'Intraday VWAP'
        unique_together = [['symbol', 'timestamp']]
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return self.symbol


class WeeklyVWAP(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    timestamp = models.DateTimeField(auto_now_add=False, blank=True)
    close = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    vwap = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    p_one_sd = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    n_one_sd = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'Intraday Weekly VWAP'
        unique_together = [['symbol', 'timestamp']]
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return self.symbol


class IntradayVPOC(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    timestamp = models.DateTimeField(auto_now_add=False, blank=True)
    close = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    agrclose = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    vpoc = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'Intraday VPOC'
        unique_together = [['symbol', 'timestamp']]
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return self.symbol


class IntradayIB(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    timestamp = models.DateTimeField(auto_now_add=False, blank=True)
    ib_high = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    ib_low = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'Intraday IB'
        unique_together = [['symbol', 'timestamp']]
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return self.symbol


class IntradayDelDivShort(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    timestamp = models.DateTimeField(auto_now_add=False, blank=True)
    close = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    delta = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    pos_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    neg_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    net_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'Intraday Del Div Short'
        unique_together = [['symbol', 'timestamp']]
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return self.symbol


class IntradayDelDivLong(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    timestamp = models.DateTimeField(auto_now_add=False, blank=True)
    close = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    delta = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    pos_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    neg_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    net_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'Intraday Del Div Long'
        unique_together = [['symbol', 'timestamp']]
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return self.symbol


class IntradayRSIDivShort(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    timestamp = models.DateTimeField(auto_now_add=False, blank=True)
    close = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    rsi = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    pos_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    neg_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    net_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'Intraday RSI Div Short'
        unique_together = [['symbol', 'timestamp']]
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return self.symbol


class IntradayRSIDivLong(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    timestamp = models.DateTimeField(auto_now_add=False, blank=True)
    close = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    rsi = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    pos_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    neg_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    net_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'Intraday RSI Div Long'
        unique_together = [['symbol', 'timestamp']]
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return self.symbol


class IntradayADXDivShort(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    timestamp = models.DateTimeField(auto_now_add=False, blank=True)
    close = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    p_di_period = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    p_pos_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    p_neg_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    p_net_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    n_di_period = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    n_pos_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    n_neg_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    n_net_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'Intraday ADX Div Short'
        unique_together = [['symbol', 'timestamp']]
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return self.symbol


class IntradayADXDivLong(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    timestamp = models.DateTimeField(auto_now_add=False, blank=True)
    close = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    p_di_period = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    p_pos_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    p_neg_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    p_net_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    n_di_period = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    n_pos_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    n_neg_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    n_net_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'Intraday ADX Div Long'
        unique_together = [['symbol', 'timestamp']]
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return self.symbol


class IntradayVolDiv(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    timestamp = models.DateTimeField(auto_now_add=False, blank=True)
    close = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    pos_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    neg_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    net_score = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'Intraday Vol Div'
        unique_together = [['symbol', 'timestamp']]
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return self.symbol


class EodTodayOHLC(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    date = models.DateField(auto_now_add=False, blank=True)
    open = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    high = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    low = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    close = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'EOD Today OHLC'
        unique_together = [['symbol', 'date']]
        indexes = [
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return self.symbol


class EodYestOHLC(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    date = models.DateField(auto_now_add=False, blank=True)
    open = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    high = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    low = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    close = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'EOD Yesterday OHLC'
        unique_together = [['symbol', 'date']]
        indexes = [
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return self.symbol


class EodWeekHL(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    date = models.DateField(auto_now_add=False, blank=True)
    high = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    low = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'EOD Week HL'
        unique_together = [['symbol', 'date']]
        indexes = [
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return self.symbol


class EodMonthHL(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    date = models.DateField(auto_now_add=False, blank=True)
    high = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    low = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'EOD Month HL'
        unique_together = [['symbol', 'date']]
        indexes = [
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return self.symbol


class EodYearHL(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    date = models.DateField(auto_now_add=False, blank=True)
    high = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    low = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'EOD Year HL'
        unique_together = [['symbol', 'date']]
        indexes = [
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return self.symbol


class EodYtdHL(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    date = models.DateField(auto_now_add=False, blank=True)
    high = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    low = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'EOD Ytd HL'
        unique_together = [['symbol', 'date']]
        indexes = [
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return self.symbol


class EodSMA(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    date = models.DateField(auto_now_add=False, blank=True)
    close = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    sma10 = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    sma20 = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    sma50 = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    sma100 = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    sma200 = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'EOD SMA'
        unique_together = [['symbol', 'date']]
        indexes = [
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return self.symbol


class EodMonthVWAP(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    date = models.DateField(auto_now_add=False, blank=True)
    close = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    vwap = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    p_one_sd = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    n_one_sd = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'EOD Monthly VWAP'
        unique_together = [['symbol', 'date']]
        indexes = [
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return self.symbol


class EODYearVWAP(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    date = models.DateField(auto_now_add=False, blank=True)
    close = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    vwap = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    p_one_sd = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    n_one_sd = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'EOD Yearly VWAP'
        unique_together = [['symbol', 'date']]
        indexes = [
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return self.symbol


class EODYearVPOC(models.Model):
    symbol = models.CharField(blank=True, null=True, max_length=500)
    date = models.DateField(auto_now_add=False, blank=True)
    close = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    volume = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    agrclose = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    vpoc = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'EOD Year VPOC'
        unique_together = [['symbol', 'date']]
        indexes = [
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return self.symbol


class MetaTable(models.Model):
    table_name = models.CharField(primary_key=True, default='', max_length=500)
    max_timestamp = models.DateTimeField(auto_now_add=False, blank=True)
    last_fetch = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['table_name', 'max_timestamp']),
        ]

    # def save(self, *args, **kwargs):
    #     if self.table_name == 'IntradaySMA':
    #         self.max_timestamp = self.fetch_max_timestamp_isma
    #     super(MetaTable, self).save(*args, **kwargs)
    #
    # @property
    # def fetch_max_timestamp_isma(self):
    #     return IntradaySMA.objects.values_list('timestamp').order_by('timestamp')



