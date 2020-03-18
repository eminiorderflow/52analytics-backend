import plotly.graph_objects as go
import pandas as pd
from pivots.strategy.data.data_pull import IntradayMinuteData


df = pd.DataFrame(IntradayMinuteData.objects.all().values())

fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

# fig.show()

# fig = go.Figure(data=go.Bar(y=[10, 2, 3, 1]))
fig.write_html('first_figure.html', auto_open=True)
