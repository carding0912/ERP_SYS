from django.db import models

# Create your models here.

class Nation(models.Model):
    id = models.IntegerField(primary_key=True)
    n_name = models.CharField('国家名称',max_length=30)

    class Meta:
        db_table = 'nation'
        verbose_name = '国家表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.n_name

class Province(models.Model):
    id = models.IntegerField(primary_key=True)
    p_name = models.CharField('省份名称',max_length=30)
    nation = models.ForeignKey(to=Nation,related_name='province_list',on_delete=models.CASCADE)

    class Meta:
        db_table = 'province'
        verbose_name = '省份表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.p_name

class City(models.Model):
    id = models.IntegerField(primary_key=True)
    c_name = models.CharField('省份名称',max_length=30)
    province = models.ForeignKey(to=Province,related_name='city_list',on_delete=models.CASCADE)

    class Meta:
        db_table = 'city'
        verbose_name = '城市表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.c_name



