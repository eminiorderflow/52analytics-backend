from channels.routing import ProtocolTypeRouter
from pivots.routing import websockets

application = ProtocolTypeRouter({
    "websocket": websockets,
})