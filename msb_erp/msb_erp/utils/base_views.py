from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.decorators import action
from rest_framework.response import Response

from msb_erp.utils.cont import NumberPrefix
from msb_erp.utils.generate_code import generate_code


class MultipleDestroyMixin:
    """
    定义批量删除的视图函数
    """
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
    """
    定义批量起用或禁用的视图函数
    """
    del_ids = openapi.Schema(type=openapi.TYPE_OBJECT, required=['ids'], properties={
        'ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER),
                              description='选择要批量启用或禁用的ID'),
        "is_open": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                  description='是否启用,启用:Ture,禁用:False')
    })

    @swagger_auto_schema(method='delete', request_body=del_ids, operation_description='批量启用或禁用')
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
    prefix_prarm = openapi.Parameter(name='prefix', in_=openapi.IN_QUERY, description='编号的前辍,可以参考cont.py',
                                     type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[prefix_prarm])
    def get(self, request, *args, **kwargs):
        """
        自动生成各种编号(流水号)

        生成各种编号的接口，必须传一个前缀: /api/generate_code/prefix=ord，可以参考cont.py返回一个28位的编号字符串, return： code就是生成的编号
        """
        prefix = request.query_params.get('prefix',None)

        if prefix:
            if prefix.lower() in NumberPrefix.__members__:
                code = generate_code(NumberPrefix[prefix].value)
                return Response(data={'code':code},status=status.HTTP_200_OK)
            else:
                return Response(data={'detail':'prefix没有配置,请参考cont.py'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'detail':'prefix没有,该参数必传,请参考cont.py'},status=status.HTTP_400_BAD_REQUEST)
