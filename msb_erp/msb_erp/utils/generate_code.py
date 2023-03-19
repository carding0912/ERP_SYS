import string
import time
import random


def generate_code(prefix):
    """
    生成28位流水编号: 3位前缀 + 14位的时间 + 7位的微秒 + 4位随机数
    """
    seeds = string.digits
    random_str = random.choices(seeds, k=4)

    random_str = "".join(random_str)
    code_no = "%s%s%s%s" % (prefix,
                            time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())),
                            str(time.time()).replace('.', '')[-7:],
                            random_str)
    return code_no


if __name__ == '__main__':
    print(generate_code('ORD'))
