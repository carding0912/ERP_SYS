from django.db.models import Q
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet
from goods_info.models import UnitsModel
from goods_info.serializer.units_serializer import UnitsSerializer
from msb_erp.utils.base_views import MultipleDestroyMixin, MultipleOpenMixin

param_pid = openapi.Parameter(name='name', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='搜索计量单位名称关键字')


@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[param_pid]))
class UnitsView(ModelViewSet, MultipleDestroyMixin, MultipleOpenMixin):
    """
    create:
    计量单位信息--新增

    计量单位信息新增, status: 201(成功), return: 新增计量单位信息信息
    destroy:
    计量单位信息--删除

    计量单位信息删除, status: 204(成功), return: None
    multiple_delete:
    计量单位信息--批量删除,必传参数：ids=[1,2,3,4...]

    计量单位信息批量删除, status: 204(成功), return: None
    multiple_open:
    计量单位信息--批量启用或禁用,必传参数：ids=[1,2,3,4...] is_open=True 表示启用, is_open=False 表示禁用

    计量单位信息批量启用或禁用, status: 204(成功), return: None
    update:
    计量单位信息--修改

    计量单位信息修改, status: 200(成功), return: 修改后的计量单位信息信息
    partial_update:
    计量单位信息--局部修改,可以传参任意属性的值，服务器会修改指定的属性值

    计量单位信息局部修改, status: 200(成功), return: 修改后的计量单位信息信息
    list:
    计量单位信息列表 可传参,传参为搜索计量单位或副单位的名称的关键字

    计量单位信息列表信息, status: 200(成功), return: 计量单位信息信息列表
    retrieve:
    查询某一个计量单位信息

    查询指定ID的计量单位信息, status: 200(成功), return: 用户计量单位信息
    """

    queryset = UnitsModel.objects.all()
    serializer_class = UnitsSerializer

    def get_queryset(self):
        if self.action == 'list':
            keywords = self.request.query_params.get('name', None)
            query = Q()
            if keywords:
                query.add(Q(basic_name__contains=keywords), 'OR')
                query.add(Q(backup_name__contains=keywords), 'OR')
            return UnitsModel.objects.filter(query).all()
        else:
            return self.queryset
