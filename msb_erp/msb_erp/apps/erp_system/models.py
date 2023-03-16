from django.contrib.auth.models import AbstractUser
from django.db import models
from msb_erp.utils.base_model import BaseModel


# Create your models here.
class MenuModel(BaseModel):
    """
    功能菜单模型类
    """
    number = models.IntegerField('排序数字', blank=True, null=True)
    url = models.CharField('菜单访问的url地址', max_length=256, blank=True, null=True)
    name = models.CharField('菜单名称', max_length=256, blank=True, null=True)
    # 前端调用删除功能的时候,后端数据库不会真正的删除数据,而是把数据设置成不显示的操作,默认是0为显示,1为不显示
    delete_flag = models.CharField('删除的标记', max_length=1, default='0')
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        db_table = 't_menu'
        verbose_name = '功能菜单表'
        verbose_name_plural = verbose_name
        ordering = ['number']

    def __str__(self):
        return self.name


# erp系统的用户模型类
class UserModel(AbstractUser, BaseModel):
    phone = models.CharField('手机号码', max_length=11, unique=True, blank=True, null=True)
    real_name = models.CharField('真实姓名', max_length=64, blank=True, null=True)
    # 用户所有角色
    roles = models.ManyToManyField('RolesModel', db_table='t_users_roles', blank=True, verbose_name='用户所有的角色')
    dept = models.ForeignKey(to='DeptModel', blank=True, null=True, verbose_name='所属部门', on_delete=models.SET_NULL)

    class Meta:
        db_table = 't_user'
        verbose_name = '系统用户表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username + ':' + self.real_name


class PermissionsModel(BaseModel):
    """
    权限的模型类,包含两个要素:资源(父菜单,接口),操作
    """
    method_choices = (
        ('POST', '增'),
        ('DELETE', '删'),
        ('PUT', '改'),
        ('PATCH', '改局部'),
        ('GET', '查')
    )
    """
    只要是choices参数的字段,如果你想要获取对应的key和value,默认获取的是key,如果需要获取value,可以采用get_字段名_display()获取
    例: print(permission.method)  获取key
        print(permission.get_method_display()) 获取value
    """
    # method_choices = ('POST', 'DELETE', 'PUT', 'PATCH', 'GET')  #  也可以这么写

    name = models.CharField('权限名称', max_length=50)
    is_menu = models.BooleanField('是否为菜单', default=True)  # True为菜单,False为子菜单
    # 操作
    method = models.CharField('操作', max_length=8, blank=True, default='', choices=method_choices)
    path = models.CharField('访问url地址', max_length=256, blank=True, null=True)
    desc = models.CharField('权限的描述', max_length=512, blank=True, null=True)
    menu = models.ForeignKey('MenuModel', null=True, blank=True, related_name='permissions_list',
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_permissions'
        verbose_name = '权限表'
        verbose_name_plural = verbose_name
        ordering = ['id']


class RolesModel(BaseModel):
    """
    角色模型
    """
    name = models.CharField('角色名称', unique=True, max_length=50)
    permissions = models.ManyToManyField('PermissionsModel', db_table='t_roles_permissions',
                                         blank=True, verbose_name='角色的权限')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_roles'
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        ordering = ['id']


class DeptModel(BaseModel):
    """
    部门模型
    """
    name = models.CharField('部门名称', unique=True, max_length=50)
    address = models.CharField('部门地址', blank=True, null=True, max_length=256)
    parent = models.ForeignKey(to='self', verbose_name='部门从属(上级)部门', related_name='children', blank=True,
                               null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_dept'
        verbose_name = '部门表'
        verbose_name_plural = verbose_name
        ordering = ['id']
