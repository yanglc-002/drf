#!/usr/bin/env python3
# _*_ coding:utf8 _*_
# __author__ = yanglc


from rest_framework import serializers
from .models import Article,Category,Tag


# 普通序列化，很少用
'''
class ArticleSerializer(serializers.Serializer):  # 最普通的序列化类，需要对Article类的每一个字段都需要自己定义，定义的字段必须跟Article类一样
    id = serializers.IntegerField(read_only=True)  # id是Article类中自主生产的，而不是传过去的，所以我们定义为只读
    vum = serializers.IntegerField(required=True)
    content = serializers.CharField(max_length=1000)
    title = serializers.CharField(required=True, max_length=100)

    def create(self, validated_data):  # validated_data表示传递过来的数据
        return Article.objects.create(**validated_data)  # 保存数据

    def update(self, instance, validated_data):  # instance：传递过来的实例，就是 model实例，validated_data传递过来的数据，
        instance.title = validated_data.get('title', instance.title)  # instance:表示Article实例，validated_data传递过来的数据
        instance.vum = validated_data.get('vum', instance.vum)  # get('vum', instance.vum)：表示没有取到就用原来的值
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
'''
###################

#设计分类表(Category)(1对多)
'''
class  ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        # fields = ('id', 'title', 'vum', 'content')     #fields、exclude、fields 三者只能取一
        fields = ('id', 'title', 'vum', 'content', 'category')  # #增加 category 序列化外键

       #exclude = () 表示不返回字段
       #fields = '__all__': 表示所有字段(表示模型有什么字段，我们就显示什么字段)

       #read_only_fields = () #设置只读字段 不接受用户修改


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
#######################
'''

########
# StringRelatedField获取 model 模型类中Category类的 def __str__中返回的值(self.name)
'''
class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()  # modle模型Article中有category字段

    class Meta:
        model = Article
        fields = ("id", 'vum', 'content', 'title', 'category')  # 新增显示category字段。





class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')




class CategorySerializer(serializers.ModelSerializer):
    articles = serializers.StringRelatedField(many=True)  #因为查文章分类是多个对象，所以要加 many=True
    class Meta:
        model = Category
        fields = ('id', 'name', 'articles')  #article字段是在模型类Article中related_name中反射出来的
'''

#######PrimaryKeyRelatedField############
'''

class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)  # read_only=True 是必须传的，不然会报错

    class Meta:
        model = Article
        fields = ("id", 'vum', 'content', 'title', 'category')


class CategorySerializer(serializers.ModelSerializer):
    articles = serializers.PrimaryKeyRelatedField(read_only=True, many=True)  # 多个实例，一个分类下有多篇文章

    class Meta:
        model = Category
        fields = ('id', 'name', 'articles')
'''

#HyperlinkedRelatedField

'''
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
'''

#SlugRelatedField
'''
class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'  # 指定只返回模型类Category中的某个字段，这边我们返回name吧。
    )

    class Meta:
        model = Article
        fields = ("id", 'vum', 'content', 'title', 'category')


class CategorySerializer(serializers.ModelSerializer):
    articles = serializers.SlugRelatedField(
        read_only=True,
        slug_field='vum',  # 指定只返回模型类Article的vum字段
        many=True
    )

    class Meta:
        model = Category
        fields = ('id', 'name', 'articles')
'''

# HyperlinkedIdentityField
'''
class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.HyperlinkedIdentityField(
        view_name="drfapi02:category-detail",  # view_name是必须传的
        lookup_field='id'  # 默认是pk

    )

    class Meta:
        model = Article
        fields = ("id", 'vum', 'content', 'title', 'category')
        #fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    articles = serializers.HyperlinkedIdentityField(
        view_name="drfapi02:article-detail",
        lookup_field = 'id',
        many=True
    )

    class Meta:
        model = Category
        fields = ('id', 'name', 'articles')
        # fields = '__all__'

'''

# HyperlinkedModelSerializer
'''
class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"

        extra_kwargs = {
            'url': {'view_name': 'drfapi02:article-detail', 'lookup_field': 'id'},
            'category': {'view_name': 'drfapi02:category-detail', 'lookup_field': 'id'},
        }


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'articles', 'url')  # url字段自己添加

        extra_kwargs = {
            'url': {'view_name': 'drfapi02:category-detail', 'lookup_field': 'id'},
            'articles': {'view_name': 'drfapi02:article-detail', 'lookup_field': 'id'},
        }
        
'''


# 序列化嵌套
'''
class ArticleSerializer(serializers.ModelSerializer):
    # category = CategorySerializer() 这边不能嵌套CategorySerializer()，会报CategorySerializer没有定义错误
    class Meta:
        model = Article
        fields = ("id", 'vum', 'content', 'title', 'category')


class CategorySerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True)  # 所以只能这边嵌套序列化关系

    class Meta:
        model = Category
        fields = ('id', 'name', 'articles')  # articles先通过文章模型(Article类)去找文章序列化，系列化哪些字段，这边是全局字段
'''


# 序列化嵌套
'''
class ArticleSerializer(serializers.ModelSerializer):


    class Meta:
        model = Article
        fields = ("id", 'vum', 'content', 'title', 'category')
        depth = 2  # 表示深度查找2层

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'articles')



### SerializerMethodField


class CategorySerializer(serializers.ModelSerializer):
    # articles = ArticleSerializer(many=True)
    count = serializers.SerializerMethodField()  # 自定义序列化方法字段count

    class Meta:
        model = Category
        fields = '__all__'  # 加上count字段

    def get_count(self, obj):  # obj指得是model模型Category类对象
        return obj.articles.count()  # articles反查的字段
'''

###source
'''
class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")  # 数据来源是Category类中的name值

    class Meta:
        model = Article
        fields = ("id", 'vum', 'content', 'title', 'category')


# class CategorySerializer(serializers.ModelSerializer):
#     # articles = ArticleSerializer(many=True)
#     count = serializers.SerializerMethodField()  # 自定义序列化方法字段count
#
#     class Meta:
#         model = Category
#         fields = '__all__'  # 加上count字段
#
#     def get_count(self, obj):  # obj指得是model模型Category类对象
#         return obj.articles.count()  # articles反查的字段

class CategorySerializer(serializers.ModelSerializer):
    arts = serializers.CharField(source="articles.all") # related反查的情况下用articles.all
    #arts = serializers.CharField(source="articles_set.all") #没有related反查的情况下用articles_set.all
    class Meta:
        model = Category
        fields = ('id','name','articles','arts')  #添加arts字段
'''
'''
class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")  # 数据来源是Category类中的name值

    class Meta:
        model = Article
        fields = ("id", 'vum', 'content', 'title', 'category')


class MyCharField(serializers.CharField):
    def to_representation(self, value):  #value 就是 articles.all中所有的值
        data_list = []
        for row in value:
            data_list.append({'title': row.title, 'content': row.content})
        return data_list  #必须要有返回值


class CategorySerializer(serializers.ModelSerializer):
    arts = MyCharField(source="articles.all")  #MyCharField需要跟上面自定义的一样
    class Meta:
        model = Category
        fields = ('id','name','articles','arts')  #添加arts字段

#利用source实现可读可写
from collections import OrderedDict


class ChoiceDisplayField(serializers.Field):
    """Custom ChoiceField serializer field."""

    def __init__(self, choices, **kwargs):
        """init."""
        self._choices = OrderedDict(choices)
        super(ChoiceDisplayField, self).__init__(**kwargs)

    # 返回可读性良好的字符串而不是 1，-1 这样的数字
    def to_representation(self, obj):
        """Used while retrieving value for the field."""
        return self._choices[obj]

    def to_internal_value(self, data):
        """Used while storing value for the field."""
        for i in self._choices:
            # 这样无论用户POST上来但是CHOICES的 Key 还是Value 都能被接受
            if i == data or self._choices[i] == data:
                return i
        raise serializers.ValidationError("Acceptable values are {0}.".format(list(self._choices.values())))
'''


# to_representation方法

# class ArticleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         fields = ("id", 'vum', 'content', 'title', 'category', 'tags')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("id", 'vum', 'content', 'title', 'category', 'tags')
        depth = 2 #深度显示，只支持序列化(get)，不支持反序列化(post、patch、put)



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'articles')


class TagSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  #重写时间展示
    class Meta:
        model = Tag
        fields = ('id', 'name', 'create_time')



