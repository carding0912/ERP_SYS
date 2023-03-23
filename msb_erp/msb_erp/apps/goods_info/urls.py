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
from rest_framework import routers

from goods_info.views import category, units, attachment, goods

urlpatterns = []

router = routers.DefaultRouter()
router.register(r'category',category.CategoryView)   # 货品类别管理的路由
router.register(r'units',units.UnitsView)   # 计量单位管理的路由
router.register(r'attachment',attachment.AttachmentView)   # 上传文件管理的路由
router.register(r'goods',goods.GoodsView)   # 上传文件管理的路由
urlpatterns += router.urls