from datetime import datetime

from rest_framework import serializers


class BlockSerializer(serializers.Serializer):
    hash = serializers.CharField()
    height = serializers.IntegerField()
    time = serializers.IntegerField()
    time_into_datetime = serializers.SerializerMethodField('get_time')
    block_index = serializers.IntegerField()

    def get_time(self, instance):
        to_datetime = datetime.fromtimestamp(instance['time'])
        datetime_string = to_datetime.strftime("%d-%b-%Y (%H:%M:%S)")
        return datetime_string


class BlockTransactionSerializer(serializers.Serializer):
    hash = serializers.CharField()
    time = serializers.IntegerField()
    time_into_datetime = serializers.SerializerMethodField('get_time')
    size = serializers.IntegerField()
    weight = serializers.IntegerField()
    fee = serializers.IntegerField()

    def get_time(self, instance):
        to_datetime = datetime.fromtimestamp(instance['time'])
        datetime_string = to_datetime.strftime("%d-%b-%Y (%H:%M:%S)")
        return datetime_string


class BlockDetailsSerializer(serializers.Serializer):
    hash = serializers.CharField()
    time = serializers.IntegerField()
    time_into_datetime = serializers.SerializerMethodField('get_time')
    fee = serializers.IntegerField()
    size = serializers.IntegerField()
    height = serializers.IntegerField()
    weight = serializers.IntegerField()

    def get_time(self, instance):
        print('innstance', dict(instance))
        to_datetime = datetime.fromtimestamp(dict(instance)['time'])
        datetime_string = to_datetime.strftime("%d-%b-%Y (%H:%M:%S)")
        return datetime_string
