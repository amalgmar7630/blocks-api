from rest_framework import serializers


class BlockSerializer(serializers.Serializer):
    hash = serializers.CharField()
    height = serializers.IntegerField()
    time = serializers.IntegerField()
    block_index = serializers.IntegerField()


class BlockTransactionSerializer(serializers.Serializer):
    hash = serializers.CharField()
    time = serializers.IntegerField()
    size = serializers.IntegerField()
    weight = serializers.IntegerField()
    fee = serializers.IntegerField()


class BlockDetailsSerializer(serializers.Serializer):
    hash = serializers.CharField()
    time = serializers.IntegerField()
    fee = serializers.IntegerField()
    size = serializers.IntegerField()
    height = serializers.IntegerField()
    weight = serializers.IntegerField()
