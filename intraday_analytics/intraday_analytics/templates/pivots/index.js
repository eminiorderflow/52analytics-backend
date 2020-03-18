function coloring(y1, y2) {
    if (y1 >= y2) {
        return 'green';
    } else {
        return 'red';}
 }

 function updateLevel(dataset, dataLength, key, name, plot_index){
    chart.yAxis[0].options.plotLines[plot_index].value = dataset[dataLength - 1][key];
    chart.yAxis[0].options.plotLines[plot_index].label.text = [name + ' ' + dataset[dataLength - 1][key]].join(' ');
    chart.yAxis[0].options.plotLines[plot_index].color = coloring(dataset[dataLength - 1]['close'], dataset[dataLength - 1][key]);
    return null;
 }

 function updateBand(dataset, dataLength, key1, key2, plot_index){
    chart.yAxis[0].options.plotBands[plot_index].from = dataset[dataLength - 1][key1];
    chart.yAxis[0].options.plotBands[plot_index].to = dataset[dataLength - 1][key2];
    return null;
 }

Highcharts.getJSON('http://127.0.0.1:8000/pivots/api/intraday_analytics/', function (data) {

    // split the data set into ohlc and volume
    var ohlc = [],
        volume = [],
        sma10 = [],
        sma20 = [],
        sma50 = [],
        sma100 = [],
        sma200 = [],
        ib = [],
        intraday_vwap = [],
        intraday_vpoc = []
        week_vwap = [],
        month_vwap = [],
        year_vwap = [],
        eod_sma = [],
        intra_ohl = [],
        yest_ohlc = [],
        eod_week_hl = [],
        eod_month_hl = [],
        eod_ytd_hl = [],
        eod_year_hl = [],
        vol_div = [],
        rsi_div_short = [],
        rsi_div_long = [],
        adx_div_p_short = [],
        adx_div_n_short = [],
        adx_div_p_long = [],
        adx_div_n_long = [],
        del_div_short = [],
        del_div_long = [],
        dataLength = data.length,
        i = 0;

    for (i; i < dataLength; i += 1) {
        symbol = data[0]['symbol']
        ohlc.push([
            data[i]['timestamp'], // the date
            data[i]['open'], // open
            data[i]['high'], // high
            data[i]['low'], // low
            data[i]['close'] // close
        ]);

        volume.push([
            data[i]['timestamp'], // the date
            data[i]['volume'] // the volume
        ]);

        sma10.push([
            data[i]['timestamp'],
            data[i]['sma10'],
        ]);

        sma20.push([
            data[i]['timestamp'],
            data[i]['sma20'],
        ]);

        sma50.push([
            data[i]['timestamp'],
            data[i]['sma50'],
        ]);

        sma100.push([
            data[i]['timestamp'],
            data[i]['sma100'],
        ]);

        sma200.push([
            data[i]['timestamp'],
            data[i]['sma200'],
        ]);

        intraday_vwap.push([
                data[i]['timestamp'],
                data[i]['intra_vwap'],
                data[i]['intra_p_one_sd'],
                data[i]['intra_n_one_sd']
        ]);

        intraday_vpoc.push([
                data[i]['timestamp'],
                data[i]['intra_vpoc'],
        ]);

        ib.push([
            data[i]['timestamp'],
            data[i]['ib_high'],
            data[i]['ib_low']
        ]);

        week_vwap.push([
                data[i]['timestamp'],
                data[i]['week_vwap'],
                data[i]['week_p_one_sd'],
                data[i]['week_n_one_sd']
        ]);

        month_vwap.push([
                data[i]['timestamp'],
                data[i]['month_vwap'],
        ]);

        year_vwap.push([
                data[i]['timestamp'],
                data[i]['year_vwap'],
        ]);

        eod_sma.push([
                data[i]['timestamp'],
                data[i]['eod_sma10'],
                data[i]['eod_sma20'],
                data[i]['eod_sma50'],
                data[i]['eod_sma100'],
                data[i]['eod_sma200'],
        ]);

         intra_ohl.push([
                data[i]['timestamp'],
                data[i]['intra_open'],
                data[i]['intra_high'],
                data[i]['intra_low'],
        ]);

        yest_ohlc.push([
                data[i]['timestamp'],
                data[i]['yest_open'],
                data[i]['yest_high'],
                data[i]['yest_low'],
                data[i]['yest_close'],
        ]);

        eod_week_hl.push([
                data[i]['timestamp'],
                data[i]['week_high'],
                data[i]['week_low'],
        ]);

        eod_month_hl.push([
                data[i]['timestamp'],
                data[i]['month_high'],
                data[i]['month_low'],
        ]);

        eod_ytd_hl.push([
                data[i]['timestamp'],
                data[i]['ytd_high'],
                data[i]['ytd_low'],
        ]);

        eod_year_hl.push([
                data[i]['timestamp'],
                data[i]['year_high'],
                data[i]['year_low'],
        ]);

        vol_div.push([
            data[i]['timestamp'],
            data[i]['vol_div']
        ]);

        rsi_div_short.push([
            data[i]['timestamp'],
            data[i]['rsi_div_short']
        ]);

        rsi_div_long.push([
            data[i]['timestamp'],
            data[i]['rsi_div_long']
        ]);

        adx_div_p_short.push([
            data[i]['timestamp'],
            data[i]['adx_div_p_short']
        ]);

        adx_div_n_short.push([
            data[i]['timestamp'],
            data[i]['adx_div_n_short']
        ]);

        adx_div_p_long.push([
            data[i]['timestamp'],
            data[i]['adx_div_p_long']
        ]);

        adx_div_n_long.push([
            data[i]['timestamp'],
            data[i]['adx_div_n_long']
        ]);

        del_div_short.push([
            data[i]['timestamp'],
            data[i]['del_div_short'],
        ]);

        del_div_long.push([
            data[i]['timestamp'],
            data[i]['del_div_long']
        ]);
    }

function requestData() {
    $.ajax({
        url: 'http://127.0.0.1:8000/pivots/api/intraday_analytics/',
        success: function(dataset) {
            var series = chart.series[0],
            shift = 0;
            new_ohlc = [dataset[dataLength - 1]['timestamp'], // the date
                        dataset[dataLength - 1]['open'], // open
                        dataset[dataLength - 1]['high'], // high
                        dataset[dataLength - 1]['low'], // low
                        dataset[dataLength - 1]['close'], // close
            ]

            new_vol_div = [dataset[dataLength - 1]['timestamp'],
                           dataset[dataLength - 1]['vol_div']]

            new_rsi_div_short = [dataset[dataLength - 1]['timestamp'],
                                 dataset[dataLength - 1]['rsi_div_short']]

            new_rsi_div_long = [dataset[dataLength - 1]['timestamp'],
                                dataset[dataLength - 1]['rsi_div_long']]

            new_del_div_short = [dataset[dataLength - 1]['timestamp'],
                                 dataset[dataLength - 1]['del_div_short']]

            new_del_div_long = [dataset[dataLength - 1]['timestamp'],
                                dataset[dataLength - 1]['del_div_long']]

            new_adx_div_p_short = [dataset[dataLength - 1]['timestamp'],
                                   dataset[dataLength - 1]['adx_div_p_short']]

            new_adx_div_n_short = [dataset[dataLength - 1]['timestamp'],
                                   dataset[dataLength - 1]['adx_div_n_short']]

            new_adx_div_p_long = [dataset[dataLength - 1]['timestamp'],
                                  dataset[dataLength - 1]['adx_div_p_long']]

            new_adx_div_n_long = [dataset[dataLength - 1]['timestamp'],
                                  dataset[dataLength - 1]['adx_div_n_long']]

            new_sma10 = [dataset[dataLength - 1]['timestamp'],
                         dataset[dataLength - 1]['sma10']]

            new_sma20 = [dataset[dataLength - 1]['timestamp'],
                         dataset[dataLength - 1]['sma20']]

            new_sma50 = [dataset[dataLength - 1]['timestamp'],
                         dataset[dataLength - 1]['sma50']]

            new_sma100 = [dataset[dataLength - 1]['timestamp'],
                          dataset[dataLength - 1]['sma100']]

            new_sma200 = [dataset[dataLength - 1]['timestamp'],
                          dataset[dataLength - 1]['sma200']]

            if (!(ohlc[ohlc.length - 1][0] === dataset[dataLength - 1]['timestamp'])) {
                ohlc.push(new_ohlc);
                chart.series[0].addPoint(new_ohlc, true, shift);
                chart.series[1].addPoint(new_vol_div, true, shift);
                chart.series[2].addPoint(new_vol_div, true, shift);
                chart.series[3].addPoint(new_vol_div, true, shift);
                chart.series[4].addPoint(new_vol_div, true, shift);
                chart.series[5].addPoint(new_rsi_div_short, true, shift);
                chart.series[6].addPoint(new_rsi_div_long, true, shift);
                chart.series[7].addPoint(new_del_div_short, true, shift);
                chart.series[8].addPoint(new_del_div_long, true, shift);

                chart.series[9].addPoint(new_sma10, true, shift);
                chart.series[10].addPoint(new_sma20, true, shift);
                chart.series[11].addPoint(new_sma50, true, shift);
                chart.series[12].addPoint(new_sma100, true, shift);
                chart.series[12].addPoint(new_sma200, true, shift);

                updateLevel(dataset, dataLength, 'intra_vwap', 'Intraday VWAP', 0);
                updateBand(dataset=dataset, dataLength=dataLength, key1='intra_p_one_sd', key2='intra_n_one_sd', plot_index=0);

                updateLevel(dataset, dataLength, 'intra_vpoc', 'Intraday VPOC', 1);

                updateLevel(dataset, dataLength, 'ib_high', 'IB High', 2);
                updateLevel(dataset, dataLength, 'ib_low', 'IB Low', 3);

                updateLevel(dataset, dataLength, 'week_vwap', 'Week VWAP', 4);
                updateBand(dataset=dataset, dataLength=dataLength, key1='week_p_one_sd', key2='week_n_one_sd', plot_index=1);

                updateLevel(dataset, dataLength, 'month_vwap', 'Month VWAP', 5);
                updateLevel(dataset, dataLength, 'year_vwap', 'Year VWAP', 6);

                updateLevel(dataset, dataLength, 'eod_sma10', 'EOD SMA10', 7);
                updateLevel(dataset, dataLength, 'eod_sma20', 'EOD SMA20', 8);
                updateLevel(dataset, dataLength, 'eod_sma50', 'EOD SMA50', 9);
                updateLevel(dataset, dataLength, 'eod_sma100', 'EOD SMA100', 10);
                updateLevel(dataset, dataLength, 'eod_sma200', 'EOD SMA200', 11);

                updateLevel(dataset, dataLength, 'intra_open', 'Intraday Open', 12);
                updateLevel(dataset, dataLength, 'intra_high', 'Intraday High', 13);
                updateLevel(dataset, dataLength, 'intra_low', 'Intraday Low', 14);

                updateLevel(dataset, dataLength, 'yest_open', 'Yesterday Open', 15);
                updateLevel(dataset, dataLength, 'yest_high', 'Yesterday High', 16);
                updateLevel(dataset, dataLength, 'yest_low', 'Yesterday Low', 17);
                updateLevel(dataset, dataLength, 'yest_close', 'Yesterday Close', 18);

                updateLevel(dataset, dataLength, 'week_high', 'EOD Week High', 19);
                updateLevel(dataset, dataLength, 'week_low', 'EOD Week Low', 20);
                updateLevel(dataset, dataLength, 'month_high', 'EOD Month High', 21);
                updateLevel(dataset, dataLength, 'month_low', 'EOD Month Low', 22);
                updateLevel(dataset, dataLength, 'ytd_high', 'EOD YTD High', 23);
                updateLevel(dataset, dataLength, 'ytd_low', 'EOD YTD Low', 24);
                updateLevel(dataset, dataLength, 'year_high', 'EOD Year High', 25);
                updateLevel(dataset, dataLength, 'year_low', 'EOD Year Low', 26);

                chart.yAxis[0].update();
                chart.yAxis[0].render();
                };
            setTimeout(requestData, 5000);
        },
        cache: false
    });
}

// create the chart
chart = Highcharts.stockChart('container', {

    displayErrors: true,

    chart: {
        events: {
            load: requestData
        },
        panning:{
            enabled:true,
            type: "x",
        },
    },
    title: {
        text: symbol
    },

    xAxis: {
            crosshair: true,
            type: 'datetime',
            dateTimeLabelFormats: {
                time: '%H:%M:%S'
            },
            dataGrouping: {
                units: [
                        ["minute", [1]]
                    ],
            },
//            scrollbar: {   //Doesnt help with candle consolidation problem
//                enabled: true
//            }

    },
    yAxis: [
//        {
//            crosshair: true,
//        },
        {
            startOnTick: false,
            endOnTick: false,
            height: '70%',
            resize: {
                enabled: true
            },
            labels: {
                align: 'right',
                x: -3
            },
            offset: 50,
            resize: {
                enabled: true
            },
            plotBands: [
                {
                    color: '#AFD9FB', // Color value
                    opacity: 0.1,
                    zIndex: -1,
                    from: intraday_vwap[dataLength - 1][2], // Start of the plot band
                    to: intraday_vwap[dataLength - 1][3] // End of the plot band
                },
                {
                    color: '#F3CCFE', // Color value
                    opacity: 0.1,
                    zIndex: -1,
                    from: week_vwap[dataLength - 1][2], // Start of the plot band
                    to: week_vwap[dataLength - 1][3] // End of the plot band
                },
              ],
            plotLines: [
                {
                    value: intraday_vwap[dataLength - 1][1],
                    color: coloring(ohlc[ohlc.length - 1][4], intraday_vwap[dataLength - 1][1]),
                    dashStyle: 'shortdash',
                    width: 1.5,
                    label: {
                        text: ['Intraday VWAP  ' + intraday_vwap[dataLength - 1][1]].join(' '),
                        align: 'center',
                    }
                },
                {
                    value: intraday_vpoc[dataLength - 1][1],
                    color: coloring(ohlc[ohlc.length - 1][4], intraday_vpoc[dataLength - 1][1]),
                    dashStyle: 'shortdash',
                    width: 1.5,
                    label: {
                        text: ['Intraday VPOC  ' + intraday_vpoc[dataLength - 1][1]].join(' '),
                        align: 'center',
                    }
                },
                {
                    value: ib[dataLength - 1][1],
                    color: coloring(ohlc[ohlc.length - 1][4], ib[dataLength - 1][1]),
                    dashStyle: 'shortdash',
                    width: 1.5,
                    label: {
                        text: ['IB High  ' + ib[dataLength - 1][1]].join(' '),
                        align: 'center',
                    }
                },
                {
                    value: ib[dataLength - 1][2],
                    color: coloring(ohlc[ohlc.length - 1][4], ib[dataLength - 1][2]),
                    dashStyle: 'shortdash',
                    width: 1.5,
                    label: {
                        text: ['IB Low  ' + ib[dataLength - 1][2]].join(' '),
                        align: 'center',
                    }
                },
                {

                    value: week_vwap[dataLength - 1][1],
                    color: coloring(ohlc[ohlc.length - 1][4], week_vwap[dataLength - 1][1]),
                    dashStyle: 'solid',
                    width: 1.5,
                    label: {
                        text: ['Week VWAP  ' + week_vwap[dataLength - 1][1]].join(' ')
                    }
                },
                {

                    value: month_vwap[dataLength - 1][1],
                    color: coloring(ohlc[ohlc.length - 1][4], month_vwap[dataLength - 1][1]),
                    dashStyle: 'solid',
                    width: 1.5,
                    label: {
                        text: ['Month VWAP  ' + month_vwap[dataLength - 1][1]].join(' ')
                    }
                },
                {

                    value: year_vwap[dataLength - 1][1],
                    color: coloring(ohlc[ohlc.length - 1][4], year_vwap[dataLength - 1][1]),
                    dashStyle: 'solid',
                    width: 1.5,
                    label: {
                        text: ['Year VWAP  ' + year_vwap[dataLength - 1][1]].join(' ')
                    }
                },
                {
                    value: eod_sma[dataLength - 1][1],
                    color: coloring(ohlc[ohlc.length - 1][4], eod_sma[dataLength - 1][1]),
                    dashStyle: 'solid',
                    width: 1.5,
                    label: {
                        text: ['EOD SMA10  ' + eod_sma[dataLength - 1][1]].join(' ')
                    }
                },
                {
                    value: eod_sma[dataLength - 1][2],
                    color: coloring(ohlc[ohlc.length - 1][4], eod_sma[dataLength - 1][2]),
                    dashStyle: 'solid',
                    width: 1.5,
                    label: {
                        text: ['EOD SMA20  ' + eod_sma[dataLength - 1][2]].join(' ')
                    }
                },
                {
                    value: eod_sma[dataLength - 1][3],
                    color: coloring(ohlc[ohlc.length - 1][4], eod_sma[dataLength - 1][3]),
                    dashStyle: 'solid',
                    width: 1.5,
                    label: {
                        text: ['EOD SMA50  ' + eod_sma[dataLength - 1][3]].join(' ')
                    }
                },
                {
                    value: eod_sma[dataLength - 1][4],
                    color: coloring(ohlc[ohlc.length - 1][4], eod_sma[dataLength - 1][4]),
                    dashStyle: 'solid',
                    width: 1.5,
                    label: {
                        text: ['EOD SMA100  ' + eod_sma[dataLength - 1][4]].join(' ')
                    }
                },
                {
                    value: eod_sma[dataLength - 1][5],
                    color: coloring(ohlc[ohlc.length - 1][4], eod_sma[dataLength - 1][5]),
                    dashStyle: 'solid',
                    width: 1.5,
                    label: {
                        text: ['EOD SMA200  ' + eod_sma[dataLength - 1][5]].join(' ')
                    }
                },
                {
                    value: intra_ohl[dataLength - 1][1],
                    color: coloring(ohlc[ohlc.length - 1][4], intra_ohl[dataLength - 1][1]),
                    dashStyle: 'shortdash',
                    width: 1.5,
                    label: {
                        text: ['Intraday Open  ' + intra_ohl[dataLength - 1][1]].join(' '),
                        align: 'center',
                    }
                },
                {
                    value: intra_ohl[dataLength - 1][2],
                    color: coloring(ohlc[ohlc.length - 1][4], intra_ohl[dataLength - 1][2]),
                    dashStyle: 'shortdash',
                    width: 1.5,
                    label: {
                        text: ['Intraday High  ' + intra_ohl[dataLength - 1][2]].join(' '),
                        align: 'center',
                    }
                },
                {
                    value: intra_ohl[dataLength - 1][3],
                    color: coloring(ohlc[ohlc.length - 1][4], intra_ohl[dataLength - 1][3]),
                    dashStyle: 'shortdash',
                    width: 1.5,
                    label: {
                        text: ['Intraday Low  ' + intra_ohl[dataLength - 1][3]].join(' '),
                        align: 'center',
                    }
                },
                {
                    value: yest_ohlc[dataLength - 1][1],
                    color: coloring(ohlc[ohlc.length - 1][4], yest_ohlc[dataLength - 1][1]),
                    dashStyle: 'shortdash',
                    width: 1.5,
                    label: {
                        text: ['Yesterday Open  ' + yest_ohlc[dataLength - 1][1]].join(' ')
                    }
                },
                {
                    value: yest_ohlc[dataLength - 1][2],
                    color: coloring(ohlc[ohlc.length - 1][4], yest_ohlc[dataLength - 1][2]),
                    dashStyle: 'shortdash',
                    width: 1.5,
                    label: {
                        text: ['Yesterday High  ' + yest_ohlc[dataLength - 1][2]].join(' ')
                    }
                },
                {
                    value: yest_ohlc[dataLength - 1][3],
                    color: coloring(ohlc[ohlc.length - 1][4], yest_ohlc[dataLength - 1][3]),
                    dashStyle: 'shortdash',
                    width: 1.5,
                    label: {
                        text: ['Yesterday Low  ' + yest_ohlc[dataLength - 1][3]].join(' ')
                    }
                },
                {
                    value: yest_ohlc[dataLength - 1][4],
                    color: coloring(ohlc[ohlc.length - 1][4], yest_ohlc[dataLength - 1][4]),
                    dashStyle: 'shortdash',
                    width: 1.5,
                    label: {
                        text: ['Yesterday Close  ' + yest_ohlc[dataLength - 1][4]].join(' ')
                    }
                },
                {
                    value: eod_week_hl[dataLength - 1][1],
                    color: coloring(ohlc[ohlc.length - 1][4], eod_week_hl[dataLength - 1][1]),
                    dashStyle: 'solid',
                    width: 1.5,
                    label: {
                        text: ['EOD Week High  ' + eod_week_hl[dataLength - 1][1]].join(' ')
                    }
                },
                {

                    value: eod_week_hl[dataLength - 1][2],
                    color: coloring(ohlc[ohlc.length - 1][4], eod_week_hl[dataLength - 1][2]),
                    dashStyle: 'solid',
                    width: 1.5,
                    label: {
                        text: ['EOD Week Low  ' + eod_week_hl[dataLength - 1][2]].join(' ')
                    }
                },
                {
                    value: eod_month_hl[dataLength - 1][1],
                    color: coloring(ohlc[ohlc.length - 1][4], eod_month_hl[dataLength - 1][1]),
                    dashStyle: 'solid',
                    width: 1.5,
                    label: {
                        text: ['EOD Month High  ' + eod_month_hl[dataLength - 1][1]].join(' ')
                    }
                },
                {

                    value: eod_month_hl[dataLength - 1][2],
                    color: coloring(ohlc[ohlc.length - 1][4], eod_month_hl[dataLength - 1][2]),
                    dashStyle: 'solid',
                    width: 1.5,
                    label: {
                        text: ['EOD Month Low  ' + eod_month_hl[dataLength - 1][2]].join(' ')
                    }
                },
                {
                    value: eod_ytd_hl[dataLength - 1][1],
                    color: coloring(ohlc[ohlc.length - 1][4], eod_ytd_hl[dataLength - 1][1]),
                    dashStyle: 'solid',
                    width: 1.5,
                    label: {
                        text: ['EOD YTD High  ' + eod_ytd_hl[dataLength - 1][1]].join(' ')
                    }
                },
                {

                    value: eod_ytd_hl[dataLength - 1][2],
                    color: coloring(ohlc[ohlc.length - 1][4], eod_ytd_hl[dataLength - 1][2]),
                    dashStyle: 'solid',
                    width: 1.5,
                    label: {
                        text: ['EOD YTD Low  ' + eod_ytd_hl[dataLength - 1][2]].join(' ')
                    }
                },
                {
                    value: eod_year_hl[dataLength - 1][1],
                    color: coloring(ohlc[ohlc.length - 1][4], eod_year_hl[dataLength - 1][1]),
                    dashStyle: 'solid',
                    width: 1.5,
                    label: {
                        text: ['EOD Year High  ' + eod_year_hl[dataLength - 1][1]].join(' ')
                    }
                },
                {

                    value: eod_year_hl[dataLength - 1][2],
                    color: coloring(ohlc[ohlc.length - 1][4], eod_year_hl[dataLength - 1][2]),
                    dashStyle: 'solid',
                    width: 1.5,
                    label: {
                        text: ['EOD Year Low  ' + eod_year_hl[dataLength - 1][2]].join(' ')
                    }
                },
                ]
        },
        {
            top: '70%',
            height: '10%',
            labels: {
                align: 'right',
                x: -3
            },
            offset: 50,
            title: {
                text: 'Vol Div'
            }
        },
        {
            top: '80%',
            height: '10%',
            labels: {
                align: 'right',
                x: -3
            },
            offset: 50,
            title: {
                text: 'RSD'
            }
        },
        {
            top: '90%',
            height: '10%',
            labels: {
                align: 'right',
                x: -3
            },
            offset: 50,
            title: {
                text: 'DeD'
            }
        },
        ],

    tooltip: {
        split: true
    },
    navigator: {
            enabled: false
    },
    rangeSelector: {
        enabled: false
    },
    plotOptions: {
        series: {
            gapSize: 10
        },
        dataGrouping: {
            enabled: false
        },
        candlestick:{
               color: '#D57D6B',
               upColor: '#DDDDDD'
        },
        column: {
                grouping: false,
                shadow: false
        },
    },
    series: [{
        type: 'candlestick',
        id: 'price_chart',
        name: symbol,
        data: ohlc,
    },
    {
        type: 'column',
        name: 'ADX Divergence P Short',
        data: adx_div_p_short,
        yAxis: 1,
        linkedTo: 'price_chart',
        color: '#EF4D00',
        opacity: '0.6'
    },
    {
        type: 'column',
        name: 'ADX Divergence N Short',
        data: adx_div_n_short,
        yAxis: 1,
        linkedTo: 'price_chart',
        color: '#EF4D00',
        opacity: '0.6'
    },
    {
        type: 'column',
        name: 'ADX Divergence P Long',
        data: adx_div_p_long,
        yAxis: 1,
        linkedTo: 'price_chart',
        color: '#018D85',
        opacity: '0.6'
    },
    {
        type: 'column',
        name: 'ADX Divergence N Long',
        data: adx_div_n_long,
        yAxis: 1,
        linkedTo: 'price_chart',
        color: '#018D85',
        opacity: '0.6'
    },
    {
        type: 'column',
        name: 'RSI Divergence Short',
        data: rsi_div_short,
        yAxis: 2,
        linkedTo: 'price_chart',
        color: '#EF4D00',
        opacity: '0.6'
    },
    {
        type: 'column',
        name: 'RSI Divergence Long',
        data: rsi_div_long,
        yAxis: 2,
        linkedTo: 'price_chart',
        color: '#018D85',
        opacity: '0.6'
    },
    {
        type: 'column',
        name: 'Delta Divergence Short',
        data: del_div_short,
        yAxis: 3,
        linkedTo: 'price_chart',
        color: '#EF4D00',
        opacity: '0.6'
    },
    {
        type: 'column',
        name: 'Delta Divergence Long',
        data: del_div_long,
        yAxis: 3,
        linkedTo: 'price_chart',
        color: '#018D85',
        opacity: '0.6'
    },
    {
        type: 'spline',
        name: 'SMA 10',
        data: sma10,
        yAxis: 0,
        linkedTo: 'price_chart',
        color: '#9DA103',
        opacity: '1'
    },
    {
        type: 'spline',
        name: 'SMA 20',
        data: sma20,
        yAxis: 0,
        linkedTo: 'price_chart',
        color: '#3FA103',
        opacity: '1'
    },
    {
        type: 'spline',
        name: 'SMA 50',
        data: sma50,
        yAxis: 0,
        linkedTo: 'price_chart',
        color: '#037AA1',
        opacity: '1'
    },
    {
        type: 'spline',
        name: 'SMA 100',
        data: sma100,
        yAxis: 0,
        linkedTo: 'price_chart',
        color: '#5303A1',
        opacity: '1'
    },
    {
        type: 'spline',
        name: 'SMA 200',
        data: sma200,
        yAxis: 0,
        linkedTo: 'price_chart',
        color: '#A10367',
        opacity: '1'
    },
    ],

    exporting: {
            buttons: [{
              text: 'Zoom Out',
              onclick: function () {
                day_highs = []
                i=0
                for (i; i < ohlc.length; i += 1) {
                    if (!isNaN(ohlc[i][2])) {
                        day_highs.push(ohlc[i][2])
                  }
                }

               max_high = Math.max.apply(Math, day_highs);
               upper_limit = max_high + max_high*0.15 //going 15% above the HOD

               day_lows = []
                i=0
                for (i; i < ohlc.length; i += 1) {
                    if (!isNaN(ohlc[i][3])) {
                        day_lows.push(ohlc[i][3])
                  }
                }

               min_low = Math.max.apply(Math, day_lows);
               lower_limit = min_low - min_low*0.15 //going 15% below the LOD

               chart.yAxis[0].setExtremes(lower_limit, upper_limit);
              },
            },
            {
              text: 'Zoom In',
              onclick: function () {
                chart.yAxis[0].setExtremes(null, null);
              },
            }]
        }

});
});