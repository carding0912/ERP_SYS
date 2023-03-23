from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from msb_erp.utils.base_views import MultipleDestroyMixin, MultipleAuditMixin
from msb_erp.utils.pagination import GlobalPagination
from purchase_info.models import PurchaseModel
from purchase_info.serializer.purchase_serializer import PurchaseSerializer, PurchaseGetSerializer


class PurchaseView(viewsets.ModelViewSet, MultipleDestroyMixin, MultipleAuditMixin):
    """
    create:
    采购订单信息--新增,注意：其中images_list="1,2,3,4";里面是附件的ID

    采购订单信息新增, status: 201(成功), return: 新增采购订单信息信息

    destroy:
    采购订单信息--删除

    采购订单信息删除, status: 204(成功), return: None

    multiple_delete:
    采购订单信息--批量删除,必传参数：ids=[1,2,3,4...]

    采购订单信息批量删除, status: 204(成功), return: None

    multiple_open:
    采购订单信息--批量启用或者禁用,必传(json)参数：ids=[1,2,3,4...](列表中可以只有一个)，is_open=1/0

    {
        "ids":[1,2],
        "is_open":"0"
    }
    is_open=1表示禁用，is_open=0表示启用，
    采购订单信息批量启用或者禁用, status: 204(成功), return: None

    update:
    采购订单信息--修改,注意：其中images_list="1,2,3,4";里面是附件的ID

    采购订单信息修改, status: 200(成功), return: 修改后的采购订单信息信息

    partial_update:
    采购订单信息--局部修改,可以传参任意属性的值，服务器会修改指定的属性值

    采购订单信息局部修改, status: 200(成功), return: 修改后的采购订单信息信息

    list:
    采购订单信息

    采购订单信息列表信息, status: 200(成功), return: 采购订单信息信息列表

    retrieve:
    查询某一个采购订单信息

    查询指定ID的采购订单信息, status: 200(成功), return: 用户采购订单信息

    find:
    关键字及其它过滤查寻

    根据指定条件返回的采购订单信息, status: 200(成功), return: 用户采购订单信息
    multiple_audit:
    批量审核 [ids1,ids2...],is_status=false 反审核  is_status=ture 审核

    批量审核反审核订单
    """
    serializer_class = PurchaseSerializer
    queryset = PurchaseModel.objects.all()
    pagination_class = GlobalPagination

    def get_queryset(self):
        if self.action == 'find':  # 过滤查询
            # 获取请求参数(在json中)：
            number_code = self.request.data.get('number_code', None)
            keyword = self.request.data.get('keyword', None)
            start_date = self.request.data.get('start_date', None)
            end_date = self.request.data.get('start_date', None)
            supplier = self.request.data.get('supplier', 0)
            operator_user = self.request.data.get('operator_user', 0)
            status = self.request.data.get('status', None)
            remark = self.request.data.get('remark', None)
            query = Q()
            if keyword:
                child_query = Q()
                child_query.add(Q(item_list__name__contains=keyword), 'OR')
                child_query.add(Q(item_list__specification=keyword), 'OR')
                query.add(child_query, 'AND')
            if start_date:
                query.add(Q(invoices_date__gt=start_date), 'AND')
            if end_date:
                query.add(Q(invoices_date__lt=end_date), 'AND')
            if supplier:
                query.add(Q(supplier__id=supplier), 'AND')
            if number_code:
                query.add(Q(number_code__contains=number_code), 'AND')
            if operator_user:
                query.add(Q(operator_user__id=operator_user), 'AND')
            if status:
                query.add(Q(status=status), 'AND')
            if remark:
                query.add(Q(remark__contains=remark), 'AND')

            return PurchaseModel.objects.filter(query).distinct().all()
        else:
            return PurchaseModel.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PurchaseGetSerializer
        return PurchaseSerializer

    params = openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'keyword': openapi.Schema(type=openapi.TYPE_STRING, description="名称的关键字或者型号"),
        'start_date': openapi.Schema(type=openapi.TYPE_STRING, description="起始日期2020-10-01"),
        'remark': openapi.Schema(type=openapi.TYPE_STRING, description="采购订单的描述关键字"),
        'number_code': openapi.Schema(type=openapi.TYPE_STRING, description="编号(序列号)"),
        'end_date': openapi.Schema(type=openapi.TYPE_STRING, description="结束日期2020-10-01"),
        'status': openapi.Schema(type=openapi.TYPE_STRING, description="状态0或者1,2,3.."),
        'supplier': openapi.Schema(type=openapi.TYPE_INTEGER, description="供应商的ID"),
        'operator_user': openapi.Schema(type=openapi.TYPE_INTEGER, description="操作用户的ID"),
    })
    # 分页参数必须是query_param(看源码)
    page_param = openapi.Parameter(name='page', in_=openapi.IN_QUERY, description="页号",
                                   type=openapi.TYPE_INTEGER)
    size_param = openapi.Parameter(name='size', in_=openapi.IN_QUERY, description="每页显示数量",
                                   type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(method='POST', request_body=params, manual_parameters=[page_param, size_param],
                         operation_description="采购订单的搜索过滤")
    @action(methods=['POST'], detail=False)
    def find(self, request, *args, **kwargs):
        return super(PurchaseView, self).list(request=request, *args, **kwargs)
