#!/usr/bin/env python3
# _*_ coding:utf8 _*_
# __author__ = yanglc


from rest_framework import serializers
from .models import Article,Category


# 普通序列化，很少用
# class ArticleSerializer(serializers.Serializer):  # 最普通的序列化类，需要对Article类的每一个字段都需要自己定义，定义的字段必须跟Article类一样
#     id = serializers.IntegerField(read_only=True)  # id是Article类中自主生产的，而不是传过去的，所以我们定义为只读
#     vum = serializers.IntegerField(required=True)
#     content = serializers.CharField(max_length=1000)
#     title = serializers.CharField(required=True, max_length=100)
#
#     def create(self, validated_data):  # validated_data表示传递过来的数据
#         return Article.objects.create(**validated_data)  # 保存数据
#
#     def update(self, instance, validated_data):  # instance：传递过来的实例，就是 model实例，validated_data传递过来的数据，
#         instance.title = validated_data.get('title', instance.title)  # instance:表示Article实例，validated_data传递过来的数据
#         instance.vum = validated_data.get('vum', instance.vum)  # get('vum', instance.vum)：表示没有取到就用原来的值
#         instance.content = validated_data.get('content', instance.content)
#         instance.save()
#         return instance

###################

#设计分类表(Category)(1对多)
# class  ArticleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         # fields = ('id', 'title', 'vum', 'content')     #fields、exclude、fields 三者只能取一
#         fields = ('id', 'title', 'vum', 'content', 'category')  # #增加 category 序列化外键
#
#        #exclude = () 表示不返回字段
#        #fields = '__all__': 表示所有字段(表示模型有什么字段，我们就显示什么字段)
#
#        #read_only_fields = () #设置只读字段 不接受用户修改
#
#
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('id', 'name')
########################


########
# StringRelatedField获取 model 模型类中Category类的 def __str__中返回的值(self.name)

# class ArticleSerializer(serializers.ModelSerializer):
#     category = serializers.StringRelatedField()  # modle模型Article中有category字段
#
#     class Meta:
#         model = Article
#         fields = ("id", 'vum', 'content', 'title', 'category')  # 新增显示category字段。





# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('id', 'name')




# class CategorySerializer(serializers.ModelSerializer):
#     articles = serializers.StringRelatedField(many=True)  #因为查文章分类是多个对象，所以要加 many=True
#     class Meta:
#         model = Category
#         fields = ('id', 'name', 'articles')  #article字段是在模型类Article中related_name中反射出来的


#######PrimaryKeyRelatedField############


# class ArticleSerializer(serializers.ModelSerializer):
#     category = serializers.PrimaryKeyRelatedField(read_only=True)  # read_only=True 是必须传的，不然会报错
#
#     class Meta:
#         model = Article
#         fields = ("id", 'vum', 'content', 'title', 'category')
#
#
# class CategorySerializer(serializers.ModelSerializer):
#     articles = serializers.PrimaryKeyRelatedField(read_only=True, many=True)  # 多个实例，一个分类下有多篇文章
#
#     class Meta:
#         model = Category
#         fields = ('id', 'name', 'articles')


#HyperlinkedRelatedField


class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.HyperlinkedRelatedField(
        view_name='drfapi02:category-detail',  # urls路由的别名
        lookup_field='id',  # 数据库字段的名字,这个字段到数据库中去找
        read_only=True
    )

    class Meta:
        model = Article
        fields = ("id", 'vum', 'content', 'title', 'category')


class CategorySerializer(serializers.ModelSerializer):
    articles = serializers.HyperlinkedRelatedField(
        view_name='drfapi02:article-detail',
        lookup_field="id",
        many=True,
        read_only=True
    )

    class Meta:
        model = Category
        fields = ('id', 'name', 'articles')


#