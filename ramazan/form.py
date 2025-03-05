from django.forms import ModelForm
from django import forms
from .models import *

class ramazan_point_register(ModelForm):
    class Meta:
        model = ramazan_point
        fields = ['amount', 'type']
        widgets = {
        'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        'type': forms.Select(attrs={'class': 'form-control'})  
}
