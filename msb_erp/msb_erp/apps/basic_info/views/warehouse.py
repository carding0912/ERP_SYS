from django.db.models import Q
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from basic_info.models import WarehouseModel
from basic_info.serializer.warehouse_serialzer import WarehouseSerializer, WarehouseSearchSerializer
from msb_erp.utils.base_views import MultipleDestroyMixin,MultipleOpenMixin
from msb_erp.utils.pagination import GlobalPagination

re_name = openapi.Parameter(name='name', in_=openapi.IN_QUERY,type=openapi.TYPE_STRING,description='名字搜索的关键字')
re_remark = openapi.Parameter(name='re_remark', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,description='备注搜索的关键字')
@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[re_name,re_remark]))
class WarehouseView(viewsets.ModelViewSet,MultipleDestroyMixin,MultipleOpenMixin):
    """ create:
    仓库信息--新增

    仓库信息新增, status: 201(成功), return: 新增仓库信息信息
    destroy:
    仓库信息--删除

    仓库信息删除, status: 204(成功), return: None
    multiple_delete:
    仓库信息--批量删除,必传参数：ids=[1,2,3,4...]

    仓库信息批量删除, status: 204(成功), return: None
    multiple_open:
    仓库信息--批量启用或者禁用,必传(json)参数：ids=[1,2,3,4...](列表中可以只有一个)，is_open=1/0 { "ids":[1,2], "is_open":"0" }
    is_open=1表示禁用，is_open=0表示启用，

    仓库信息批量启用或者禁用, status: 204(成功), return: None
    update:
    仓库信息--修改,

    仓库信息修改, status: 200(成功), return: 修改后的仓库信息
    partial_update:
    仓库信息--局部修改,可以传参任意属性的值，服务器会修改指定的属性值

    仓库信息局部修改, status: 200(成功), return: 修改后的仓库信息
    list:
    仓库信息--获取分页列表，可选json参数:name(名称)，re_remark(备注)

    仓库信息列表信息, status: 200(成功), return: 仓库信息列表
    retrieve:
    查询某一个仓库信息

    查询指定ID的仓库信息, status: 200(成功), return: 用户仓库信息
    """
    queryset = WarehouseModel.objects.all()
    serializer_class = WarehouseSerializer
    pagination_class = GlobalPagination

    def get_serializer_class(self):
        if self.action == 'list' or self.action=='retrieve':
            return WarehouseSearchSerializer
        return self.serializer_class

    def get_queryset(self):
        if self.action == 'list':
            # name = self.request.data.get('name',None)
            # phone = self.request.data.get('phone',None)
            # mobile = self.request.data.get('mobile',None)
            name = self.request.query_params.get('name',None)
            remark = self.request.query_params.get('remark',None)
            query = Q()
            if name:
                query.add(Q(name__contains=name),'AND')
            if remark:
                query.add(Q(remark__contains=remark),'AND')
            return WarehouseModel.objects.filter(query)
        else:
            return self.queryset
