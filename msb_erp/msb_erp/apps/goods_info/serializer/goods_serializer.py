from django.db import transaction
from rest_framework import serializers
from goods_info.models import GoodsInventoryModel, GoodsModel, AttachmentModel
from goods_info.serializer.attachment_serializer import AttachmentSerializer
from goods_info.serializer.goodscategory_serializer import CategorySerializer
from goods_info.serializer.units_serializer import UnitsSerializer
from msb_erp.utils.get_inventory import get_inventory


class GoodsInventorySerializer(serializers.ModelSerializer):
    """
    商品的库存 序列化器
    """

    class Meta:
        model = GoodsInventoryModel
        fields = '__all__'


class GoodsBaseSerializer(serializers.ModelSerializer):
    """
    商品新增，修改，的序列化器
    """
    # 商品对应的多个：商品库存对象。因为有很多个仓库
    inventory_list = GoodsInventorySerializer(many=True, required=True)

    class Meta:
        model = GoodsModel
        fields = '__all__'

    def create(self, validated_data):
        item_list = validated_data.pop('inventory_list')
        with transaction.atomic():
            goods = GoodsModel.objects.create(**validated_data)
            for item in item_list:
                item['cur_inventory'] = item.get('init_inventory', 0)  # 新建时，当前库存=初始库存
                GoodsInventoryModel.objects.create(goods=goods, **item)
        return goods

    def update(self, instance, validated_data):
        item_list = validated_data.pop('inventory_list')
        # 保护代码,去掉取出的商品数据库信息,保证只有库存数据库信息
        # old_list = instance.inventory_list.all()
        #
        # if old_list.exists():
        #     # 然后把旧数据删除，因为在validated_data拿不到货品库存数据的ID
        #     instance.inventory_list.all().delete()
        with transaction.atomic():
            for item in item_list:  # 遍历每条库存信息，并修改最高库存和最低库存
                GoodsInventoryModel.objects.filter(warehouse__name=item['warehouse_name']).update(
                    lowest_inventory=item.get('lowest_inventory', 0), highest_inventory=item.get('highest_inventory', 0))
            goods = super(GoodsBaseSerializer, self).update(instance=instance, validated_data=validated_data)
        return goods

class GoodsGetSerializer(serializers.ModelSerializer):
    """
    商品查询的序列化器
    目标：
        1、把商品的单位——所有信息展示出来
        2、展示商品信息所属的商品列表——所有信息展示出来
        3、展示商品的所有附件图片——所有图片信息展示出来
        4、展示商品的所有仓库中的库存信息
    """

    units = UnitsSerializer(read_only=True)     # 嵌套序列化器拿所有信息
    # units = serializers.CharField(source='basic_name')     # 自定义序列化字段,拿关联表的指定字段
    category = CategorySerializer(read_only=True)
    images_list = serializers.SerializerMethodField(read_only=True)
    inventory_list = GoodsInventorySerializer(many=True, read_only=True)
    # 该货品的当前总库存数量
    cur_inventory = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = GoodsModel
        fields = '__all__'

    def get_images_list(self, obj):
        result = []  # 返回的列表，列表中是多个字典(每个字典就是一个附件)
        if obj.images_list:
            # images_list属性是由多个附件的ID组成，中间使用逗号分割
            ids = obj.images_list.split(',')
            if ids:
                for i in ids:
                    image = AttachmentModel.objects.get(id=int(i))
                    ser = AttachmentSerializer(instance=image)
                    result.append(ser.data)
        return result

    def get_cur_inventory(self, obj):
        return get_inventory(obj.id)