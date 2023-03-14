from rest_framework.pagination import PageNumberPagination


class GlobalPagination(PageNumberPagination):
    # 项目默认的分页配置
    page_size = 10  # 每页显示数据条数
    page_size_query_param = 'size'  # 前端发送每页显示数目的参数名:/?size=?
    max_page_size = 100   #保护性代码,前端能够设置的每页数量的上限