import logging
from celery import shared_task
from erp_system.models import PermissionsModel, MenuModel
from msb_erp.utils.tasks_hook import HookTask

logger = logging.getLogger('erp')
methods = {'POST': '新增', 'GET': '查询', 'PUT': '修改', 'DELETE': '删除', 'PATCH': '改局部'}

@shared_task(base=HookTask)    # HookTask 是指定的任务钩子,监控并打印任务的执行
def create_menu_permission(menu_id):  # 创建celery任务函数, 是项目中创建菜单资源对应的权限
    instance = MenuModel.objects.get(pk=menu_id)

    if not instance.parent:   # 如果不是父菜单,那么menu就是功能块菜单对象
        permission = PermissionsModel.objects.create(name=instance.name + '的权限', is_menu=True)
        permission.menu = instance
        permission.save()
        return logger.info('创建了功能块菜单对象,已在MenuModel中插入了数据,但是没有提供权限')
    else:  # 当前菜单是接口
        for method in methods.keys():
            permission = PermissionsModel.objects.create(name=methods.get(method),
                                                         desc=f'{instance.name}的{methods.get(method)}的权限',
                                                         is_menu=False, method=method, path=instance.url)
            permission.menu = instance
            permission.save()
        return logger.info('已创建菜单资源对应的权限')

@shared_task(base=HookTask)    # HookTask 是指定的任务钩子,监控并打印任务的执行
def change_menu_permission(menu_id):
    PermissionsModel.objects.filter(menu_id=menu_id).delete()
    instance = MenuModel.objects.get(id=menu_id)
    if instance.parent:
        for method in methods.keys():
            PermissionsModel.objects.create(name=methods.get(method),
                                            desc=f'{instance.name}的{methods.get(method)}的权限',
                                            is_menu=False, method=method, path=instance.url, menu=instance)
    else:
        PermissionsModel.objects.create(name=str(instance.name) + '的权限', is_menu=True ,menu=instance)
