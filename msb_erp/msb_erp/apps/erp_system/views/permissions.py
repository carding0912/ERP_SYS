import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from erp_system.models import PermissionsModel, RolesModel
from msb_erp.utils.base_views import MultipleDestroyMixin
from erp_system.serializer.permissions_serializer import PermissionsSerializer

logger = logging.getLogger('erp')


class PermissionsView(viewsets.ModelViewSet, MultipleDestroyMixin):
    """
    create:
    权限-新增

    权限新增,status:201(成功),return:新增权限信息
    destroy:
    权限--删除 单个权限

    权限删除,status:204(成功),return:None
    multiple_delete:
    批量删除多个权限

    权限批量删除,status:204(成功),return:None
    update:
    权限--修改,权限本身的信息(属性)

    权限修改,status:200(成功),return:修改的权限信息
    partial_update:
    局部修改权限,权限本身的信息(属性)

    权限局部修改,status:200(成功),return:修改的权限信息
    list:
    查询所有权限

    获取所有的权限
    find_permissions_by_menu:
    查询属于指定菜单或者接口的权限列表

    需要传参:menu_id 例:/find_permissions_by_menu/?menu_id=2 返回权限列表,status:200(成功),return:返回权限列表
    find_permissions:
    获取单个pid角色所对应的所有权限列表和整个项目的所有权限(树型)列表,必传参数:pid(t_roles表中的角色对应ID)

    返回权限列表,status:200(成功),return:返回权限列表
    retrieve:
    查询某一个指定id的权限信息

    返回对应的id的权限信息
    """
    queryset = PermissionsModel.objects.all()
    serializer_class = PermissionsSerializer

    menu_id_set = openapi.Parameter(name='menu_id', in_=openapi.IN_QUERY,type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(method='get', manual_parameters=[menu_id_set])
    @action(methods=['get'], detail=False)
    def find_permissions_by_menu(self, request, *args, **kwargs):
        menu_id = request.query_params.get('menu_id')
        permission_list = PermissionsModel.objects.filter(menu__id=menu_id).all()
        ser = PermissionsSerializer(instance=permission_list, many=True)
        return Response(ser.data)

    rid_set = openapi.Parameter(name='rid', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(method='get', manual_parameters=[rid_set])
    @action(methods=['get'], detail=False)
    def find_permissions(self, request, *args, **kwargs):
        result = {}  # 返回值,字典
        # 返回当前角色的所有已经拥有的权限ID列表,以及整个系统中所有的权限(树型)数据
        rid = request.query_params.get('rid', None)
        if rid:
            ids = RolesModel.objects.filter(id=rid).values_list('permissions', flat=True).distinct()
            result['ids'] = ids  # 把已经授权的id列表存入返回的字典中 格式:result = {ids:[id1(权限1),id2(权限2),...]}
        # 查询整个系统中,所有的权限列表
        permission_list = PermissionsModel.objects.values('id', 'name', 'menu__name', 'menu_id', 'menu__parent_id')
        tree_dict = {}  # 表示一个父节点
        tree_data = []  # 表示整个权限的树形数据

        for item in permission_list:
            tree_dict[item['menu_id']] = item  # 形成tree_dict字典中的每个元素 格式 menu_id : {id:?,name:?,menu_name:?,...}
        for i in tree_dict:  # i的格式为字典中的元素: menu_id : {id:?,name:?,menu_name:?,...}
            if tree_dict[i]['menu__parent_id']:  # 如果i是子菜单
                pid = tree_dict[i]['menu__parent_id']  # 找到i对应的父菜单id
                parent = tree_dict[pid]
                # 找到父菜单对应的字典 parent格式为:{id:?,name:?,menu_name:?,menu_id,:?,'menu__parent_id':None}
                child = dict()
                child['menu_id'] = tree_dict[i]['menu_id']
                child['menu__name'] = tree_dict[i]['menu__name']
                child.setdefault('permissions', [])
                parent.setdefault('children', []).append(child)
                # 重新形成了只有子菜单的组成的字典,即去掉了所有tree_dict中的父菜单元素

            else:  # 如果i是父菜单
                print(tree_dict[i])
                tree_data.append(tree_dict[i])
                # tree_dict[i]的格式是 menu_id:{id:?,name:?,menu_name:?,menu_id:?,'menu__parent_id':None}
        # print(tree_data)
        for parent in tree_data:
            print(parent)
            if 'children' in parent:
                for child in parent['children']:
                    # 得到child(二级)
                    for node in permission_list:
                        if node['menu__parent_id'] and node['menu_id'] == child['menu_id']:
                            child['permissions'].append(node)

        result['tree_data'] = tree_data
        return Response(result)
