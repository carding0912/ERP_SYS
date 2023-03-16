import json
import logging
import re

from django.conf import settings
from django_redis import get_redis_connection
from rest_framework.permissions import BasePermission

from msb_erp.utils.cache_permissions import redis_storage_permissions

logger = logging.getLogger('erp')


class RbacPermission(BasePermission):
    @staticmethod
    def do_url(url):
        """
        把一个不完整的接口地址,变成一个完整的
        :param url: 从redis中取出的不完整的url
        :return: 一个完整的url
        """
        base_api = settings.BASE_API
        uri = '/' + base_api + '/' + url + '/'
        return re.sub('/+', '/', uri)  # 防止拼接后的地址中出现多个/,进行替换

    def has_permission(self, request, view):
        """
        判断是否有权限,该函数必须要重写
        思路和步骤:
        1 获取请求的url,和请求方法method,user用户对象
        2 判断是否白名单的url,或者用户的角色是admin也直接放行
        3 从redis中得到当前登录用户的所有权限
        4 判断是否存在权限
        """
        request_url = request.path
        request_method = request.method
        logger.info(f'请求地址为:{request_url},请求方法为:{request_method}')
        for safe_url in settings.WHITE_LIST:
            if re.match(settings.REGEX_URL.format(url=safe_url), request_url):  # 用户请求的是白名单中的url
                return True

        user = request.user  # 查看当前登录的用户
        role_name_list = user.roles.values_list('name', flat=True)
        if "admin" in role_name_list:
            return True

        # 从redis中来获取该用户的所有权限
        redis_conn = get_redis_connection('default')
        if not redis_conn.exists(f'user_{user.id}'):
            redis_storage_permissions(user)  # 如果redis中没有缓存权限,再次从mysql中取出权限并缓存到redis中

        # 得到所有的权限中key,其中key是接口的url地址
        url_keys = redis_conn.hkeys(f'user_{user.id}')
        redis_key = None
        for url_key in url_keys:
            if re.match(settings.REGEX_URL.format(url=self.do_url(url_key.decode())), request_url):
                # 判断redis中的url和请求中的url是一致的
                redis_key = url_key.decode()
                break

        if redis_key:
            perms = json.loads(redis_conn.hget(f'user_{user.id}',redis_key).decode())  #perms是一个列表
            for permission in perms:
                if permission.get('method') == request_method:
                    return True
        else:
            return False







