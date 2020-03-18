from bokeh.plotting import figure, output_file, show, gridplot
import pandas as pd
from pivots.strategy.data.data_pull import IntradayMinuteData, IntradayRSIDiv
# from bokeh.io import output_file, show
from bokeh.models import CustomJS, ColumnDataSource, HoverTool, NumeralTickFormatter, Range1d, Span, Legend


def candlestick_plot(df, name):
    # Colour scheme for increasing and descending candles
    INCREASING_COLOR = '#33930B'
    DECREASING_COLOR = '#F2583E'

    # Select the datetime format for the x axis depending on the timeframe
    xaxis_dt_format = '%d %b %Y'
    if df['timestamp'][0].hour > 0:
        xaxis_dt_format = '%d %b %Y, %H:%M:%S'

    price = figure(height=250,
                   # sizing_mode='stretch_both',
                   tools="crosshair, pan, xpan, ypan, wheel_zoom",
                   active_drag='pan',
                   active_scroll='wheel_zoom',
                   x_axis_type='linear',
                   y_axis_location="right",
                   # y_range=Range1d(float(min(df['low'])) - 50, float(max(df['high'])) + 50, bounds="auto"),
                   title=name
                   )
    price.yaxis[0].formatter = NumeralTickFormatter(format="₹5.3f")
    inc = df.close > df.open
    dec = ~inc
    width = 0.5
    inc_source = ColumnDataSource(data=dict(
        x1=df.index[inc],
        top1=df.open[inc],
        bottom1=df.close[inc],
        high1=df.high[inc],
        low1=df.low[inc],
        Date1=df.timestamp[inc]
    ))

    dec_source = ColumnDataSource(data=dict(
        x2=df.index[dec],
        top2=df.open[dec],
        bottom2=df.close[dec],
        high2=df.high[dec],
        low2=df.low[dec],
        Date2=df.timestamp[dec]
    ))
    # Plot candles
    # High and low
    price.segment(x0='x1', y0='high1', x1='x1', y1='low1', source=inc_source, color=INCREASING_COLOR)
    price.segment(x0='x2', y0='high2', x1='x2', y1='low2', source=dec_source, color=DECREASING_COLOR)

    # Open and close
    r1 = price.vbar(x='x1', width=width, top='top1', bottom='bottom1', source=inc_source,
                    fill_color=INCREASING_COLOR, line_color="black")
    r2 = price.vbar(x='x2', width=width, top='top2', bottom='bottom2', source=dec_source,
                    fill_color=DECREASING_COLOR, line_color="black")

    hline = Span(location=170, dimension='width', line_color='red', line_width=1.5)
    legend = Legend(items=[("IB_High", [price.line(x=[0, 0.1], y=1, line_width=1.5, color="red")])], location=(5, 170),
                    orientation="horizontal")
    price.add_layout(legend)
    price.renderers.extend([hline])

    # Add on extra lines (e.g. moving averages) here
    # fig.line(x='timestamp', y='open', line_width=2, source=df)

    # Add date labels to x axis
    price.xaxis.major_label_overrides = {
        i: date.strftime(xaxis_dt_format) for i, date in enumerate(pd.to_datetime(df["timestamp"]))
    }

    # Set up the hover tooltip to display some useful data
    price.add_tools(HoverTool(
        renderers=[r1],
        tooltips=[
            ("Open", "@top1"),
            ("High", "@high1"),
            ("Low", "@low1"),
            ("Close", "@bottom1"),
            ("Date", "@Date1{" + xaxis_dt_format + "}"),
        ],
        formatters={
            'Date1': 'datetime',
        }))

    price.add_tools(HoverTool(
        renderers=[r2],
        tooltips=[
            ("Open", "@top2"),
            ("High", "@high2"),
            ("Low", "@low2"),
            ("Close", "@bottom2"),
            ("Date", "@Date2{" + xaxis_dt_format + "}")
        ],
        formatters={
            'Date2': 'datetime'
        }))

    # JavaScript callback function to automatically zoom the Y axis to
    # view the data properly
    source = ColumnDataSource({'Index': df.index, 'High': df.high, 'Low': df.low})
    callback = CustomJS(args={'y_range': price.y_range, 'source': source}, code='''
        clearTimeout(window._autoscale_timeout);
        var Index = source.data.Index,
            Low = source.data.Low,
            High = source.data.High,
            start = cb_obj.start,
            end = cb_obj.end,
            min = Infinity,
            max = -Infinity;
        for (var i=0; i < Index.length; ++i) {
            if (start <= Index[i] && Index[i] <= end) {
                max = Math.max(High[i], max);
                min = Math.min(Low[i], min);
            }
        }
        var pad = (max - min) * .05;
        window._autoscale_timeout = setTimeout(function() {
            y_range.start = min - pad;
            y_range.end = max + pad;
        });
    ''')

    # Finalise the figure
    price.x_range.callback = callback

    df2 = pd.DataFrame(IntradayRSIDiv.objects.all().values().order_by('-timestamp'))
    df2 = df2[::-1]
    df2.index = df2.index[::-1]

    rsidiv = figure(height=50, y_range=(-20, 20))
    rsidiv.multi_line(xs=[df2.index], ys=[df2['net_score']],
                      line_color=['brown', 'grey', 'grey'], line_width=1)
    rsidiv.xaxis.major_label_overrides = {
        i: date.strftime(xaxis_dt_format) for i, date in enumerate(pd.to_datetime(df2["timestamp"]))
    }

    chart = gridplot([[price, None], [rsidiv, None]], sizing_mode='scale_width')
    show(chart)


# Main function
if __name__ == '__main__':
    data_object = IntradayMinuteData.objects
    df = pd.DataFrame(data_object.all().values().order_by('-timestamp'))

    # Reverse the order of the dataframe - comment this out if it flips your chart
    df = df[::-1]
    df.index = df.index[::-1]

    # Convert the dates column to datetime objects
    df["timestamp"] = pd.to_datetime(df["timestamp"], format='%Y-%m-%d %H:%M:%S')  # Adjust this

    output_file(f"templates/{data_object.values_list('symbol')[0][0]} Minute Plot.html")
    candlestick_plot(df, f"{data_object.values_list('symbol')[0][0]} Minute")

