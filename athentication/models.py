from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib import messages

# change the name of user instanse for show the full name of teacher in kalss form creation
def get_full_name(self):
    return "{} {}".format(self.first_name, self.last_name)


User.add_to_class("__str__", get_full_name)

type = (
    ('operator','اوپراتور'),
    ('teacher','معلم'),
    ('student','دانش اموز'),
    ('Guest',"مهمان")
)

class extra_user_data(models.Model):

    sex_choice = (
        ('male', 'مرد'),
        ('female', 'زن')
    )
    age=jmodels.jDateField(blank=True,null=True,verbose_name='سن')
    adress=models.CharField(blank=True,null=True,max_length=500,verbose_name='ادرس')
    #type of user for ristricing
    type =models.CharField(blank=True,null=True,max_length=50, choices=type,default="Guest")
    meli_cood = models.CharField(blank=True,null=True,max_length=50, verbose_name="کد ملی")
    sex = models.CharField(blank=True,null=True,max_length=50, choices=sex_choice,default='male')
    forign_key = models.ForeignKey(User, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='personality_picture/',default="personality_picture/boy.png")




class phone(models.Model):
    phone_owner = (
        ('itself', 'شخصی'),
        ('father', 'پدر'),
        ('mather', 'مادر'),
    )
    phone_number=models.CharField(max_length=50,blank=True,verbose_name='شماره تلفن ')
    owner = models.CharField(max_length=6, choices=phone_owner,blank=True, verbose_name='مالکیت')
    forign_key = models.ForeignKey(User, on_delete=models.CASCADE,)

