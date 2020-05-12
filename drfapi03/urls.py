#!/usr/bin/env python3
# _*_ coding:utf8 _*_
# __author__ = yanglc


from django.urls import path
from . import views

urlpatterns = [
    path("user/", views.user_list, name="user-list"),  # 编写drfapi03->urls.py => http://127.0.0.1:8000/api/user/
    path("user/<int:id>/",views.user_detail,name="user-detail"),   #传入 user id

]