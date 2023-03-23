from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from goods_info.models import GoodsCategoryModel


class CategorySerializer(ModelSerializer):
    """
    商品的序列化器
    """
    class Meta:
        model = GoodsCategoryModel
        fields = "__all__"


class CategoryListSerializer(ModelSerializer):
    """
    商品的序列化器
    """
    children = serializers.SerializerMethodField(read_only=True)  # 为了显示树形的类别结构

    class Meta:
        model = GoodsCategoryModel
        fields = "__all__"

    def get_children(self, obj):  # 函数的命名为: get_属性名字
        if obj.children:
            return CategorySerializer(obj.children, many=True).data
        else:
            return None
