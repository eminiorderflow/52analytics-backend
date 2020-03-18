from django.urls import path

from channels.routing import URLRouter

from .consumer import LiveMarketData

websockets = URLRouter([
    path("ws/live-market-data/", LiveMarketData, name="live-market-data")
])