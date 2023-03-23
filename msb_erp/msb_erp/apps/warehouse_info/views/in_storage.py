import logging

from django.db import transaction
from django.db.models import Q, F, Sum
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from basic_info.models import SupplierModel
from erp_system.models import UserModel
from goods_info.models import GoodsInventoryModel
from msb_erp.utils.base_views import MultipleDestroyMixin, MultipleAuditMixin
from warehouse_info.models import PurchaseStorageModel
from warehouse_info.serializer.instorage_serializer import InStorageSerializer, InStorageGetSerializer

logger = logging.getLogger('erp')


class InStorageView(viewsets.ModelViewSet, MultipleDestroyMixin, MultipleAuditMixin):
    """
    create:
    仓库(采购)入库单--新增,注意：其中images_list="1,2,3,4";里面是附件的ID
    
    仓库(采购)入库单新增, status: 201(成功), return: 新增仓库(采购)入库单信息
    
    destroy:
    仓库(采购)入库单--删除
    
    仓库(采购)入库单删除, status: 204(成功), return: None
    
    multiple_delete:
    仓库(采购)入库单--批量删除,必传参数：ids=[1,2,3,4...]
    
    仓库(采购)入库单批量删除, status: 204(成功), return: None
    
    multiple_open:
    仓库(采购)入库单--批量启用或者禁用,必传(json)参数：ids=[1,2,3,4...](列表中可以只有一个)，is_open=1/0
    
    {
    "ids":[1,2],
    "is_open":"0"
    }
    is_open=1表示禁用，is_open=0表示启用，
    仓库(采购)入库单批量启用或者禁用, status: 204(成功), return: None
    
    update:
    仓库(采购)入库单--修改,注意：其中images_list="1,2,3,4";里面是附件的ID
    
    仓库(采购)入库单修改, status: 200(成功), return: 修改后的仓库(采购)入库单信息
    
    partial_update:
    仓库(采购)入库单--局部修改,可以传参任意属性的值，服务器会修改指定的属性值
    
    仓库(采购)入库单局部修改, status: 200(成功), return: 修改后的仓库(采购)入库单信息
    
    list:
    仓库(采购)入库单
    
    仓库(采购)入库单列表信息, status: 200(成功), return: 仓库(采购)入库单信息列表
    
    retrieve:
    查询某一个仓库(采购)入库单
    
    查询指定ID的仓库(采购)入库单, status: 200(成功), return: 用户仓库(采购)入库单
    
    find:
    关键字及其它过滤查寻
    
    根据指定条件返回的仓库(采购)入库单, status: 200(成功), return: 用户仓库(采购)入库单
    multiple_audit:
    批量审核 [ids1,ids2...],is_status=false 反审核  is_status=ture 审核
    
    批量审核反审核订单
    """
    queryset = PurchaseStorageModel.objects.all()
    serializer_class = InStorageSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return InStorageGetSerializer
        return self.serializer_class

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
            warehouse = self.request.data.get('warehouse', 0)
            account = self.request.data.get('account', 0)
            purchase_number_code = self.request.data.get('purchase_number_code', None)
            query = Q()
            if keyword:
                child_query = Q()
                child_query.add(Q(item_list__name__contains=keyword), 'OR')
                child_query.add(Q(item_list__specification=keyword), 'OR')
                query.add(child_query, 'AND')
            if warehouse:
                query.add(Q(item_list__warehouse=warehouse), 'AND')
            if account:
                query.add(Q(account__id=account), "AND")
            if purchase_number_code:
                query.add(Q(purchase_number_code__contains=purchase_number_code), "AND")
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

            return PurchaseStorageModel.objects.filter(query).distinct().all()
        else:
            return self.queryset

    params = openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'keyword': openapi.Schema(type=openapi.TYPE_STRING, description="名称的关键字或者型号"),
        'start_date': openapi.Schema(type=openapi.TYPE_STRING, description="起始日期2020-10-01"),
        'number_code': openapi.Schema(type=openapi.TYPE_STRING, description="编号(序列号)"),
        'end_date': openapi.Schema(type=openapi.TYPE_STRING, description="结束日期2020-10-01"),
        'status': openapi.Schema(type=openapi.TYPE_STRING, description="状态0或者1,2,3.."),
        'supplier': openapi.Schema(type=openapi.TYPE_INTEGER, description="供应商的ID"),
        'operator_user': openapi.Schema(type=openapi.TYPE_INTEGER, description="操作用户的ID"),
        'warehouse': openapi.Schema(type=openapi.TYPE_INTEGER, description="仓库的ID"),
        'account': openapi.Schema(type=openapi.TYPE_INTEGER, description="结算账户的ID"),
        'purchase_number_code': openapi.Schema(type=openapi.TYPE_STRING, description="货品编号"),
    })
    # 分页参数必须是query_param(看源码)
    page_param = openapi.Parameter(name='page', in_=openapi.IN_QUERY, description="页号",
                                   type=openapi.TYPE_INTEGER)
    size_param = openapi.Parameter(name='size', in_=openapi.IN_QUERY, description="每页显示数量",
                                   type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(method='POST', request_body=params, manual_parameters=[page_param, size_param],
                         operation_description="入库单的搜索过滤")
    @action(methods=['POST'], detail=False)
    def find(self, request, *args, **kwargs):
        return super().list(request=request, *args, **kwargs)

    body_json = openapi.Schema(type=openapi.TYPE_OBJECT, required=['ids'], properties={
        'ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
        'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='用户的ID')
    })

    @swagger_auto_schema(method='put', request_body=body_json)
    @action(methods=['put'], detail=False)
    @transaction.atomic()  # 自动数据库事务装饰器
    def multiple_audit(self, request, *args, **kwargs):
        audit_ids = request.data.get('ids')
        user_id = request.data.get('user_id')
        is_audit = '1'  # 只能是审核
        if not audit_ids:
            return Response(data={'detail': '参数错误,ids为必传参数'}, status=status.HTTP_400_BAD_REQUEST)
        elif not isinstance(audit_ids, list):
            return Response(data={'detail': 'ids格式错误,必须为List'}, status=status.HTTP_400_BAD_REQUEST)

        # 首先删除传递过来的菜单
        in_list = self.get_queryset().filter(id__in=audit_ids).all()
        check_user = UserModel.objects.get(id=int(user_id))  # 审批人
        for in_storage in in_list:
            # 审批的条件判断:1 入库单的状态必须是0
            if in_storage.status != '0':
                return Response(data={'detail': '不能审核,因为入库已审核'}, status=status.HTTP_400_BAD_REQUEST)
            if in_storage.purchase:  # 如果该入库单有关联的采购订单
                # 首先检查对应的采购订单的状态
                if not any([in_storage.purchase.status == '1', in_storage.purchase.status == '5',
                            in_storage.purchase.status == '2']):
                    return Response(data={'detail': '不能审核,因为关联的采购订单状态不支持审核操作'},
                                    status=status.HTTP_400_BAD_REQUEST)
                # 业务处理逻辑 修改关联的采购订单, 状态为:部分入库或者全部入库
                in_count = PurchaseStorageModel.objects.filter(purchase_id=in_storage.purchase_id).exclude(
                    status='0').aggregate(sum=Sum('number_count'))  # 查询该采购单,已经入库的数量
                if not in_count.get('sum', 0):
                    in_count = 0
                if in_count + in_storage.number_count == in_storage.purchase.number_count:  # 已入库数量加本次入库等于采购总数
                    in_storage.purchase.status = '3'  # 修改订单状态为3:全部入库
                elif in_count + in_storage.number_count <= in_storage.purchase.number_count:
                    in_storage.purchase.status = '2'  # 已入库数量加本次入库小于采购总数,修改订单状态为 2:部分入库
                else:
                    return Response(data={'detail': '入库单的入库数量有误'}, status=status.HTTP_400_BAD_REQUEST)
                in_storage.purchase.save()
            # 相关的货品的库存,需要增加:原来的库存 += 当前入库数量
            for item in in_storage.item_list.all():
                GoodsInventoryModel.objects.filter(goods_id=item.goods, warehouse_id=item.warehouse_id).update(
                    cur_inventory=F('cur_inventory') + item.purchase_count)

            if in_storage.supplier and in_storage.this_debt > 0:  # 修改供应商的期末应负+=本次欠款
                SupplierModel.objects.filter(id=in_storage.supplier_id).update(
                    current_pay=F('current_pay') + in_storage.this_debt)

        self.get_queryset().filter(id__in=audit_ids).update(status=is_audit, check_user_id=check_user.id,
                                                            check_user_name=check_user.real_name)
        return Response(status=status.HTTP_200_OK)
