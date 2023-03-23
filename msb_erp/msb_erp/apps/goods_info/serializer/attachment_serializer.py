from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from goods_info.models import AttachmentModel


class AttachmentSerializer(ModelSerializer):
    """
    文件管理的正反序列化器
    """
    type_display = serializers.CharField(source='get_a_type_display', read_only=True)

    class Meta:
        model = AttachmentModel
        fields = "__all__"
