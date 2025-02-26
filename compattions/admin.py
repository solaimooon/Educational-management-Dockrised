from django.contrib import admin
from .models import *

# Register your models here.
class compattions_admin(admin.ModelAdmin):
    list_display=['name','monasebat']

admin.site.register(compattions,compattions_admin)

