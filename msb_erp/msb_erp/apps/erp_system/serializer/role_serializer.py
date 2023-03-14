from rest_framework.serializers import ModelSerializer, IntegerField, BooleanField, Serializer

from erp_system.models import RolesModel
from erp_system.serializer.permissions_serializer import PermissionsSerializer


class BaseRolesSerializer(ModelSerializer):
    """
    普通的序列化类,支持:新增,修改角色姓名,删除,查询
    """
    permissions = PermissionsSerializer(many=True, read_only=True)

    class Meta:
        model = RolesModel
        fields = '__all__'


class RolesPartialSerializer(ModelSerializer):
    """
    用于给某一个角色批量授权的序列化
    """

    class Meta:
        model = RolesModel
        fields = ['id', 'permissions']


class RoleSetPermissionSerializer(Serializer):
    """
    用于给某一个角色单一授权,包括取消授权
    """
    # 角色id
    role_id = IntegerField(write_only=True, required=True)
    # 权限id
    permission_id = IntegerField(write_only=True, required=True)
    # 是否是:新授予权限(Ture),还是取消(False)
    is_create = BooleanField(write_only=True, required=True)
