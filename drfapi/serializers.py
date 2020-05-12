#!/usr/bin/env python3
# _*_ coding:utf8 _*_
# __author__ = yanglc

from rest_framework.serializers import HyperlinkedModelSerializer

from .models import User, group    ##也可以写“*“代表导入所有表

from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):  # HyperlinkedModelSerializer 用的是超链接的序列化
    class Meta:
        model = User  # 需要序列化类
        fields = ('id', 'username', 'password', 'email', 'gid')  # 需要序列化的属性，属性是在 序列化类中的，这里就是User中的字段，gid是外键，一样可以加。


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = group
        fields = ('id', 'groupname')



