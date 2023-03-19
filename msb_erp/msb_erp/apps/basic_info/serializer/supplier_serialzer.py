from rest_framework.serializers import ModelSerializer

from basic_info.models import SupplierModel


class SupplierSerializer(ModelSerializer):
    """供应商的序列化类"""
    class Meta:
        model = SupplierModel
        fields = '__all__'