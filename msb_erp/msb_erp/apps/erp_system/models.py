from django.db import models

from msb_erp.utils.base_model import BaseModel


# Create your models here.
class MenuModel(BaseModel):
    """
    功能菜单模型类
    """
    number = models.IntegerField('排序数字',blank=True,null=True)
    url = models.CharField('菜单访问的url地址',max_length=256,blank=True,null=True)
    name = models.CharField('菜单访问的url地址',max_length=256,blank=True,null=True)
    # 前端调用删除功能的时候,后端数据库不会真正的删除数据,而是把数据设置成不显示的操作,默认是0为显示,1为不显示
    delete_flag = models.CharField('删除的标记',max_length=1,default='0')
    parent = models.ForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)

    class Meta:
        db_table = 't_menu'
        verbose_name = '功能菜单表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
