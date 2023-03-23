from django.apps import AppConfig


class GoodsInfoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'goods_info'

    def ready(self):
        import goods_info.signals
