from django.db import models

# Create your models here.



class Article(models.Model):
    title = models.CharField(verbose_name='标题', max_length=100)
    vum = models.IntegerField(verbose_name='浏览量')
    content = models.TextField(verbose_name='内容')
    category = models.ForeignKey(to="Category",on_delete=models.CASCADE,related_name="articles")  #related_name反查
    tags = models.ManyToManyField(to="Tag", related_name="articles")  # related_name反查

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(verbose_name="分类", max_length=10)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(verbose_name="标签名字", max_length=10)
    create_time = models.DateTimeField()

    def __str__(self):
        return self.name