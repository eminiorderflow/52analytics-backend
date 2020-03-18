from rest_framework import serializers

from pivots.models import IntradayMinuteData


class IntradayAnalyticsSerializer(serializers.ModelSerializer):

    class Meta:
        model = IntradayMinuteData
        fields = '__all__'
