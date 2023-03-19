from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from basic_info.models import WarehouseModel


class WarehouseSerializer(ModelSerializer):
    """仓库的序列化类"""
    class Meta:
        model = WarehouseModel
        fields = '__all__'

class WarehouseSearchSerializer(ModelSerializer):
    """仓库的序列化类"""
    leader_user = serializers.SlugRelatedField(slug_field='real_name', read_only=True)

    class Meta:
        model = WarehouseModel
        fields = '__all__'
