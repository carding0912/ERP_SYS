from django.db.models import Q
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from basic_info.models import SettlementAccountModel
from basic_info.serializer.settlement_account_serialzer import SettlementAccountSerializer
from msb_erp.utils.base_views import MultipleDestroyMixin, MultipleOpenMixin
from msb_erp.utils.pagination import GlobalPagination

re_name = openapi.Parameter(name='name', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                            description='结算账户名称搜索的关键字')
re_remark = openapi.Parameter(name='remark', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='结算账户描述搜索的关键字')
re_number_code = openapi.Parameter(name='number_code', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                                   description='结算账户编号搜索的关键字')


@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[re_name, re_remark, re_number_code]))
class SettlementAccountView(viewsets.ModelViewSet, MultipleDestroyMixin, MultipleOpenMixin):
    """ create:
    结算账户信息--新增

    结算账户信息新增, status: 201(成功), return: 新增结算账户信息信息
    destroy:
    结算账户信息--删除

    结算账户信息删除, status: 204(成功), return: None
    multiple_delete:
    结算账户信息--批量删除,必传参数：ids=[1,2,3,4...]

    结算账户信息批量删除, status: 204(成功), return: None
    multiple_open:
    结算账户信息--批量启用或者禁用,必传(json)参数：ids=[1,2,3,4...](列表中可以只有一个)，is_open=1/0 { "ids":[1,2], "is_open":"0" }
    is_open=1表示禁用，is_open=0表示启用，

    结算账户信息批量启用或者禁用, status: 204(成功), return: None
    update:
    结算账户信息--修改,

    结算账户信息修改, status: 200(成功), return: 修改后的结算账户信息
    partial_update:
    结算账户信息--局部修改,可以传参任意属性的值，服务器会修改指定的属性值

    结算账户信息局部修改, status: 200(成功), return: 修改后的结算账户信息
    list:
    结算账户信息--获取分页列表，可选json参数:name(名称)，mobile(手机号码)，phone(联系电话)

    结算账户信息列表信息, status: 200(成功), return: 结算账户信息列表
    retrieve:
    查询某一个结算账户信息

    查询指定ID的结算账户信息, status: 200(成功), return: 用户结算账户信息
    """
    queryset = SettlementAccountModel.objects.all()
    serializer_class = SettlementAccountSerializer
    pagination_class = GlobalPagination

    def get_queryset(self):
        if self.action == 'list':
            # name = self.request.data.get('name',None)
            # phone = self.request.data.get('phone',None)
            # mobile = self.request.data.get('mobile',None)
            name = self.request.query_params.get('name', None)
            remark = self.request.query_params.get('remark', None)
            number_code = self.request.query_params.get('number_code', None)
            query = Q()
            if name:
                query.add(Q(name__contains=name), 'AND')
            if remark:
                query.add(Q(remark__contains=remark), 'AND')
            if number_code:
                query.add(Q(number_code__contains=number_code), 'AND')
            return SettlementAccountModel.objects.filter(query)
        else:
            return self.queryset
