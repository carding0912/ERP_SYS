from rest_framework.serializers import ModelSerializer

from basic_info.models import CustomerModel


class CustomerSerializer(ModelSerializer):
    """客户的序列化类"""
    class Meta:
        model = CustomerModel
        fields = '__all__'