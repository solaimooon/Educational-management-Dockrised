from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from enroll.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from enroll.models import *

class presence_absence(models.Model):
    was_or_not= (
        ('present', 'حاضر'),
        ('absent_unwarranted', 'غایب/غیر موجه'),
        ('absent_warranted', 'غایب/موجه')
    )
    enroll=models.ForeignKey(link_table,on_delete=models.CASCADE)
    was_or_not_or = models.CharField(choices=was_or_not, max_length=50)
    time=models.TimeField(null=True)
    date=jmodels.jDateField()


class score (models.Model):
    method=(
        ('kosha_ravankhani','kosha_ravankhani'),
        ('kosha_tajvid','kosha_tajvid'),
        ('noramal','noramal')
    )
    enroll=models.ForeignKey(link_table,on_delete=models.CASCADE)
    date_for=jmodels.jDateField()
    creat_at=models.DateField(auto_now_add=True,null=True)
    method=models.CharField(choices=method,max_length=50)
    ons=models.PositiveIntegerField(null=True)


class type(models.Model):
    name=models.CharField(max_length=50)
    avalable=models.IntegerField()

    def __str__(self):
        return self.name


class amount(models.Model):
    score=models.ForeignKey(score,on_delete=models.CASCADE)
    number=models.IntegerField()
    type=models.ForeignKey(type,on_delete=models.SET_NULL,null=True)


# define views sum_final and each session.
class sum_emtiyazat(models.Model):
    id = models.BigIntegerField(primary_key=True)
    score=models.ForeignKey(score,on_delete=models.DO_NOTHING)
    enroll=models.ForeignKey(link_table,on_delete=models.DO_NOTHING)
    date_for=jmodels.jDateField()
    sumed_emtiyaz=models.DecimalField(max_digits=10,decimal_places=2)
    class Meta:
        managed = False
        db_table = 'sum_emtiyazat_for_each_day'

class SUM_final(models.Model):
    enroll=models.ForeignKey(link_table,on_delete=models.DO_NOTHING)
    SUM=models.DecimalField(max_digits=10,decimal_places=2)
    class Meta:
        managed=False
        db_table='SUM_final'

@receiver(post_save, sender=presence_absence)
def my_handler(sender, instance, created, **kwargs):
    key = '78634F47647561304B41467244444B344B7172625A73766939754C5644654376777A44726D6E6476517A383D'
    if created:
        if instance.was_or_not_or == 'absent_unwarranted' :
            print("sms sent")
            enroll_id=instance.enroll.id
            enroll_object=link_table.objects.get(id=enroll_id)
            student_id=enroll_object.student_id_id
            student_object=User.objects.get(id=student_id)
            phone_number=student_object.username
            print(str(phone_number))
            first_name=str(student_object.first_name)
            last_name=str(student_object.last_name)
            full_name=first_name+" "+last_name
            print(str(full_name))
            date=instance.date
            print("gfsdgfdgsdfg",date)
            klass_name=enroll_object.klass_id.level
            print(klass_name)
            # this is the api of cavenegar , pass the key to url
            api = 'https://api.kavenegar.com/v1/%s/verify/lookup.json' % key
            paloyd = {'receptor': str(phone_number), 'token': str(date),'token20':str(full_name),"token10":str(klass_name), "template": "absent"}
            response = requests.post(api, data=paloyd)
            print("response detail sms",response.text)
            
        