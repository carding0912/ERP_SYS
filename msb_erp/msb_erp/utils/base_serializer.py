from rest_framework import serializers


class ChoiceGoodsSerializer(serializers.Serializer):
    """
    选择商品列表的序列化器 和 反序列化
    """
    # 反序列化使用的属性
    keyword = serializers.CharField(label='货品搜索关键字,名称,型号,规格,颜色',write_only=True,required=False)
    # 反序列化和序列化都使用的属性
    number_code = serializers.CharField(label='货品编号',required=False)
    category_id = serializers.IntegerField(label='货品类别ID',required=False)
    warehouse_id = serializers.IntegerField(label='仓库ID',required=False)
    # 序列化都使用的属性
    id = serializers.IntegerField(label='货品ID',read_only=True)
    name = serializers.CharField(label='货品名称',read_only=True)
    category__name = serializers.CharField(label='货品名称',read_only=True)
    specification = serializers.CharField(label='货品规格',read_only=True)
    model_number = serializers.CharField(label='货品型号',read_only=True)
    color = serializers.CharField(label='货品颜色',read_only=True)
    units__basic_name = serializers.CharField(label='货品单位',read_only=True)
    cur_inventory = serializers.CharField(label='当前库存',read_only=True)

