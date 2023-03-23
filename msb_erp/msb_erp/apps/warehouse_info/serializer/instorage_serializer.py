from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from goods_info.models import GoodsModel
from msb_erp.utils.get_inventory import get_inventory
from warehouse_info.models import PurchaseStorageModel, PurchaseStorageItemModel


class InStorageItemSerializer(serializers.ModelSerializer):
    """
    入库单--反序列化器(只用于新增和修改)和查询列表的序列化器(用于入库单列表)
    由于要显示库存数据,所以序列化器中要增加一个库存字段
    """
    cur_inventory = serializers.SerializerMethodField(read_only=True,label='在当前仓库中的库存')

    class Meta:
        model = PurchaseStorageItemModel
        fields = "__all__"

    def get_cur_inventory(self,obj:PurchaseStorageItemModel):
        result = get_inventory(obj.goods.id,obj.warehouse.id) if get_inventory(obj.goods.id,obj.warehouse.id) else 0
        return result

class InStorageSerializer(serializers.ModelSerializer):
    """
    入库单--反序列化器(只用于新增和修改)和查询列表的序列化器(用于入库单列表)
    """
    item_list = InStorageItemSerializer(many=True, write_only=True)
    goods_info = serializers.SerializerMethodField(read_only=True,label='入库单中的每个商品信息')

    class Meta:
        model = PurchaseStorageModel
        fields = "__all__"

    def get_goods_info(self,obj:PurchaseStorageModel):
        """
        商品信息是由:商品1名称 商品规格,商品2名称 商品规格,.....

        """
        if obj.item_list.all():
            result = []
            for item in obj.item_list.all():
                result.append(item.name + (item.specification if item.specification else ''))
            return ','.join(result)
        return ''

    def create(self, validated_data):
        item_list = validated_data.pop('item_list')
        with transaction.atomic():
            in_storage = PurchaseStorageModel.objects.create(**validated_data)
            for item in item_list:
                psi: PurchaseStorageItemModel = PurchaseStorageItemModel.objects.create(purchase_storage=in_storage,
                                                                                        **item)
            goods: GoodsModel = item.get('goods')
            psi.specification = goods.specification
            psi.model_number = goods.model_number
            psi.number_code = goods.number_code
            psi.color = goods.color
            psi.category = goods.category
            psi.category_name = goods.category.name
            psi.units = goods.units
            psi.units_name = goods.units.basic_name
            psi.save()
        return in_storage

    def update(self, instance, validated_data):
        if instance.status != '0':
            raise ValidationError('入库订单已经生效,不能修改.')
        item_list = validated_data.pop('item_list')
        old_list = instance.item_list.all()
        with transaction.atomic():
            if old_list.exists():
                old_list.delete()
            for item in item_list:
                psi: PurchaseStorageItemModel = PurchaseStorageItemModel.objects.create(purchase_storage=instance,
                                                                                        **item)
                goods: GoodsModel = item.get('goods')
                psi.specification = goods.specification
                psi.model_number = goods.model_number
                psi.number_code = goods.number_code
                psi.color = goods.color
                psi.category = goods.category
                psi.category_name = goods.category.name
                psi.units = goods.units
                psi.units_name = goods.units.basic_name
                psi.save()
        return super(InStorageSerializer, self).update(validated_data=validated_data, instance=instance)


# 用于查询单个入库单的序列化器
class InStorageGetSerializer(serializers.ModelSerializer):
    """
    入库单--序列化器 查询单个入库单的序列化器
    显示的列包括:仓库名称,货品编号,货品名称,规格,型号,颜色,库存,单位,入库数量,单价,金额,备注
    注意:以上显示只有库存数据没有
    """
    item_list = InStorageItemSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseStorageModel
        fields = "__all__"