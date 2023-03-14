"""msb_erp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token   # JWT处理登陆的视图函数
from .views import menu, user, roles, permissions, dept

urlpatterns = [
    re_path(r'^user/login/$',obtain_jwt_token),    # JWT 签发和认证token的视图类
    re_path(r'^user/register/$',user.RegisterView.as_view()),    # 用户账户注册路由
    re_path(r'^user/reset_password/(?P<pk>\d+)/$',user.UserResetPasswordView.as_view()),    # 用户修改密码

]

router = routers.DefaultRouter()
router.register(r'menus',menu.MenuView)
router.register(r'roles',roles.RolesView)
router.register(r'permissions',permissions.PermissionsView)
router.register(r'dept',dept.DeptView)
router.register(r'user',user.UsersView)
urlpatterns += router.urls