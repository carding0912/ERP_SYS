from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


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
