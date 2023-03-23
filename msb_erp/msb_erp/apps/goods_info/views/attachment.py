from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser

from goods_info.models import AttachmentModel
from goods_info.serializer.attachment_serializer import AttachmentSerializer

class AttachmentView(mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    """
    create:
    附件或者图片--新增。

    a_file：必须是选择的一个文件， a_type:是一个字符串，参考模型类代码 附件或者图片新增, status: 201(成功), return: 新增附件或者图片信息
    destroy:
    附件或者图片--删除

    附件或者图片删除, status: 204(成功), return: None
    list:
    附件或者图片--获取分页列表

    附件或者图片列表信息, status: 200(成功), return: 附件或者图片信息列表
    retrieve:
    查询某一个附件或者图片

    查询指定ID的附件或者图片, status: 200(成功), return: 用户附件或者图片
    """
    parser_classes = (MultiPartParser,)
    queryset = AttachmentModel.objects.all()
    serializer_class = AttachmentSerializer

    file = openapi.Parameter(name='a_file', in_=openapi.IN_FORM, type=openapi.TYPE_FILE, required=True,
                             description='上传文件')

    @swagger_auto_schema(manual_parameters=[file])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
