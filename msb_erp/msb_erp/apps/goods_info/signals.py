from django.db.models.signals import post_save
from django.dispatch import receiver
from basic_info.models import WarehouseModel
from goods_info.models import GoodsModel, GoodsInventoryModel
import logging

logger = logging.getLogger('erp')


@receiver(post_save, sender=WarehouseModel)
def create_goods_inventory(sender, instance, created, **kwargs):
    """
    创建信号监控函数
    创建新仓库之后， 给所有的货品在当前的新仓库 新增库存数据
    """
    if created:
        logger.info('创建当前的新仓库——新增库存数据')
        if isinstance(instance, WarehouseModel):
            # 首先查询所有的货品id
            ids = GoodsModel.objects.values_list('id', flat=True).all()
            inventory_list = []
            for gid in ids:
                inventory_list.append(GoodsInventoryModel(
                    goods_id=gid,
                    warehouse_name=instance.name,
                    warehouse=instance
                ))
            # 一定要采用批量新增函数：bulk_create
            GoodsInventoryModel.objects.bulk_create(inventory_list)   # bulk_create()方法用于批量插入数据库表格数据
        else:
            logger.info('不是WarehouseModel类型，所以不需要创建库存数据')