from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from erp_system.models import DeptModel


class DeptSerializer(ModelSerializer):
    """部门的序列化类"""
    # create_time要将日期格式改成字符串格式,以方便前端展示
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = DeptModel
        fields = '__all__'
