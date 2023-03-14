import logging
from django.contrib.auth.backends import ModelBackend

from msb_erp.utils.cache_permissions import redis_storage_permissions
from .models import UserModel

logger = logging.getLogger('erp')


class UserLoginAuth(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        实现用户认证
        """
        try:
            user = UserModel.objects.get(username=username)
        except:
            return None
        # 判断密码
        if user.check_password(password):
            redis_storage_permissions(user)
            return user  # 把user对象返回到request中
