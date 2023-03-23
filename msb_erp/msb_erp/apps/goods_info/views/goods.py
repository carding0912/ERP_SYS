import logging

from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from goods_info.models import GoodsModel
from goods_info.serializer.goods_serializer import GoodsBaseSerializer, GoodsGetSerializer
from msb_erp.utils.base_views import MultipleDestroyMixin, MultipleOpenMixin
from msb_erp.utils.pagination import GlobalPagination

logger = logging.getLogger('erp')


class GoodsView(viewsets.ModelViewSet, MultipleDestroyMixin, MultipleOpenMixin):
    """
    create:
    货品(商品)信息--新增,注意：其中images_list="1,2,3,4";里面是附件的ID

    货品(商品)信息新增, status: 201(成功), return: 新增货品(商品)信息信息

    destroy:
    货品(商品)信息--删除

    货品(商品)信息删除, status: 204(成功), return: None

    multiple_delete:
    货品(商品)信息--批量删除,必传参数：ids=[1,2,3,4...]

    货品(商品)信息批量删除, status: 204(成功), return: None

    multiple_open:
    货品(商品)信息--批量启用或者禁用,必传(json)参数：ids=[1,2,3,4...](列表中可以只有一个)，is_open=1/0

    {
        "ids":[1,2],
        "is_open":"0"
    }
    is_open=1表示禁用，is_open=0表示启用，
    货品(商品)信息批量启用或者禁用, status: 204(成功), return: None

    update:
    货品(商品)信息--修改,注意：其中images_list="1,2,3,4";里面是附件的ID

    货品(商品)信息修改, status: 200(成功), return: 修改后的货品(商品)信息信息

    partial_update:
    货品(商品)信息--局部修改,可以传参任意属性的值，服务器会修改指定的属性值

    货品(商品)信息局部修改, status: 200(成功), return: 修改后的货品(商品)信息信息

    list:
    货品(商品)信息--该接口可以弃用

    货品(商品)信息列表信息, status: 200(成功), return: 货品(商品)信息信息列表

    retrieve:
    查询某一个货品(商品)信息

    查询指定ID的货品(商品)信息, status: 200(成功), return: 用户货品(商品)信息

    find:
    关键字及其它过滤查寻

    根据指定条件返回的货品(商品)信息, status: 200(成功), return: 用户货品(商品)信息
    """

    queryset = GoodsModel.objects.all()
    serializer_class = GoodsBaseSerializer
    pagination_class = GlobalPagination

    def get_queryset(self):
        if self.action == 'find':  # 过滤查询
            # 获取请求参数(在json中)：
            keyword = self.request.data.get('keyword', None)
            color = self.request.data.get('color', None)
            category = self.request.data.get('category', 0)
            number_code = self.request.data.get('number_code', None)
            basic_weight = self.request.data.get('basic_weight', None)
            expiration_day = self.request.data.get('expiration_day', 0)
            delete_flag = self.request.data.get('delete_flag', None)
            query = Q()
            if keyword:
                child_query = Q()
                child_query.add(Q(name__contains=keyword), 'OR')
                child_query.add(Q(specification__contains=keyword), 'OR')
                child_query.add(Q(model_number__contains=keyword), 'OR')
                query.add(child_query, 'AND')
            if color:
                query.add(Q(color=color), 'AND')
            if category:
                query.add(Q(category__id=category), 'AND')
            if number_code:
                query.add(Q(number_code__contains=number_code), 'AND')
            if basic_weight:
                query.add(Q(basic_weight=basic_weight), 'AND')
            if expiration_day:
                query.add(Q(expiration_day=expiration_day), 'AND')
            if delete_flag:
                query.add(Q(delete_flag=delete_flag), 'AND')
            return GoodsModel.objects.filter(query).all()
        else:
            return GoodsModel.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'find':
            return GoodsGetSerializer
        return GoodsBaseSerializer

    params = openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'keyword': openapi.Schema(type=openapi.TYPE_STRING, description="名称的关键字或者规格和型号"),
        'color': openapi.Schema(type=openapi.TYPE_STRING, description="颜色"),
        'number_code': openapi.Schema(type=openapi.TYPE_STRING, description="批号(序列号)"),
        'basic_weight': openapi.Schema(type=openapi.TYPE_STRING, description="基础质量"),
        'delete_flag': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="状态0或者1"),
        'category': openapi.Schema(type=openapi.TYPE_INTEGER, description="类别的ID"),
        'expiration_day': openapi.Schema(type=openapi.TYPE_INTEGER, description="保质期天数"),
    })
    # 分页参数必须是query_param(看源码)
    page_param = openapi.Parameter(name='page', in_=openapi.IN_QUERY, description="页号", type=openapi.TYPE_INTEGER)
    size_param = openapi.Parameter(name='size', in_=openapi.IN_QUERY, description="每页显示数量", type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(method='POST', request_body=params, manual_parameters=[page_param, size_param])
    @action(methods=['POST'], detail=False)
    def find(self, request, *args, **kwargs):
        return super(GoodsView, self).list(request=request, *args, **kwargs)
