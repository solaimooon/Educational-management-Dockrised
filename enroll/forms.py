from django.forms import ModelForm, Textarea
from django import forms
from enroll.models import *
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from formset.widgets import DualSelector
from athentication.models import *


class klass_form(forms.ModelForm):
        class Meta:
            model = klass
            fields = ['name', 'course', 'start_date', 'end_data', 'start_time', 'end_time','teacher','level','student']

            # blow widget for time picker
            widgets = {
            'start_time':forms.TimeInput(attrs={
            'type': 'time',  # HTML5 time input type
            'id': 'appt',  # id attribute for the time field
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',  # HTML5 time input type
                'id': 'appt',  # id attribute for the time field

            }),
            'student':forms.SelectMultiple(attrs={'required': False})
            }

    




        # override the init function of calss model form for date picker
        def __init__(self, *args, **kwargs):
            super(klass_form, self).__init__(*args, **kwargs)
            self.fields['start_date'] = JalaliDateField(  # date format is  "yyyy-mm-dd"
                                                widget=AdminJalaliDateWidget)  # optional, to use default datepicker
            self.fields['end_data'] = JalaliDateField(  # date format is  "yyyy-mm-dd"
                                                 widget=AdminJalaliDateWidget)  # optional, to use default datepicker
            self.fields['teacher']=forms.ModelChoiceField(label=None,
                queryset=User.objects.filter(is_staff=True),
                widget = forms.Select(attrs={'class': 'form-control select2'})
            )
            for field_name, field in self.fields.items():
                field.label = ''  # غیرفعال کردن نمایش label برای تمام فیلدها




class enroll_student_form(forms.Form):
    students = forms.models.ModelMultipleChoiceField(
        queryset=User.objects.filter(id__in=extra_user_data.objects.filter(type='Guest',age__isnull=False).values_list('forign_key')),
        widget=forms.SelectMultiple(attrs={'class': 'dual-list-box'})
    )

class report_according_to_data_and_course_form(forms.Form):
    date = forms.DateField()

    # استفاده از ModelChoiceField برای انتخاب دوره‌ها
    course = forms.ModelChoiceField(label=None,
        queryset=klass.objects.all().values_list('course').distinct(),  # بارگذاری گزینه‌ها از queryset
        empty_label="انتخاب کنید"  # برچسب پیش‌فرض
    )

    CHOICES = [
        ('present', 'حاضر '),
        ('absent_unwarranted', 'غایب'),

    ]
    type = forms.ChoiceField(choices=CHOICES,label=None)

    def __init__(self, *args, **kwargs):
        super(report_according_to_data_and_course_form, self).__init__(*args, **kwargs)
        self.fields['date'] = JalaliDateField(  # date format is "yyyy-mm-dd"
                                              widget=AdminJalaliDateWidget)
        for field_name, field in self.fields.items():
            field.label = ''  # غیرفعال کردن نمایش label برای تمام فیلدها                                      


"""class student_picker(forms.Form):
    student = forms.models.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=DualSelector(search_lookup='name__icontains')
    )"""