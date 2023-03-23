from django.db.models import OuterRef, Sum, Subquery, Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from erp_system.models import UserModel
from goods_info.models import GoodsInventoryModel, GoodsModel
from msb_erp.utils.base_serializer import ChoiceGoodsSerializer
from msb_erp.utils.cont import NumberPrefix
from msb_erp.utils.generate_code import generate_code
from msb_erp.utils.pagination import GlobalPagination


class MultipleDestroyMixin:
    del_ids = openapi.Schema(type=openapi.TYPE_OBJECT, required=['ids'], properties={
        'ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER))
    })

    @swagger_auto_schema(method='delete', request_body=del_ids)
    @action(methods=['delete'], detail=False)
    def multiple_delete(self, request, *args, **kwargs):
        delete_ids = request.data.get('ids')
        if not delete_ids:
            return Response(data={'detail': '参数错误,ids为必传参数'}, status=status.HTTP_400_BAD_REQUEST)
        elif not isinstance(delete_ids, list):
            return Response(data={'detail': 'ids格式错误,必须为List'}, status=status.HTTP_400_BAD_REQUEST)

        # 首先删除传递过来的菜单
        queryset = self.get_queryset()
        del_queryset = queryset.filter(id__in=delete_ids)
        if del_queryset.count() != len(delete_ids):
            return Response(data={'detail': '删除的数据不存在'}, status=status.HTTP_400_BAD_REQUEST)

        del_queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MultipleOpenMixin:
    del_ids = openapi.Schema(type=openapi.TYPE_OBJECT, required=['ids'], properties={
        'ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER),
                              description='选择要批量启用或禁用的ID'),
        "is_open": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                  description='是否启用,启用:Ture,禁用:False')
    })

    @swagger_auto_schema(method='delete', request_body=del_ids)
    @action(methods=['delete'], detail=False)
    def multiple_open(self, request, *args, **kwargs):
        delete_ids = request.data.get('ids')
        is_open = request.data.get('is_open', 0)
        if not delete_ids:
            return Response(data={'detail': '参数错误,ids为必传参数'}, status=status.HTTP_400_BAD_REQUEST)
        elif not isinstance(delete_ids, list):
            return Response(data={'detail': 'ids格式错误,必须为List'}, status=status.HTTP_400_BAD_REQUEST)

        # 首先删除传递过来的菜单
        queryset = self.get_queryset()
        del_queryset = queryset.filter(id__in=delete_ids)
        if del_queryset.count() != len(delete_ids):
            return Response(data={'detail': '数据不存在'}, status=status.HTTP_400_BAD_REQUEST)

        del_queryset.update(delete_flag=is_open)
        return Response(status=status.HTTP_200_OK)


class GenerateCode(views.APIView):
    prefix_parm = openapi.Parameter(name='prefix', in_=openapi.IN_QUERY, description='编号的前辍,可以参考cont.py',
                                    type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[prefix_parm])
    def get(self, request, *args, **kwargs):
        """
        自动生成各种编号(流水号)

        生成各种编号的接口，必须传一个前缀: /api/generate_code/prefix=ord，可以参考cont.py返回一个28位的编号字符串, return： code就是生成的编号
        """
        prefix = request.query_params.get('prefix', None)

        if prefix:
            if prefix.lower() in NumberPrefix.__members__:
                code = generate_code(NumberPrefix[prefix].value)
                return Response(data={'code': code}, status=status.HTTP_200_OK)
            else:
                return Response(data={'detail': 'prefix没有配置,请参考cont.py'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'detail': 'prefix没有,该参数必传,请参考cont.py'}, status=status.HTTP_400_BAD_REQUEST)

# 选择货品(商品)界面展示的列表内容
class ChoiceGoodsView(generics.GenericAPIView):
    serializer_class = ChoiceGoodsSerializer
    pagination_class = GlobalPagination

    # 分页参数必须是query_param(看源码)
    page_param = openapi.Parameter(name='page', in_=openapi.IN_QUERY, description="页号", type=openapi.TYPE_INTEGER)
    size_param = openapi.Parameter(name='size', in_=openapi.IN_QUERY, description="每页显示数量",
                                   type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(operation_description='搜索需要选择的货品列表', request_body=ChoiceGoodsSerializer,
                         manual_parameters=[page_param, size_param])
    def post(self, request, *args, **kwargs):
        ser = ChoiceGoodsSerializer(data=request.data)
        if ser.is_valid():
            warehouse_id = ser.validated_data.get('warehouse_id', 0)
            keyword = ser.validated_data.get('keyword', None)
            category_id = ser.validated_data.get('category_id', 0)
            number_code = ser.validated_data.get('number_code', None)
            query = Q()
            if warehouse_id:  # 查询指定仓库每个商品的库存数量
                inventory_list = GoodsInventoryModel.objects.filter(id=warehouse_id).filter(
                    goods_id=OuterRef('pk')).values(
                    'goods_id').annotate(total_sum=Sum('cur_inventory'))

            else:   #  查询每个仓库每个商品的库存数量
                inventory_list = GoodsInventoryModel.objects.filter(goods_id=OuterRef('pk')).values(
                    'goods_id').annotate(total_sum=Sum('cur_inventory'))

            if keyword:
                child_query = Q()
                child_query.add(Q(name__contains=keyword), 'OR')
                child_query.add(Q(specification=keyword), 'OR')
                child_query.add(Q(model_number=keyword), 'OR')
                query.add(child_query, 'AND')
            if category_id:
                query.add(Q(category__id=category_id), 'AND')
            if number_code:
                query.add(Q(number_code__contains=number_code), 'AND')

            result = GoodsModel.objects.filter(query).values('id', 'name', 'number_code', 'specification',
                                                             'model_number', 'color', 'units__basic_name',
                                                             'category__name', 'category_id').annotate(
                cur_inventory=Subquery(inventory_list.values('total_sum'))).all()
            pg_result = self.paginate_queryset(result)  # 加上分页
            # 借助序列化器把查询结果进行序列化
            result_ser = self.get_serializer(instance=pg_result, many=True)
            return self.get_paginated_response(result_ser.data)


class MultipleAuditMixin:
    """
    批量审核和反审核的视图含数
    """
    body_json = openapi.Schema(type=openapi.TYPE_OBJECT, required=['ids'], properties={
        'ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
        'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='用户的ID'),
        'is_audit': openapi.Schema(type=openapi.TYPE_STRING, description='是否审核,审核:1,反审核:0')
    })

    @swagger_auto_schema(method='put', request_body=body_json)
    @action(methods=['put'], detail=False)
    def multiple_audit(self, request, *args, **kwargs):
        audit_ids = request.data.get('ids')
        user_id = request.data.get('user_id')
        is_audit = request.data.get('is_audit')
        if not audit_ids:
            return Response(data={'detail': '参数错误,ids为必传参数'}, status=status.HTTP_400_BAD_REQUEST)
        elif not isinstance(audit_ids, list):
            return Response(data={'detail': 'ids格式错误,必须为List'}, status=status.HTTP_400_BAD_REQUEST)

        # 首先删除传递过来的菜单
        queryset = self.get_queryset()
        audit_queryset = queryset.filter(id__in=audit_ids)
        if audit_queryset.count() != len(audit_ids):
            return Response(data={'detail': '审核的数据不存在'}, status=status.HTTP_400_BAD_REQUEST)
        for item in audit_queryset.all():
            if item.status != '1' and is_audit == '0':  #订单状态为1以后的,是不可以返审核的
                return Response(data={'detail': '不能反审核,因为订单已经生效'}, status=status.HTTP_400_BAD_REQUEST)
            if item.status != '0' and is_audit == '1':  #订单状态不为0的,是不可以审核的
                return Response(data={'detail': '不能审核,因为订单已经生效'}, status=status.HTTP_400_BAD_REQUEST)
        if not user_id:
            return Response(data={'detail': '参数错误,user_id为必传参数'},status=status.HTTP_400_BAD_REQUEST)
        check_user = UserModel.objects.get(id=int(user_id))
        audit_queryset.update(status=is_audit,check_user_name=check_user.real_name,check_user_id=check_user.id)
        return Response(status=status.HTTP_200_OK)