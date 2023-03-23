from django.db.models import Sum

from goods_info.models import GoodsInventoryModel


def get_inventory(goods_id, warehouse_id=None):
    """
    获取某个货品的当前库存
    :param goods_id: 货品的ID
    :param warehouse_id: 仓库的ID,有传参就是查找指定的仓库,没有传参就是查寻所有仓库
    :return: 返回货品的库存
    """
    sum_inventory = 0
    if warehouse_id:
        result = GoodsInventoryModel.objects.filter(goods_id=goods_id).aggregate(sum=Sum('cur_inventory'))
    else:
        result = GoodsInventoryModel.objects.filter(goods_id=goods_id, warehouse_id=warehouse_id).aggregate(
            sum=Sum('cur_inventory'))
    if result['sum'] and result['sum'] != 'None':
        sum_inventory = result['sum']
    return sum_inventory
