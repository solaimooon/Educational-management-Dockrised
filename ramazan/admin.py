from django.contrib import admin
from .models import *

# Register your models here.
class type_emtiyaz_admin(admin.ModelAdmin):
    list_display=['name','max_point']

class Time_period_admin(admin.ModelAdmin):
    list_display=['name','image','date_shamsi','date_hejri']
    
class ramazan_point_amin(admin.ModelAdmin):
    list_display=['own_user','amount','type','create_at','Time_period','user_register'] 
       
admin.site.register(type_emtiyaz,type_emtiyaz_admin)
admin.site.register(Time_period,Time_period_admin)
admin.site.register(ramazan_point,ramazan_point_amin)

# Register your models here.
