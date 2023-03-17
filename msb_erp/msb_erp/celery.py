import os

from celery import Celery
from django.conf import settings

# 为celery设置django默认的环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'msb_erp.settings.dev')
# 注册celery的APP,参数必须是项目名字
app = Celery('msb_erp')

# 绑定celery的配置文件,一般配置在settings文件中以大写的CELERY开头,以免与其它设置产生冲突
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动加载任务的APP,通常设置为已注册的APP应用中加载
app.autodiscover_tasks(lambda :settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')