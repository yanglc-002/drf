#!/usr/bin/env python3
# _*_ coding:utf8 _*_
# __author__ = yanglc

from rest_framework import serializers
from .models import User
import re




#初始化


"""
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
"""

#序列化验证
"""
from rest_framework import serializers
from .models import User
import re


class UserSerializer(serializers.ModelSerializer):
    # 因为phone没有办法支持11位，需重新定义phone规则。
    phone = serializers.CharField(max_length=11, min_length=11, required=True)

    class Meta:
        model = User
        fields = "__all__"

    # 自定义单个字段验证规则：validate_验证字段名(phone)，参数：传入的是当前字段(phone)
    # 当我们序列化的时候，phone字段就会走自定义序列化函数
    def validate_phone(self, phone):
        # 检测手机是否合法
        if not re.match(r'1[3456789]\d{9}', phone):
            raise serializers.ValidationError("手机号码不合法")  # 如果不匹配我抛出一个异常

        # 检测手机号是否存在
        if User.objects.filter(phone=phone).all():
            raise serializers.ValidationError("手机号已被注册")

        return phone  # 一定要有返回值，意思就是把你验证后的字段返回给模型类
"""


#组合字段验证(validate)
"""
class UserSerializer(serializers.ModelSerializer):
    # 因为phone没有办法支持11位，需重新定义phone规则。
    phone = serializers.CharField(max_length=11, min_length=11, required=True)
    # 序列化一个新字段pwd1，只是我们这个字段的值不保存数据库，后续验证完毕之后需要删除
    pwd1 = serializers.CharField(max_length=64, write_only=True)  # write_only表示必须要从前端传递过来
    class Meta:
        model = User
        fields = "__all__"

    # 自定义单个字段验证规则：validate_验证字段名(phone)，参数：传入的是当前字段(phone)
    # 当我们序列化的时候，phone字段就会走自定义序列化函数
    def validate_phone(self, phone):  # 单个验证
        # 检测手机是否合法
        if not re.match(r'1[3456789]\d{9}', phone):
            raise serializers.ValidationError("手机号码不合法")  # 如果不匹配我抛出一个异常

        # 检测手机号是否存在
        if User.objects.filter(phone=phone).all():
            raise serializers.ValidationError("手机号已被注册")

        return phone  # 一定要有返回值，意思就是把你验证后的字段返回给模型类

    def validate(self, attrs):  # 组合验证
        # print(attrs)  #attrs是：OrderedDict([('phone', '18366666666'), ('pwd1', '12345'), ('name', '杨**'), ('gender', 1), ('pwd', '12345')])
        if attrs.get('pwd1') != attrs.get('pwd'):
            raise serializers.ValidationError("两次密码不一样")
        attrs.pop('pwd1')  # 验证完毕需要删除pwd1，因为pwd1在模型类User中没有这个字段
        return attrs  # 一定要有返回值
    
"""




# #登录密码加密
"""
class UserSerializer(serializers.ModelSerializer):
    # 因为phone没有办法支持11位，需重新定义phone规则。
    phone = serializers.CharField(max_length=11, min_length=11, required=True)
    # 序列化一个新字段pwd1，只是我们这个字段的值不保存数据库，后续验证完毕之后需要删除
    pwd1 = serializers.CharField(max_length=64, write_only=True)  # write_only表示必须要从前端传递过来

    gender = serializers.CharField(source='get_gender_display')  # 根据source数据来源定义字段
    class Meta:
        model = User
        fields = "__all__"

    # def create(self, validated_data):
    #     # 重写create方法，对密码加密完之后，再插入到数据库中
    #     return User.objects.create()



    # 自定义单个字段验证规则：validate_验证字段名(phone)，参数：传入的是当前字段(phone)
    # 当我们序列化的时候，phone字段就会走自定义序列化函数
    def validate_phone(self, phone):  # 单个验证
        # 检测手机是否合法
        if not re.match(r'1[3456789]\d{9}', phone):
            raise serializers.ValidationError("手机号码不合法")  # 如果不匹配我抛出一个异常

        # 检测手机号是否存在
        if User.objects.filter(phone=phone).all():
            raise serializers.ValidationError("手机号已被注册")

        return phone  # 一定要有返回值，意思就是把你验证后的字段返回给模型类

    def validate(self, attrs):  # 组合验证
        # print(attrs)
        if attrs.get('pwd1') != attrs.get('pwd'):
            raise serializers.ValidationError("两次密码不一样")
        attrs.pop('pwd1')  # 验证完毕需要删除pwd1，因为pwd1在模型类User中没有这个字段
        return attrs  # 一定要有返回值

"""

#重写 to_representation 方法
"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def to_representation(self, instance):  # 重写to_representation方法
        representation = super(UserSerializer, self).to_representation(instance)  # 继承UserSerializer父类
        representation['gender'] = instance.get_gender_display()  # 重新定义gender字段

        return representation
"""


# 重新定义字段，实现可读可写
#
# from collections import OrderedDict
#
# class ChoiceDisplayField(serializers.Field):
#     """Custom ChoiceField serializer field."""
#
#     def __init__(self, choices, **kwargs):
#         """init."""
#         self._choices = OrderedDict(choices)
#         super(ChoiceDisplayField, self).__init__(**kwargs)
#
#     # 返回可读性良好的字符串而不是 1，-1 这样的数字
#     def to_representation(self, obj):
#         """Used while retrieving value for the field."""
#         return self._choices[obj]
#
#     def to_internal_value(self, data):
#         """Used while storing value for the field."""
#         for i in self._choices:
#             # 这样无论用户POST上来但是CHOICES的 Key 还是Value 都能被接受
#             if i == data or self._choices[i] == data:
#                 return i
#         raise serializers.ValidationError("Acceptable values are {0}.".format(list(self._choices.values())))
#
#
# class UserSerializer(serializers.ModelSerializer):
#     GENDERS = ((1, '男'), (2, '女'))
#     gender = ChoiceDisplayField(choices=GENDERS)  # 调用ChoiceDisplayField
#
#     class Meta:
#         model = User
#         fields = "__all__"





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {  # 额外字段,就是说你必须传参，但是不需要出参。额外字段：改变我们字段的修饰
            "pwd": {"write_only": True}  # write_only: True 表示只允许入参，不允许出参
        }
