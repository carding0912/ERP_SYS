import logging

from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from erp_system.models import DeptModel
from erp_system.serializer.dept_serializer import DeptSerializer
from msb_erp.utils.base_views import MultipleDestroyMixin
from msb_erp.utils.pagination import GlobalPagination

logger = logging.getLogger('erp')

"""
部门的视图类

1 新增
2 查询单个部门
3 查询所有部门
4 查询某个父部门下面的所有子部门列表
5 查询所有顶级部门列表
6 删除某一个部门
7 批量删除多个部门  传参:[x,y,z]
8 修改部门属性
"""

query_param = openapi.Parameter(name='pid', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[query_param]))
class DeptView(viewsets.ModelViewSet, MultipleDestroyMixin):
    """
   create:
   新增部门,

   参数: 部门,其中address,parent_id,create_time,update_time 不用传参,return:添加之后的对象

   retrieve:
   查询单个部门

   查询单个部门
   list:
   查询所有的部门

   如果参数中有Pid,则查询某一个父菜单列表,pid=0表示查询项目顶级菜单列表

   update:
    修改部门

    修改部门信息
   destroy:
    删除指定id的部门

    删除指定id的部门
   multiple_delete:
   批量删除部门

   参数: 传参要求是个id列表[id1,id2,id3,...]

   partial_update:
   局部修改部门,修改任意部门的属性

   局部修改部门,修改任意部门的属性
    """

    # permission_classes = [IsAuthenticated]

    queryset = DeptModel.objects.all()
    serializer_class = DeptSerializer
    pagination_class = GlobalPagination

    def get_queryset(self):
        pid = self.request.query_params.get('pid', None)
        if pid:
            pid = int(pid)
            if pid == 0:  # 查询所有父部门列表
                return DeptModel.objects.filter(parent__isnull=True).all()
            else:  # 查询某个父部门下面的所有子部门列表
                return DeptModel.objects.filter(parent__id=pid).all()
        else:
            return DeptModel.objects.all()
