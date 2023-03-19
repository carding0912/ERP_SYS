from enum import unique, Enum


@unique
class NumberPrefix(Enum):

    acc = 'ACC'  # 结算账户编号的前辍
    ord = "ORD"  # 销售订单编号的前辍
    cat = "CAT"  # 商品类别编号的前辍
    goo = "GOO"  # 商品信息编号的前辍