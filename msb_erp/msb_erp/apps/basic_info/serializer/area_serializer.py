from rest_framework.serializers import ModelSerializer
from basic_info.models import Nation, Province, City


class NationSerializer(ModelSerializer):
    """国家的序列化类"""
    class Meta:
        model = Nation
        fields = '__all__'


class ProvinceSerializer(ModelSerializer):
    """省份的序列化类"""
    class Meta:
        model = Province
        fields = '__all__'


class CitySerializer(ModelSerializer):
    """城市的序列化类"""
    class Meta:
        model = City
        fields = '__all__'


