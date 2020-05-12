from .serializers import ArticleSerializer,CategorySerializer,TagSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from .models import Article,Category,Tag
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


class JSONResponse(HttpResponse):
    """重新封装一下HttpResponse避免重复代码"""
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt #解决 post 提交数据  报错403 csrf_token验证问题
def article_list(request):
    """
    文章标题
    :return:
    """
    if request.method == "GET":
        arts = Article.objects.all()
        ser = ArticleSerializer(instance=arts, many=True,context={'request':request})  # 因为是多个对象实例，所以必须加上 many=true
        # JSONRenderer 已经帮你封装好了，所以下面两行代码注释
        # json_data = JSONRenderer().render(ser.data)
        # return HttpResponse(json_data, content="application/json", status=200)
        return JSONResponse(ser.data, status=200)
    elif request.method == "POST":
        data = JSONParser().parse(request)  # 把前端页面传递过来的数据转成 python识别的数据类型
        ser = ArticleSerializer(data=data,context={'request':request})  # 反序列化新增数据需要传入data

        if ser.is_valid():
            ser.save()
            return JSONResponse(ser.data, status=201)  # 状态码(status)到 RESTFul介绍中去找，里面有详细的说明
        return JSONResponse(ser.errors, status=400)






@csrf_exempt #解决 post 提交数据  报错403 csrf_token验证问题
def article_detail(request, id):  # 插入参数 id
    """
    文章详情
    :param request:
    :param id: 文章id
    :return:
    """
    try:
        art = Article.objects.get(id=id)  # 需要做异常处理，当不存在的时候
    except Article.DoesNotExist as e:
        return HttpResponse(status=404)

    if request.method == "GET":  # 获取单条数据
        ser = ArticleSerializer(instance=art,context={'request':request})  # instance 可以写也可以不写
        return JSONResponse(ser.data, status=200)

    elif request.method == "PUT":  # 全部更新
        data = JSONParser().parse(request)
        ser = ArticleSerializer(instance=art, data=data,context={'request':request})
        if ser.is_valid():
            ser.save()
            return JSONResponse(ser.data, status=201)
        return JSONResponse(ser.errors, status=400)
    elif request.method == "PATCH":  # 部分更新
        data = JSONParser().parse(request)
        ser = ArticleSerializer(instance=art, data=data, partial=True,context={'request':request})  # partial=True 意思是我要部分更新，默认是False
        if ser.is_valid():
            ser.save()
            return JSONResponse(ser.data, status=201)
        return JSONResponse(ser.errors, status=400)

    elif request.method == "DELETE":  # 删除
        art.delete()
        return HttpResponse(status=204)


@csrf_exempt
def category_list(request):
    """
    文章标题
    :return:
    """
    if request.method == "GET":
        arts = Category.objects.all()
        ser = CategorySerializer(instance=arts, many=True,context={'request':request})
        return JSONResponse(ser.data, status=200)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        ser = CategorySerializer(data=data,context={'request':request})
        if ser.is_valid():
            ser.save()
            return JSONResponse(ser.data, status=201)
        return JSONResponse(ser.errors,status=401)


@csrf_exempt
def category_detail(request,id):
    """
    文章详情
    :param request:
    :param id: 文章id
    :return:
    """
    try:
        art = Category.objects.get(id=id)
    except Category.DoesNotExist as e:
        return HttpResponse(status=404)

    if request.method == "GET":
        ser = CategorySerializer(instance=art, context={'request':request})
        return JSONResponse(ser.data,status=200)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        ser = CategorySerializer(instance=art, data=data, context={'request':request})
        if ser.is_valid():
            ser.save()
            return JSONResponse(ser.data,status=201)
        return JSONResponse(ser.errors,status=400)
    elif request.method == "PATCH":
        data = JSONParser().parse(request)
        ser = CategorySerializer(instance=art,data=data,partial=True,context={'request':request}) #partial=True 意思是我要部分更新，默认是False
        if ser.is_valid():
            ser.save()
            return JSONResponse(ser.data,status=201)
        return JSONResponse(ser.errors,status=400)

    elif request.method == "DELETE":
        art.delete()
        return HttpResponse(status=204)



@csrf_exempt
def tag_list(request):
    if request.method == "GET":
        arts = Tag.objects.all()
        ser = TagSerializer(instance=arts, many=True,context={'request':request})
        return JSONResponse(ser.data, status=200)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        ser = TagSerializer(data=data,many=True)
        if ser.is_valid():
            ser.save()
            return JSONResponse(ser.data, status=201)
        return JSONResponse(ser.errors,status=401)


@csrf_exempt
def tag_detail(request,id):
    try:
        art = Tag.objects.get(id=id)
    except Tag.DoesNotExist as e:
        return HttpResponse(status=404)

    if request.method == "GET":
        ser = TagSerializer(instance=art,context={'request':request})
        return JSONResponse(ser.data,status=200)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        ser = TagSerializer(instance=art,data=data,context={'request':request})
        if ser.is_valid():
            ser.save()
            return JSONResponse(ser.data,status=201)
        return JSONResponse(ser.errors,status=400)
    elif request.method == "PATCH":
        data = JSONParser().parse(request)
        ser = TagSerializer(instance=art,data=data,partial=True,context={'request':request})
        if ser.is_valid():
            ser.save()
            return JSONResponse(ser.data,status=201)
        return JSONResponse(ser.errors,status=400)

    elif request.method == "DELETE":
        art.delete()
        return HttpResponse(status=204)





