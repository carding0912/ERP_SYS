# Generated by Django 3.2.6 on 2023-03-17 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_info', '0003_alter_province_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creat_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('delete_flag', models.BooleanField(default=False, max_length=1, verbose_name='启动和禁用标记')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='供应商名称')),
                ('mobile', models.CharField(max_length=11, verbose_name='手机号码')),
                ('phone', models.CharField(max_length=22, verbose_name='联系电话')),
                ('contacts_name', models.CharField(max_length=22, verbose_name='联系人名')),
                ('email', models.CharField(max_length=50, verbose_name='电子邮箱')),
                ('ratepayer_number', models.CharField(max_length=50, verbose_name='纳税人识别号码')),
                ('bank', models.CharField(max_length=50, verbose_name='开户银行')),
                ('account_number', models.CharField(max_length=50, verbose_name='银行账号')),
                ('nation', models.CharField(max_length=50, verbose_name='国家')),
                ('province', models.CharField(max_length=50, verbose_name='省份')),
                ('city', models.CharField(max_length=50, verbose_name='城市')),
                ('address', models.CharField(max_length=50, verbose_name='详细地址')),
                ('remark', models.CharField(max_length=512, verbose_name='备注')),
                ('init_pay', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='初期应付')),
                ('current_pay', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='末期应付')),
                ('order_number', models.IntegerField(default=100, verbose_name='排序号码')),
            ],
            options={
                'verbose_name': '供应商',
                'verbose_name_plural': '供应商',
                'db_table': 't_supplier',
                'ordering': ['order_number', 'id'],
            },
        ),
    ]