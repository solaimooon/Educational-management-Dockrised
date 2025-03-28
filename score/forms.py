from django import forms
from .models import *
from django.contrib.auth.models import User
from enroll.models import *


class presence_absence_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        klass_id = kwargs.pop('klass_id', None)
        super().__init__(*args, **kwargs)
        if klass_id is not None:
            self.fields['enroll'].queryset = link_table.objects.filter(klass_id=klass_id)
        for field_name, field in self.fields.items():
            field.label = ''  # غیرفعال کردن نمایش label برای تمام فیلدها    
        # Set the 'time' field to not required
        self.fields['time'].required = False
    class Meta:
        model = presence_absence
        fields = [ 'was_or_not_or','time', 'enroll']
        widgets = {
            'time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'id': 'appt',
                }
            )
        }


class pure_emtiyaz_and_ons_form(forms.Form):
    enroll = forms.ModelChoiceField(queryset=None)
    ons = forms.IntegerField(label=' انس ')

    def __init__(self, *args, **kwargs):
        klass_id = kwargs.pop('klass_id', None)  # Get klass_id from kwargs
        super().__init__(*args, **kwargs)
        if klass_id:
            self.fields['enroll'].queryset = link_table.objects.filter(klass_id=klass_id)
        else:
            self.fields[
                'enroll'].queryset = link_table.objects.none()  # Set an empty queryset if no klass_id is provided
        for field_name, field in self.fields.items():
            field.label = ''  # غیرفعال کردن نمایش label برای تمام فیلدها        


class basic_kosha_form(forms.Form):
    hozore_va_hamrahi = forms.IntegerField(min_value=0, max_value=30,required=False,label="")
    hefz_hadis = forms.IntegerField(min_value=0, max_value=20,required=False,label="" )
    estema_file_soty = forms.IntegerField(min_value=0, max_value=40,required=False,label="" )
    rang_amizi_daftar = forms.IntegerField(min_value=0, max_value=20,required=False,label="" )
    ravankhani = forms.IntegerField(min_value=0, max_value=60,required=False,label="")
    hegi = forms.IntegerField(min_value=0, max_value=20,required=False, label="")
    gheraat = forms.IntegerField(min_value=0, max_value=40,required=False,label="" )
    other = forms.IntegerField(min_value=0, max_value=20,required=False,label="")

class tajvid_kosha_form(forms.Form):
    hozore_va_hamrahi = forms.IntegerField(min_value=0, max_value=30, required=False,label="")
    hefz_hadis = forms.IntegerField(min_value=0, max_value=20, required=False,label="")
    estema_file_soty = forms.IntegerField(min_value=0, max_value=40, required=False,label="")
    rang_amizi_daftar = forms.IntegerField(min_value=0, max_value=20, required=False,label="")
    ravankhani = forms.IntegerField(min_value=0, max_value=60, required=False,label="")
    hegi = forms.IntegerField(min_value=0, max_value=20, required=False,label="")
    solve_question = forms.IntegerField(min_value=0, max_value=40, required=False,label="")
    other = forms.IntegerField(min_value=0, max_value=20, required=False,label="")

