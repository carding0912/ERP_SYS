from django.db import models


class BaseModel(models.Model):
    """
    抽象类,所有模型类的父类,定义了公共字段
    """
    creat_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        abstract = True


class BaseModel2(BaseModel):
    """
    抽象类,所有业务有关模型类的父类,定义了公用属性
    """
    delete_flag = models.BooleanField('启动和禁用标记', max_length=1, default=False)

    class Meta:
        abstract = True
