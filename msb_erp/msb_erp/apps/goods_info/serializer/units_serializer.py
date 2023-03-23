from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from goods_info.models import UnitsModel


class UnitsSerializer(ModelSerializer):
    """
    计量单位的序列化器和反序列化器
    """
    units_name = serializers.SerializerMethodField(read_only=True)  # 增加一个新属性,把基本单位和副单位结合在一起

    class Meta:
        model = UnitsModel
        fields = "__all__"

    def get_units_name(self, obj):
        return str(obj)
