from django.db.models import Q
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from basic_info.models import CustomerModel
from basic_info.serializer.customer_serialzer import CustomerSerializer
from msb_erp.utils.base_views import MultipleDestroyMixin,MultipleOpenMixin
from msb_erp.utils.pagination import GlobalPagination

re_name = openapi.Parameter(name='name', in_=openapi.IN_QUERY,type=openapi.TYPE_STRING,description='名字搜索的关键字')
re_phone = openapi.Parameter(name='phone', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,description='电话搜索的关键字')
re_mobile = openapi.Parameter(name='mobile', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,description='手机搜索的关键字')
@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[re_name,re_phone,re_mobile]))
class CustomerView(viewsets.ModelViewSet,MultipleDestroyMixin,MultipleOpenMixin):
    """ create:
    客户信息--新增

    客户信息新增, status: 201(成功), return: 新增客户信息信息
    destroy:
    客户信息--删除

    客户信息删除, status: 204(成功), return: None
    multiple_delete:
    客户信息--批量删除,必传参数：ids=[1,2,3,4...]

    客户信息批量删除, status: 204(成功), return: None
    multiple_open:
    客户信息--批量启用或者禁用,必传(json)参数：ids=[1,2,3,4...](列表中可以只有一个)，is_open=1/0 { "ids":[1,2], "is_open":"0" }
    is_open=1表示禁用，is_open=0表示启用，

    客户信息批量启用或者禁用, status: 204(成功), return: None
    update:
    客户信息--修改,

    客户信息修改, status: 200(成功), return: 修改后的客户信息
    partial_update:
    客户信息--局部修改,可以传参任意属性的值，服务器会修改指定的属性值

    客户信息局部修改, status: 200(成功), return: 修改后的客户信息
    list:
    客户信息--获取分页列表，可选json参数:name(名称)，mobile(手机号码)，phone(联系电话)

    客户信息列表信息, status: 200(成功), return: 客户信息列表
    retrieve:
    查询某一个客户信息

    查询指定ID的客户信息, status: 200(成功), return: 用户客户信息
    """
    queryset = CustomerModel.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = GlobalPagination

    def get_queryset(self):
        if self.action == 'list':
            # name = self.request.data.get('name',None)
            # phone = self.request.data.get('phone',None)
            # mobile = self.request.data.get('mobile',None)
            name = self.request.query_params.get('name',None)
            phone = self.request.query_params.get('phone',None)
            mobile = self.request.query_params.get('mobile',None)
            query = Q()
            if name:
                query.add(Q(name__contains=name),'AND')
            if phone:
                query.add(Q(phone__contains=phone),'AND')
            if mobile:
                query.add(Q(mobile__contains=mobile),'AND')
            return CustomerModel.objects.filter(query)
        else:
            return self.queryset
