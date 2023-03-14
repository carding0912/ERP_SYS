from rest_framework.serializers import ModelSerializer

from erp_system.models import PermissionsModel


class PermissionsSerializer(ModelSerializer):

    class Meta:
        model = PermissionsModel
        fields = '__all__'