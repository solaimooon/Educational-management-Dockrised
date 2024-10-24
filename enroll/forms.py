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
            self.fields['start_date'] = JalaliDateField(label=('تاریخ شورع کلاس'),  # date format is  "yyyy-mm-dd"
                                                widget=AdminJalaliDateWidget)  # optional, to use default datepicker
            self.fields['end_data'] = JalaliDateField(label=('تاریخ پایان کلاس'),  # date format is  "yyyy-mm-dd"
                                                 widget=AdminJalaliDateWidget)  # optional, to use default datepicker
            self.fields['teacher']=forms.ModelChoiceField(
                queryset=User.objects.filter(is_staff=True),
                widget = forms.Select(attrs={'class': 'form-control select2'})
            )




class enroll_student_form(forms.Form):
    students = forms.models.ModelMultipleChoiceField(
        queryset=User.objects.filter(id__in=extra_user_data.objects.filter(type='Guest',age__isnull=False).values_list('forign_key')),
        widget=forms.SelectMultiple(attrs={'class': 'dual-list-box'})
    )

class report_according_to_data_and_course_form(forms.Form):
    date = forms.DateField()

    # استفاده از ModelChoiceField برای انتخاب دوره‌ها
    course = forms.ModelChoiceField(
        queryset=klass.objects.all().values_list('course').distinct(),  # بارگذاری گزینه‌ها از queryset
        empty_label="انتخاب کنید"  # برچسب پیش‌فرض
    )

    CHOICES = [
        ('present', 'حاضر '),
        ('absent_unwarranted', 'غایب'),

    ]
    type = forms.ChoiceField(choices=CHOICES)

    def __init__(self, *args, **kwargs):
        super(report_according_to_data_and_course_form, self).__init__(*args, **kwargs)
        self.fields['date'] = JalaliDateField(label=('تاریخ'),  # date format is "yyyy-mm-dd"
                                              widget=AdminJalaliDateWidget)


"""class student_picker(forms.Form):
    student = forms.models.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=DualSelector(search_lookup='name__icontains')
    )"""