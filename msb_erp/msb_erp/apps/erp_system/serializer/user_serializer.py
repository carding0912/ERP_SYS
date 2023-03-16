import re

from rest_framework import serializers

from erp_system.models import UserModel
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from erp_system.serializer.dept_serializer import DeptSerializer
from erp_system.serializer.role_serializer import BaseRolesSerializer


class UserRegisterSerializer(ModelSerializer):
    """
    用户注册的序列化类
    """

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'password', 'phone', 'real_name')
        extra_kwargs = {
            'username': {
                'max_length': 12,
                'min_length': 2
            },
            'password': {
                'max_length': 8,
                'min_length': 6,
                'write_only': True
            }
        }

    @staticmethod
    def validate_phone(phone):
        """
        验证手机号码,自定义一个验证的函数(命名规则:validate_+字段名字)
        """
        if not phone:
            return phone
        else:
            if not re.match(r'^1[3589]\d{9}$', phone):
                raise ValidationError('请输入正确的手机号码')
        return phone

    def create(self, validated_data):
        """
        必须要重写create函数,因为用户的密码是不允许明文插入到数据库

        """
        user = UserModel.objects.create_user(**validated_data)
        return user


class UserWriteOnlySerializer(ModelSerializer):
    """
    用于用户的反序列化器
    """

    class Meta:
        model = UserModel
        fields = ('id', 'phone', 'real_name', 'roles', 'dept')


class UserReadOnlySerializer(ModelSerializer):
    """
    用于用户的序列化器
    """
    roles = BaseRolesSerializer(many=True, read_only=True)
    dept = DeptSerializer(many=False, read_only=True)

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'phone', 'real_name', 'roles', 'dept')


class UserResetPasswordSerializer(ModelSerializer):
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = UserModel
        fields = ('id', 'password', 'new_password', 'confirm_password')
        extra_kwargs = {
            'password': {"write_only": True},
            'new_password': {"write_only": True},
            'confirm_password': {"write_only": True},
        }

    def validate(self, attrs):
        """
        attrs: 就是创建序列化器对象时，传入data数据
        """
        password = attrs.get('password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        if not password:
            raise ValidationError('请输入原始密码')
        if not new_password:
            raise ValidationError('请输入新密码')
        if not confirm_password:
            raise ValidationError('请确认新密码')
        if new_password != confirm_password:
            raise ValidationError('两次输入的密码不一致')
        return attrs

    def save(self, **kwargs):
        if not self.instance.check_password(self.validated_data.get('password')):
            raise ValidationError('输入的密码不正确')
        else:
            self.instance.set_password(self.validated_data.get('new_password'))
            self.instance.save()
        return self.instance
