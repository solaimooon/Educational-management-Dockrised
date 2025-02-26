from email.mime import audio, image
from email.policy import default
from os import name
from tkinter.messagebox import QUESTION
from django.db import models

class compattions(models.Model):
    name=models.CharField(max_length=50)
    question=models.CharField(max_length=500)
    monasebat=models.CharField(max_length=50)
    link=models.URLField()
    image=models.ImageField( upload_to='compatitons/',null=True,default="NULL")
    audio_or_video=models.FileField(upload_to='compatitons/', max_length=100 ,null=True,default="NULL")
    def __str__(self):
        return self.name
# Create your models here.
