from django.forms import ModelForm
from django import forms
from .models import *

class Sign_up_form(ModelForm):
    class Meta:
        model = User
        fields=['username','password']


class sign_in (forms.Form):
    username=forms.CharField(max_length=255)
    password=forms.CharField(max_length=255)
