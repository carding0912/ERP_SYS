from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from goods_info.models import GoodsModel
from msb_erp.utils.get_inventory import get_inventory
from purchase_info.models import PurchaseModel, PurchaseItemModel


class PurchaseItemSerializer(serializers.ModelSerializer):
    """
    采购订单的序列化 反序列化器
    """

    class Meta:
        model = PurchaseItemModel
        fields = "__all__"


class PurchaseSerializer(serializers.ModelSerializer):
    """
    采购订单的序列化 反序列化器
    """
    item_list = PurchaseItemSerializer(many=True, write_only=True)
    # 采购订单列表中需要展示:商品信息,多个商品的名字+规格,中间使用逗号隔开组成的
    goods_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PurchaseModel
        fields = "__all__"

    def get_goods_info(self, obj):
        """
        商品的信息是由"商品1名称 商品1规格,商品2名称 商品2规格 ,.....
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
            purchase = PurchaseModel.objects.create(**validated_data)
            for item in item_list:
                pim = PurchaseItemModel.objects.create(purchase=purchase, **item)
                goods = item.get('goods')
                pim.name = goods.name
                pim.specification = goods.specification
                pim.number_code = goods.number_code
                pim.save()
        return purchase

    def update(self, instance: PurchaseModel, validated_data):
        if instance.status != '0':
            raise ValidationError('采购订单已经生效,不能修改.')
        item_list = validated_data.pop('item_list')
        old_list = instance.item_list.all()
        with transaction.atomic():
            if old_list.exists():
                old_list.delete()
            for item in item_list:
                pim = PurchaseItemModel.objects.create(purchase=instance, **item)
                goods = item.get('goods')
                pim.name = goods.name
                pim.specification = goods.specification
                pim.number_code = goods.number_code
                pim.save()
        return super(PurchaseSerializer, self).update(validated_data=validated_data, instance=instance)
        # PurchaseModel.objects.filter(id=instance.id).delete()
        # self.create(validated_data=validated_data)


class PurchaseGetSerializer(serializers.ModelSerializer):
    """
    仅仅用于查询单个采购订单的序列化器
    """
    item_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PurchaseModel
        fields = "__all__"

    def get_item_list(self,obj):
        result = []  # 返回的列表,列表中是多个字典
        if obj.item_list.all().exists():
            for item in obj.item_list.all():   # item 是一个PurchaseItemModel对象
                # 有一部分信息在PurchaseItemModel里面没有
                #  只有在GoodsModel里面有:颜色 型号 单位
                item_dict = {}
                goods = GoodsModel.objects.get(id=item.goods.id)
                item_dict['goods'] = goods.id
                item_dict['name'] = goods.name
                item_dict['number_code'] = goods.number_code
                item_dict['specification'] = goods.specification
                item_dict['model_number'] = goods.model_number
                item_dict['color'] = goods.color
                item_dict['units'] = goods.units.basic_name
                item_dict['cur_inventory'] = get_inventory(goods.id)
                item_dict['purchase_count'] = item.purchase_count
                item_dict['purchase_price'] = item.purchase_price
                item_dict['purchase_money'] = item.purchase_money
                item_dict['remark'] = item.remark
                result.append(item_dict)
        return result

