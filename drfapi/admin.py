# Register your models here.

from django.contrib import admin
from drfapi import models

admin.site.register(models.User)
admin.site.register(models.group)
admin.site.register(models.host_idc)
admin.site.register(models.host_manager)
admin.site.register(models.host_list)

