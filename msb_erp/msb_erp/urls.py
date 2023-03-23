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
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls

from msb_erp.utils import base_views

schema_view = get_schema_view(
    openapi.Info(
        title="ERP系统API接口",
        default_version='drf3.14版API接口',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

    path('admin/', admin.site.urls),
    re_path(r'^api/', include('erp_system.urls')),
    re_path(r'^api/', include('basic_info.urls')),
    re_path(r'^api/', include('goods_info.urls')),
    re_path(r'^api/', include('purchase_info.urls')),
    re_path(r'^api/', include('warehouse_info.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # 媒体资源文件的访问路由
    re_path(r'^api/generate_code/$', base_views.GenerateCode.as_view()),  # 自动生成编号的路由
    re_path(r'^api/search_goods/$', base_views.ChoiceGoodsView.as_view()),  # 选择商品的搜索过滤查询
    path('docs/', include_docs_urls(title='ERP接口文档')),
    path('doc<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),  # 导出.json格式
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # 文档接口1
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # 文档接口2
]
