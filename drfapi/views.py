from django.shortcuts import render
from .models import  User,group #导入模型
from rest_framework import viewsets
from .serializers import UserSerializer,GroupSerializer #导入序列化类


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):  # ModelViewSet是最终版，这边我们先认识一下
    queryset = User.objects.all()  # 告诉我们序列化哪些数据，这边就是说吧查出来的用户信息先给我序列化掉
    serializer_class = UserSerializer  # 告诉人家序列化哪个模型类


class GroupViewSet(viewsets.ModelViewSet):
    queryset = group.objects.all()  # 需要序列化的数据
    serializer_class = GroupSerializer  # 要哪个序列化类