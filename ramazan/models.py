from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User
class type_emtiyaz(models.Model):
    name=models.CharField(max_length=50)
    max_point=models.IntegerField()
class Time_period(models.Model):
    name=models.CharField(max_length=50)
    image=models.ImageField( upload_to='ramazan_peried/',null=True,default='null')  
    date_shamsi=models.CharField(max_length=30,null=True,default='null')
    date_hejri=models.CharField(max_length=30,null=True,default='null')
class ramazan_point(models.Model):
    amount=models.IntegerField()
    type=models.ForeignKey(type_emtiyaz, on_delete=models.SET_NULL,null=True)
    create_at=jmodels.jDateTimeField()
    Time_period=models.ForeignKey(Time_period, on_delete=models.CASCADE)
    own_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='own_user')
    user_register=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='user_register')

# Create your models here.
