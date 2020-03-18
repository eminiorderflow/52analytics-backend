from rest_framework import generics, views
from rest_framework.response import Response
from django.db import connection


class IntradayAnalyticsAPIView(views.APIView):

    def get(self, request):

        output_list = []
        with connection.cursor() as cursor:
            cursor.execute('''SELECT * FROM 
                            (SELECT intra_min.id, intra_min.symbol, intra_min.timestamp, intra_min.open, intra_min.high, 
                            intra_min.low, intra_min.close, intra_min.volume, 
                            intra_sma.sma10, intra_sma.sma20, intra_sma.sma50, intra_sma.sma100, intra_sma.sma200,
                            intra_vwap.vwap AS intra_vwap, intra_vwap.p_one_sd AS intra_p_one_sd, 
                            intra_vwap.n_one_sd AS intra_n_one_sd, intra_vpoc.vpoc AS intra_vpoc,
                            intra_ib.ib_high, intra_ib.ib_low,
                            wk_vwap.vwap AS week_vwap, wk_vwap.p_one_sd AS week_p_one_sd, wk_vwap.n_one_sd AS week_n_one_sd,
                            eod_month_vwap.vwap AS month_vwap, eod_year_vwap.vwap AS year_vwap,
                            eod_sma.sma10 AS eod_sma10, eod_sma.sma20 AS eod_sma20, eod_sma.sma50 AS eod_sma50, eod_sma.sma100 AS eod_sma100, eod_sma.sma200 AS eod_sma200,
                            eod_today_ohlc.open AS intra_open, eod_today_ohlc.high AS intra_high, eod_today_ohlc.low AS intra_low,
                            eod_yest_ohlc.open AS yest_open, eod_yest_ohlc.high AS yest_high, eod_yest_ohlc.low AS yest_low, eod_yest_ohlc.close AS yest_close,
                            eod_week_hl.high AS week_high, eod_week_hl.low AS week_low,
                            eod_month_hl.high AS month_high, eod_month_hl.low AS month_low,
                            eod_ytd_hl.high AS ytd_high, eod_ytd_hl.low AS ytd_low,
                            eod_year_hl.high AS year_high, eod_year_hl.low AS year_low,
                            intra_vol_div.net_score AS vol_div,
                            intra_rsi_div_short.net_score AS rsi_div_short,
                            intra_rsi_div_long.net_score AS rsi_div_long,
                            intra_adx_div_short.p_net_score AS adx_div_p_short, intra_adx_div_short.n_net_score AS adx_div_n_short,
                            intra_adx_div_long.p_net_score AS adx_div_p_long, intra_adx_div_long.n_net_score AS adx_div_n_long,
                            intra_del_div_short.net_score AS del_div_short,
                            intra_del_div_long.net_score AS del_div_long
                            FROM public.pivots_intradayminutedata intra_min
                            INNER JOIN public.pivots_intradaysma intra_sma 
                            ON intra_min.timestamp = intra_sma.timestamp 
                            INNER JOIN public.pivots_intradayvwap intra_vwap
                            ON intra_min.timestamp = intra_vwap.timestamp 
                            INNER JOIN public.pivots_intradayvpoc intra_vpoc
                            ON intra_min.timestamp = intra_vpoc.timestamp   
                            INNER JOIN public.pivots_intradayib intra_ib
                            ON intra_min.timestamp = intra_ib.timestamp 
                            INNER JOIN public.pivots_weeklyvwap wk_vwap
                            ON intra_min.timestamp = wk_vwap.timestamp
                            INNER JOIN public.pivots_intradayvoldiv intra_vol_div 
                            ON intra_min.timestamp = intra_vol_div.timestamp
                            INNER JOIN public.pivots_intradayrsidivshort intra_rsi_div_short 
                            ON intra_min.timestamp = intra_rsi_div_short.timestamp
                            INNER JOIN public.pivots_intradayrsidivlong intra_rsi_div_long 
                            ON intra_min.timestamp = intra_rsi_div_long.timestamp
                            INNER JOIN public.pivots_intradayadxdivshort intra_adx_div_short
                            ON intra_min.timestamp = intra_adx_div_short.timestamp
                            INNER JOIN public.pivots_intradayadxdivlong intra_adx_div_long
                            ON intra_min.timestamp = intra_adx_div_long.timestamp
                            INNER JOIN public.pivots_intradaydeldivshort intra_del_div_short 
                            ON intra_min.timestamp = intra_del_div_short.timestamp 
                            INNER JOIN public.pivots_intradaydeldivlong intra_del_div_long
                            ON intra_min.timestamp = intra_del_div_long.timestamp 
                            INNER JOIN public.pivots_eodmonthvwap eod_month_vwap
                            ON CAST(intra_min.timestamp AS DATE) = eod_month_vwap.date  
                            INNER JOIN public.pivots_eodyearvwap eod_year_vwap
                            ON CAST(intra_min.timestamp AS DATE) = eod_year_vwap.date
                            INNER JOIN public.pivots_eodsma eod_sma
                            ON CAST(intra_min.timestamp AS DATE) = eod_sma.date
                            INNER JOIN public.pivots_eodtodayohlc eod_today_ohlc
                            ON CAST(intra_min.timestamp AS DATE) = eod_today_ohlc.date
                            LEFT JOIN public.pivots_eodyestohlc eod_yest_ohlc
                            ON CAST(intra_min.timestamp AS DATE) = eod_yest_ohlc.date
                            INNER JOIN public.pivots_eodweekhl eod_week_hl
                            ON CAST(intra_min.timestamp AS DATE) = eod_week_hl.date
                            LEFT JOIN public.pivots_eodmonthhl eod_month_hl
                            ON CAST(intra_min.timestamp AS DATE) = eod_month_hl.date
                            LEFT JOIN public.pivots_eodytdhl eod_ytd_hl
                            ON CAST(intra_min.timestamp AS DATE) = eod_ytd_hl.date
                            LEFT JOIN public.pivots_eodyearhl eod_year_hl 
                            ON CAST(intra_min.timestamp AS DATE) = eod_year_hl.date
                            ORDER BY intra_min.timestamp DESC LIMIT 360) AS pivots ORDER BY pivots.timestamp;''')

            cursor_data = cursor.fetchall()

            for row in cursor_data:
                output_list.append({'id': row[0], 'symbol': row[1], 'timestamp': row[2].timestamp() * 1000,
                                    'open': row[3], 'high': row[4], 'low': row[5], 'close': row[6], 'volume': row[7],
                                    'sma10': row[8], 'sma20': row[9], 'sma50': row[10], 'sma100': row[11], 'sma200': row[12],
                                    'intra_vwap': row[13], 'intra_p_one_sd': row[14], 'intra_n_one_sd': row[15],
                                    'intra_vpoc': row[16], 'ib_high': row[17], 'ib_low': row[18],
                                    'week_vwap': row[19], 'week_p_one_sd': row[20], 'week_n_one_sd': row[21],
                                    'month_vwap': row[22], 'year_vwap': row[23], 'eod_sma10': row[24], 'eod_sma20': row[25],
                                    'eod_sma50': row[26], 'eod_sma100': row[27], 'eod_sma200': row[28], 'intra_open': row[29],
                                    'intra_high': row[30], 'intra_low': row[31], 'yest_open': row[32], 'yest_high': row[33],
                                    'yest_low': row[34], 'yest_close': row[35], 'week_high': row[36], 'week_low': row[37],
                                    'month_high': row[38], 'month_low': row[39], 'ytd_high': row[40], 'ytd_low': row[41],
                                    'year_high': row[42], 'year_low': row[43], 'vol_div': row[44],
                                    'rsi_div_short': row[45], 'rsi_div_long': row[46], 'adx_div_p_short': row[47],
                                    'adx_div_n_short': row[48], 'adx_div_p_long': row[49], 'adx_div_n_long': row[50],
                                    'del_div_short': row[51], 'del_div_long': row[52]})

        return Response(output_list)
