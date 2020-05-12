from django.contrib import admin

# Register your models here.
from drfapi02 import models

admin.site.register(models.Article)
admin.site.register(models.Category)
