# from django standard library
from django.contrib import admin

# from project module
from .models import *

# Register your models here.


admin.site.site_header = '52 Analytics Administration'
admin.site.register([LookbackPeriod, SymbolList])


class IntradayMinuteDataAdmin(admin.ModelAdmin):
    model = IntradayMinuteData
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'timestamp', 'open', 'high', 'low',  'close', 'volume', 'last_fetch', ]
    readonly_fields = ('symbol', 'timestamp', 'open', 'high', 'low',  'close', 'volume', 'last_fetch', )
    list_display_links = ['symbol']


admin.site.register(IntradayMinuteData, IntradayMinuteDataAdmin)


class IntradaySMAAdmin(admin.ModelAdmin):
    model = IntradaySMA
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'timestamp', 'close', 'sma10', 'sma20',  'sma50', 'sma100', 'sma200', 'last_fetch', ]
    readonly_fields = ('symbol', 'timestamp', 'close', 'sma10', 'sma20',  'sma50', 'sma100', 'sma200', 'last_fetch',)
    list_display_links = ['symbol']


admin.site.register(IntradaySMA, IntradaySMAAdmin)


class IntradayVWAPAdmin(admin.ModelAdmin):
    model = IntradayVWAP
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'timestamp', 'close', 'volume', 'vwap',  'p_one_sd', 'n_one_sd', 'last_fetch', ]
    readonly_fields = ('symbol', 'timestamp', 'close', 'volume', 'vwap',  'p_one_sd', 'n_one_sd', 'last_fetch', )
    list_display_links = ['symbol']


admin.site.register(IntradayVWAP, IntradayVWAPAdmin)


class WeeklyVWAPAdmin(admin.ModelAdmin):
    model = WeeklyVWAP
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'timestamp', 'close', 'volume', 'vwap',  'p_one_sd', 'n_one_sd', 'last_fetch', ]
    readonly_fields = ('symbol', 'timestamp', 'close', 'volume', 'vwap',  'p_one_sd', 'n_one_sd', 'last_fetch',)
    list_display_links = ['symbol']


admin.site.register(WeeklyVWAP, WeeklyVWAPAdmin)


class IntradayVPOCAdmin(admin.ModelAdmin):
    model = IntradayVPOC
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'timestamp', 'close', 'volume', 'agrclose',  'vpoc', 'last_fetch',]
    readonly_fields = ('symbol', 'timestamp', 'close', 'volume', 'agrclose',  'vpoc', 'last_fetch',)
    list_display_links = ['symbol']


admin.site.register(IntradayVPOC, IntradayVPOCAdmin)


class IntradayIBAdmin(admin.ModelAdmin):
    model = IntradayIB
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'timestamp', 'ib_high', 'ib_low', 'last_fetch',]
    readonly_fields = ('symbol', 'timestamp', 'ib_high', 'ib_low', 'last_fetch',)
    list_display_links = ['symbol']


admin.site.register(IntradayIB, IntradayIBAdmin)


class IntradayDelDivShortAdmin(admin.ModelAdmin):
    model = IntradayDelDivShort
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'timestamp', 'close', 'delta', 'pos_score', 'neg_score', 'net_score', 'last_fetch',]
    readonly_fields = ('symbol', 'timestamp', 'close', 'delta', 'pos_score', 'neg_score', 'net_score', 'last_fetch',)
    list_display_links = ['symbol']


admin.site.register(IntradayDelDivShort, IntradayDelDivShortAdmin)


class IntradayDelDivLongAdmin(admin.ModelAdmin):
    model = IntradayDelDivLong
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'timestamp', 'close', 'delta', 'pos_score', 'neg_score', 'net_score', 'last_fetch',]
    readonly_fields = ('symbol', 'timestamp', 'close', 'delta', 'pos_score', 'neg_score', 'net_score', 'last_fetch',)
    list_display_links = ['symbol']


admin.site.register(IntradayDelDivLong, IntradayDelDivLongAdmin)


class IntradayRSIDivShortAdmin(admin.ModelAdmin):
    model = IntradayRSIDivShort
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'timestamp', 'close', 'rsi', 'pos_score', 'neg_score', 'net_score', 'last_fetch',]
    readonly_fields = ('symbol', 'timestamp', 'close', 'rsi', 'pos_score', 'neg_score', 'net_score', 'last_fetch',)
    list_display_links = ['symbol']


admin.site.register(IntradayRSIDivShort, IntradayRSIDivShortAdmin)


class IntradayRSIDivLongAdmin(admin.ModelAdmin):
    model = IntradayRSIDivLong
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'timestamp', 'close', 'rsi', 'pos_score', 'neg_score', 'net_score', 'last_fetch',]
    readonly_fields = ('symbol', 'timestamp', 'close', 'rsi', 'pos_score', 'neg_score', 'net_score', 'last_fetch',)
    list_display_links = ['symbol']


admin.site.register(IntradayRSIDivLong, IntradayRSIDivLongAdmin)


class IntradayADXDivShortAdmin(admin.ModelAdmin):
    model = IntradayADXDivShort
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'timestamp', 'close', 'p_di_period', 'p_pos_score', 'p_neg_score', 'p_net_score',
                    'n_di_period', 'n_pos_score', 'n_neg_score', 'n_net_score']
    readonly_fields = ('symbol', 'timestamp', 'close', 'p_di_period', 'p_pos_score', 'p_neg_score', 'p_net_score',
                       'n_di_period', 'n_pos_score', 'n_neg_score', 'n_net_score',)
    list_display_links = ['symbol']


admin.site.register(IntradayADXDivShort, IntradayADXDivShortAdmin)


class IntradayADXDivLongAdmin(admin.ModelAdmin):
    model = IntradayADXDivLong
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'timestamp', 'close', 'p_di_period', 'p_pos_score', 'p_neg_score', 'p_net_score',
                    'n_di_period', 'n_pos_score', 'n_neg_score', 'n_net_score']
    readonly_fields = ('symbol', 'timestamp', 'close', 'p_di_period', 'p_pos_score', 'p_neg_score', 'p_net_score',
                       'n_di_period', 'n_pos_score', 'n_neg_score', 'n_net_score',)
    list_display_links = ['symbol']


admin.site.register(IntradayADXDivLong, IntradayADXDivLongAdmin)


class IntradayVolDivAdmin(admin.ModelAdmin):
    model = IntradayVolDiv
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'timestamp', 'close', 'volume', 'pos_score', 'neg_score', 'net_score', 'last_fetch',]
    readonly_fields = ('symbol', 'timestamp', 'close', 'volume', 'pos_score', 'neg_score', 'net_score', 'last_fetch',)
    list_display_links = ['symbol']


admin.site.register(IntradayVolDiv, IntradayVolDivAdmin)


class EodTodayOHLCAdmin(admin.ModelAdmin):
    model = EodTodayOHLC
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'last_fetch',]
    readonly_fields = ('symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'last_fetch',)
    list_display_links = ['symbol']


admin.site.register(EodTodayOHLC, EodTodayOHLCAdmin)


class EodYestOHLCAdmin(admin.ModelAdmin):
    model = EodYestOHLC
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'last_fetch',]
    readonly_fields = ('symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'last_fetch',)
    list_display_links = ['symbol']


admin.site.register(EodYestOHLC, EodYestOHLCAdmin)


class EodWeekHLAdmin(admin.ModelAdmin):
    model = EodWeekHL
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'date', 'high', 'low', 'last_fetch',]
    readonly_fields = ('symbol', 'date', 'high', 'low', 'last_fetch',)
    list_display_links = ['symbol']


admin.site.register(EodWeekHL, EodWeekHLAdmin)


class EodMonthHLAdmin(admin.ModelAdmin):
    model = EodMonthHL
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'date', 'high', 'low', 'last_fetch',]
    readonly_fields = ('symbol', 'date', 'high', 'low', 'last_fetch',)
    list_display_links = ['symbol']


admin.site.register(EodMonthHL, EodMonthHLAdmin)


class EodYearHLAdmin(admin.ModelAdmin):
    model = EodYearHL
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'date', 'high', 'low', 'last_fetch',]
    readonly_fields = ('symbol', 'date', 'high', 'low', 'last_fetch',)
    list_display_links = ['symbol']


admin.site.register(EodYearHL, EodYearHLAdmin)


class EodYtdHLAdmin(admin.ModelAdmin):
    model = EodYtdHL
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'date', 'high', 'low', 'last_fetch',]
    readonly_fields = ('symbol', 'date', 'high', 'low', 'last_fetch',)
    list_display_links = ['symbol']


admin.site.register(EodYtdHL, EodYtdHLAdmin)


class EodSMAAdmin(admin.ModelAdmin):
    model = EodSMA
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'date', 'close', 'sma10', 'sma20',  'sma50', 'sma100', 'sma200', 'last_fetch', ]
    readonly_fields = ('symbol', 'date', 'close', 'sma10', 'sma20',  'sma50', 'sma100', 'sma200', 'last_fetch',)
    list_display_links = ['symbol']


admin.site.register(EodSMA, EodSMAAdmin)


class EodMonthVWAPAdmin(admin.ModelAdmin):
    model = EodMonthVWAP
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'date', 'close', 'volume', 'vwap', 'p_one_sd', 'n_one_sd', 'last_fetch', ]
    readonly_fields = ('symbol', 'date', 'close', 'volume', 'vwap', 'p_one_sd', 'n_one_sd', 'last_fetch',)
    list_display_links = ['symbol']


admin.site.register(EodMonthVWAP, EodMonthVWAPAdmin)


class EODYearVWAPAdmin(admin.ModelAdmin):
    model = EODYearVWAP
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'date', 'close', 'volume', 'vwap', 'p_one_sd', 'n_one_sd', 'last_fetch', ]
    readonly_fields = ('symbol', 'date', 'close', 'volume', 'vwap', 'p_one_sd', 'n_one_sd', 'last_fetch',)
    list_display_links = ['symbol']


admin.site.register(EODYearVWAP, EODYearVWAPAdmin)


class EODYearVPOCAdmin(admin.ModelAdmin):
    model = EODYearVPOC
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_display = ['symbol', 'date', 'close', 'volume', 'agrclose',  'vpoc', 'last_fetch', ]
    readonly_fields = ('symbol', 'date', 'close', 'volume', 'agrclose',  'vpoc', 'last_fetch',)
    list_display_links = ['symbol']


admin.site.register(EODYearVPOC, EODYearVPOCAdmin)


class MetaTableAdmin(admin.ModelAdmin):
    model = MetaTable
    search_fields = ('table_name',)
    list_filter = ('table_name',)
    list_display = ['table_name', 'max_timestamp', 'last_fetch']
    readonly_fields = ('table_name', 'max_timestamp', 'last_fetch')
    list_display_links = ['table_name']


admin.site.register(MetaTable, MetaTableAdmin)


# class IntradaySMAInline(NestedStackedInline):
#
#     model = IntradaySMA
#     list_display = ['symbol', 'timestamp', 'close', 'sma10', 'sma20',  'sma50', 'sma100', 'sma200', 'last_fetch', ]
#     readonly_fields = ('symbol', 'timestamp', 'close', 'sma10', 'sma20',  'sma50', 'sma100', 'sma200', 'last_fetch',)
#     list_display_links = ['symbol']
#
#
# class SymbolListAdmin(NestedModelAdmin):
#     model = SymbolList
#     inlines = [IntradaySMAInline]
#
#
# admin.site.register(SymbolList, SymbolListAdmin)
