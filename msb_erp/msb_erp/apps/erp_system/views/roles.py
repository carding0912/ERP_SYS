from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from erp_system.models import RolesModel, PermissionsModel, MenuModel
from msb_erp.utils.base_views import MultipleDestroyMixin
from erp_system.serializer.role_serializer import RolesPartialSerializer,RoleSetPermissionSerializer,BaseRolesSerializer


#  角色数据库中有一个固定的角色:admin,这个角色代表所有权限,它不能删除
class RolesView(viewsets.ModelViewSet, MultipleDestroyMixin):
    """
    create:
    角色-新增

    角色新增,status:201(成功),return:新增角色信息

    destroy:
    角色--删除 单个角色

    角色删除,status:204(成功),return:None

    multiple_delete:
    角色--批量删除,多个角色

    角色批量删除,status:204(成功),return:None

    update:
    角色--修改,仅仅修改角的名字

    角色修改,status:200(成功),return:修改的角色信息

    partial_update:
    角色--局部修改(角色的批量授权),只能针对某一个角色一次性授权,之前的授权会被覆盖

    角色批量授权,status:200(成功),return:修改后的角色信息


    list:
    角色--获取列表

    角色列表信息,status:200(成功),return:角色信息列表

    set_permission_to_role:
    给单个角色,单一授权,一次只能授予该角色一个permission,也可以取消一个permission
    status:200(成功),return:修改后的角色信息

    """
    queryset = RolesModel.objects.all()

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return RolesPartialSerializer
        elif self.action == 'set_permission_to_role':
            return RoleSetPermissionSerializer
        else:
            return BaseRolesSerializer

    @action(methods=['POST'], detail=False)
    def set_permission_to_role(self, request, *args, **kwargs):
        ser = RoleSetPermissionSerializer(data=request.data)
        if ser.is_valid():  # 参数验证通过了
            # 查询当前的角色
            role = RolesModel.objects.get(id=ser.validated_data.get('role_id'))
            # 查询当前的权限
            permission = PermissionsModel.objects.get(id=ser.validated_data.get('permission_id'))
            if ser.validated_data.get('is_create'):
                # 如果授予一个角色某个子菜单的权限,那么也要授予这个权限的父菜单的权限
                parent_id = MenuModel.objects.filter(id=permission.menu.id).values_list('parent')
                if parent_id:
                    parent_permission = PermissionsModel.objects.get(menu_id=parent_id[0])
                    role.permissions.add(parent_permission)    # 授予这个角色父菜单的权限
                role.permissions.add(permission)  # 把当前的权限授予当前的角色
            else:
                role.permissions.remove(permission)  # 取消权限

            result_ser = BaseRolesSerializer(instance=role)
            return Response(data=result_ser.data)

    # 重写父类的删除函数,因为admin角色不能删除
    def destroy(self, request, *args, **kwargs):
        if self.get_object().name == 'admin':
            return Response(data={'detail': 'admin角色不可删除'}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(self, request, *args, **kwargs)

    del_ids = openapi.Schema(type=openapi.TYPE_OBJECT, required=['ids'], properties={
        'ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER),
                              description='选择哪些需要删除的id列表')
    })

    @swagger_auto_schema(method='delete', request_body=del_ids,
                         operation_description='批量删除菜单 参数: 传参要求是个id列表[id1,id2,id3,...]')
    @action(methods=['delete'], detail=False)
    def multiple_delete(self, request, *args, **kwargs):
        delete_ids = request.data.get('ids')
        try:
            admin = RolesModel.objects.get(name='admin')
            if isinstance(delete_ids, list):
                if admin.id in delete_ids:
                    return Response(data={'detail': 'admin角色不可删除'}, status=status.HTTP_400_BAD_REQUEST)

        except RolesModel.DoesNotExist as ex:
            pass
        return super().multiple_delete(request, *args, **kwargs)
