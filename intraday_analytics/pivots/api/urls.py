# from django standard library
from django.conf.urls import url
from .views import IntradayAnalyticsAPIView

urlpatterns = [
    url(r'^intraday_analytics/$', IntradayAnalyticsAPIView.as_view(), name='intraday_analytics'),
]