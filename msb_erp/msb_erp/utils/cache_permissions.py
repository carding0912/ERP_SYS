import json

from django_redis import get_redis_connection

from erp_system.models import PermissionsModel


def redis_storage_permissions(user):
    """把当前用户的权限信息,缓存到Redis数据库中
    Redis 中存放用户权限的结构为:user_用户id----> 字典{key:path,value[列表] }(json字符串)
    """
    permission_ids = user.roles.values_list('permissions', flat=True).distinct()

    # 根据权限id,获取权限的所有值,一级菜单的权限除外
    permissions = PermissionsModel.objects.filter(is_menu=False, id__in=permission_ids).values('id', 'path', 'method',
                                                                                               'name')
    if not permissions.exists():  # 如果没有查到权限
        return
    permissions_dict ={}  # 存放当前用户的权限 path为键
    for permission in permissions:
        # 因为数据需要转换成json格式的字符串,所以排除那些增加权限时无意输入的特殊符号
        # '\u200b' 是Unicode中的零宽度字符,可以理解为不可见字符
        method = str(permission.get('method')).replace('\u200b','')
        path = str(permission.get('path')).replace('\u200b','')
        _name = str(permission.get('name')).replace('\u200b','')
        _id = str(permission.get('id'))

        if path in permissions_dict:
            permissions_dict[path].append({'method':method,'sign':_name,'id':_id})
        else:
            permissions_dict[path] = [{'method':method,'sign':_name,'id':_id}]

    for key in permissions_dict:
        permissions_dict[key] = json.dumps(permissions_dict[key])

    # 存入redis中
    redis_conn = get_redis_connection('default')  # 连接redis数据库
    redis_conn.hmset(f'user_{user.id}',permissions_dict)


