import json

from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser


from pivots.models import IntradayMinuteData


class LiveMarketData(AsyncWebsocketConsumer):

    async def websocket_connect(self, message):
        pass

    async def websocket_receive(self, message):
        pass

    async def live_data(self, event):
        pass

    async def websocket_disconnect(self, message):
        pass
