from django.db import models

# Create your models here.

class group(models.Model):
    # gid = models.AutoField(primary_key=True)
    groupname = models.CharField(verbose_name='组名字', max_length=32)
    groupcreate_data = models.DateTimeField(verbose_name='组创建时间', auto_now_add=True, null=True)
    groupupdate_data = models.DateTimeField(verbose_name='组更新时间', auto_now_add=True, null=True)

class User(models.Model):
    # uid = models.AutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    email = models.EmailField(verbose_name='邮箱', max_length=32)
    gid = models.ForeignKey(to="group", on_delete=models.CASCADE)     #组和用户之间是 一对多关系




class host_idc(models.Model):
    # 自定义自增列
    # id = models.AutoField(primary_key=True)
    idcname = models.CharField(verbose_name='机房名字', max_length=64)
    idcagent = models.CharField(verbose_name='机房代理商', max_length=64)
    idcaddress = models.CharField(verbose_name='机房地址', max_length=64)



class host_manager(models.Model):
    # id = models.AutoField(primary_key=True)
    hostuser = models.CharField(verbose_name='登录账户', max_length=64)
    hostpasswd = models.CharField(verbose_name='登录密码', max_length=64)
    hostport = models.IntegerField(verbose_name='主机端口')


class host_list(models.Model):
    # id = models.AutoField(primary_key=True)
    hosttype = models.CharField(verbose_name='主机类型', max_length=64)
    hostname = models.CharField(verbose_name='主机名', max_length=64)
    hostip = models.GenericIPAddressField(verbose_name='ip', protocol="ipv4",db_index=True)
    hostconfig = models.CharField(verbose_name='主机配置', max_length=64)
    hostcreate_data = models.DateTimeField(verbose_name='主机创建时间', auto_now_add=True)
    hostupdate_data = models.DateTimeField(verbose_name='主机更新时间', auto_now_add=True)
    billing_idcid = models.ForeignKey(to="host_idc", on_delete=models.CASCADE)
    billing_managerid = models.ForeignKey(to="host_manager", on_delete=models.CASCADE)