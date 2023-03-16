from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.mixins import UpdateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from erp_system.models import UserModel
from msb_erp.apps.erp_system.serializer.user_serializer import UserRegisterSerializer, UserWriteOnlySerializer, \
    UserReadOnlySerializer, UserResetPasswordSerializer
from msb_erp.utils.base_views import MultipleDestroyMixin
from msb_erp.utils.pagination import GlobalPagination


class RegisterView(CreateAPIView):
    """
    create:
    用户的注册

    参数: username, password,(必须传递) phone real_name可选传递, 返回添加的对象
    """

    queryset = UserModel.objects.all()
    serializer_class = UserRegisterSerializer


class UsersView(ListModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericViewSet,
                MultipleDestroyMixin):
    """
    retrieve:
    单个用户查询端口

    查询单个用户的详细信息
    list:
    列表查询所有用户:

    查询所有的用户
    update:
    修改用户信息

    修改用户信息
    destroy:
    删除用户端口

    删除指定id的用户,一次只能删除一个
    partial_update:
    用户信息的局部修改信息端口

    局部修改用户信息, 修改任意指定的用户信息
    multiple_delete:
    批量删除用户端口

    输入要删除的用户ID列表,现实一次性删除多个用户
    """
    queryset = UserModel.objects.all()
    pagination_class = GlobalPagination

    def get_serializer_class(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            return UserWriteOnlySerializer
        else:
            return UserReadOnlySerializer

class UserResetPasswordView(GenericAPIView,UpdateModelMixin):
    """
    用户重置密码:

    只要用到patch方法局部修改个人信息中的密码
    :return 修改成功后返回个人信息,status:200(成功),但不显示密码
    """
    queryset = UserModel.objects.all()
    serializer_class = UserResetPasswordSerializer

    def patch(self,request,*args,**kwargs):
        return self.partial_update(request, *args, **kwargs)


