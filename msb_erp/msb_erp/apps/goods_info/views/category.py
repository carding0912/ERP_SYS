from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet

from goods_info.models import GoodsCategoryModel
from goods_info.serializer.goodscategory_serializer import CategorySerializer, CategoryListSerializer
from msb_erp.utils.base_views import MultipleDestroyMixin

param_pid = openapi.Parameter(name='pid', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='要搜索商品ID')


@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[param_pid]))
class CategoryView(ModelViewSet, MultipleDestroyMixin):
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
    货品(商品)信息--批量启用或者禁用,必传(json)参数：ids=[1,2,3,4...](列表中可以只有一个)，is_open=1/0 { "ids":[1,2], "is_open":"0" } is_open=1表示禁用，is_open=0表示启用，

    货品(商品)信息批量启用或者禁用, status: 204(成功), return: None
    update:
    货品(商品)信息--修改,注意：其中images_list="1,2,3,4";里面是附件的ID

    货品(商品)信息修改, status: 200(成功), return: 修改后的货品(商品)信息信息
    partial_update:
    货品(商品)信息--局部修改,可以传参任意属性的值，服务器会修改指定的属性值

    货品(商品)信息局部修改, status: 200(成功), return: 修改后的货品(商品)信息信息
    list:
    货品(商品)信息-- pid可选传参： pid=0 表示查询父子信息的树型结构，不传参表示查询所有货口信息，传参表示查询该父货品下面的子货品信息

    货品(商品)信息列表信息, status: 200(成功), return: 货品(商品)信息信息列表
    retrieve:
    查询某一个货品(商品)信息

    查询指定ID的货品(商品)信息, status: 200(成功), return: 用户货品(商品)信息
    """

    queryset = GoodsCategoryModel.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_class(self):
        if self.action == 'list':
            pid = self.request.query_params.get('pid', None)
            if pid:
                if int(pid) == 0:
                    return CategoryListSerializer
                else:
                    return CategorySerializer
            else:
                return CategorySerializer
        else:
            return CategorySerializer

    def get_queryset(self):
        if self.action == 'list':
            pid = self.request.query_params.get('pid', None)
            if pid:
                pid = int(pid)
                if pid == 0:
                    return GoodsCategoryModel.objects.filter(parent__isnull=True)
                else:
                    return GoodsCategoryModel.objects.filter(parent__id=pid)
            else:
                return self.queryset
        else:
            return self.queryset
