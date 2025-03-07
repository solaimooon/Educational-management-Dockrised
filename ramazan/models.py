from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User
class type_emtiyaz(models.Model):
    name=models.CharField(max_length=50)
    max_point=models.IntegerField()
    def __str__(self):
        return self.name
class Time_period(models.Model):
    name=models.CharField(max_length=50)
    image=models.ImageField( upload_to='ramazan_peried/',null=True,default='null')  
    date_shamsi=models.CharField(max_length=30,null=True,default='null')
    date_hejri=models.CharField(max_length=30,null=True,default='null')
class ramazan_point(models.Model):
    amount=models.IntegerField()
    type=models.ForeignKey(type_emtiyaz, on_delete=models.SET_NULL,null=True)
    create_at=jmodels.jDateTimeField(auto_now_add=True)
    Time_period=models.ForeignKey(Time_period, on_delete=models.CASCADE)
    own_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='own_user')
    user_register=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='user_register')

# view 

class ramazan_final(models.Model):
    rotbe = models.IntegerField(primary_key=True)
    total_amount=models.IntegerField()
    own_user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    Time_period_id=models.ForeignKey(Time_period,on_delete=models.DO_NOTHING,db_column="Time_period_id")
    period=models.CharField( max_length=50)
    class Meta:
        managed = False
        db_table = 'ramazan_final'

