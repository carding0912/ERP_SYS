# Generated by Django 3.2.6 on 2023-03-09 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='phone',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='手机号码'),
        ),
    ]