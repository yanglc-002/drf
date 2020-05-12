#!/usr/bin/env python3
# _*_ coding:utf8 _*_
# __author__ = yanglc


from django.urls import path
from . import views

urlpatterns = [
    path("article/", views.article_list, name="article-list"),  # 编写drfapi02->urls.py => http://127.0.0.1:8000/api/article/
    path("article/<int:id>/",views.article_detail,name="article-detail"),   #传入 article id
    # 新增 category的路由
    path("category/", views.category_list, name="category-list"),
    path("category/<int:id>/", views.category_detail, name="category-detail"),
    # 新增 Tag的路由
    path("tag/", views.tag_list, name="tag-list"),
    path("tag/<int:id>/", views.tag_detail, name="tag-detail")
]