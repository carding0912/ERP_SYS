from rest_framework.serializers import ModelSerializer

from basic_info.models import SettlementAccountModel


class SettlementAccountSerializer(ModelSerializer):
    """结算账户的序列化类"""
    class Meta:
        model = SettlementAccountModel
        fields = '__all__'