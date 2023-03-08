from rest_framework.serializers import ModelSerializer

from erp_system.models import MenuModel


class MenuSerializer(ModelSerializer):
    """功能菜单的序列化类"""
    class Meta:
        model = MenuModel
        fields = '__all__'