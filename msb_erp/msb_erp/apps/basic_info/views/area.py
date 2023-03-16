import logging

from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from basic_info.models import Nation, Province, City
from basic_info.serializer.area_serializer import NationSerializer, ProvinceSerializer, CitySerializer
from msb_erp.utils.base_views import MultipleDestroyMixin
from msb_erp.utils.pagination import GlobalPagination

logger = logging.getLogger('erp')


class NationsView(viewsets.ModelViewSet, MultipleDestroyMixin):
    """
    create:
    国家--新增

    国家新增, status: 201(成功), return: 新增国家信息
    destroy:
    国家--删除

    国家删除, status: 204(成功), return: None
    multiple_delete:
    国家--批量删除,必传参数：ids=[1,2,3,4...]

    国家批量删除, status: 204(成功), return: None
    update:
    国家--修改,只是修改国家名字。

    国家修改, status: 200(成功), return: 修改后的国家信息
    partial_update:
    国家--局部修改,只是修改国家名字。

    国家局部修改, status: 200(成功), return: 修改后的国家信息
    list:
    国家--获取列表

    国家列表信息, status: 200(成功), return: 国家信息列表
    retrieve:
    查询某一个国家

    查询指定ID的国家, status: 200(成功), return: 用户国家
    """

    queryset = Nation.objects.all()
    serializer_class = NationSerializer
    pagination_class = GlobalPagination


query_param = openapi.Parameter(name='nid', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)


@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[query_param]))
class ProvincesView(viewsets.ModelViewSet, MultipleDestroyMixin):
    """
    create:
    省份--新增

    省份新增, status: 201(成功), return: 新增省份信息
    destroy:
    省份--删除

    省份删除, status: 204(成功), return: None
    multiple_delete:
    省份--批量删除,必传参数：ids=[1,2,3,4...]

    省份批量删除, status: 204(成功), return: None
    update:
    省份--修改,只是修改省份名字。

    省份修改, status: 200(成功), return: 修改后的省份信息
    partial_update:
    省份--局部修改,只是修改省份名字。

    省份局部修改, status: 200(成功), return: 修改后的省份信息
    list:
    省份--获取列表，

    请求参数为nid(国家ID), 没有传参数：表示所有省份列表。有nid表示查询该国家的省份列表 省份列表信息, status: 200(成功), return: 省份信息列表
    retrieve:
    查询某一个省份

    查询指定ID的省份, status: 200(成功), return: 用户省份
    """

    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    pagination_class = GlobalPagination

    def get_queryset(self):
        # 请求参数为nid(国家ID), 没有传参数：表示所有省份列表。有nid表示查询该国家的省份列表
        nid = self.request.query_params.get('nid', None)
        if nid:
            nid = int(nid)
            return Province.objects.filter(nation__id=nid).all()
        else:
            return Province.objects.all()

query_param = openapi.Parameter(name='pid', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[query_param]))
class CitiesView(viewsets.ModelViewSet, MultipleDestroyMixin):
    """
    create:
    城市--新增

    城市新增, status: 201(成功), return: 新增城市信息
    destroy:
    城市--删除

    城市删除, status: 204(成功), return: None
    multiple_delete:
    城市--批量删除,必传参数：ids=[1,2,3,4...]

    城市批量删除, status: 204(成功), return: None
    update:
    城市--修改,只是修改城市名字。

    城市修改, status: 200(成功), return: 修改后的城市信息
    partial_update:
    城市--局部修改,只是修改城市名字。

    城市局部修改, status: 200(成功), return: 修改后的城市信息
    list:
    城市--获取列表，

    请求参数为pid(省份ID), 没有传参数：表示所有城市列表。有pid表示查询该省份的城市列表 城市列表信息, status: 200(成功), return: 城市信息列表
    retrieve:
    查询某一个城市

    查询指定ID的城市, status: 200(成功), return: 用户城市
    """

    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = GlobalPagination

    def get_queryset(self):
        # 参数为pid(省份ID), 没有传参数：表示所有城市列表。有pid表示查询该省份的城市列表
        pid = self.request.query_params.get('pid', None)
        if pid:
            pid = int(pid)
            return City.objects.filter(province__id=pid).all()
        else:
            return City.objects.all()
