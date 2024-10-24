from django.shortcuts import render
import re
from django.shortcuts import redirect
from .forms import *
from .models import *
from score.models import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
@login_required(login_url='/athentication/')
def enroll_choose(request):
    return render(request,'enroll/choose_enroll_or_edit.html')

@login_required(login_url='/athentication/')
def create_class_view(request):
    if request.method=='GET':
        # creat the pure form of kalss info and enroll student
        kalss_form_object=klass_form()
        student_picker_object=enroll_student_form()
        return render(request,"enroll/create_class.html",{"klass_form_object":kalss_form_object,"student_picker_object":student_picker_object})
        # save form
    else:
        kalss_form_object = klass_form(request.POST)
        if kalss_form_object.is_valid():
            klass_object=kalss_form_object.save()
            students = request.POST.getlist('students')
            print(":دانش اموزان", students)
            klass_object.student.set(students)
            messages.add_message(request,messages.SUCCESS,"کلاس با موفقیت ایجاد شد")
            return HttpResponseRedirect(reverse('enroll:create_class'))
        else:
            for field, errors in kalss_form_object.errors.items():
                # نمایش خطای مربوط به هر فیلد
                for error in errors:
                    # ارسال خطا به پیام‌ها
                    messages.error(request, f'خطا در فیلد {field}: {error}')
            return HttpResponseRedirect(reverse('enroll:create_class'))



#show class for teather in own dashbord
@login_required(login_url='/athentication/')
def my_class_oprator_view(request):
    klass_object=klass.objects.filter(teacher=request.user.id).order_by('-course')
    return render(request,'enroll/my_class.html',{"klass_object":klass_object})


#show class for student in own dashbord
@login_required(login_url='/athentication/')
def my_class_student_view(request):
    enroll_objects=link_table.objects.filter(student_id=request.user.id)
    return render(request,'enroll/my_class_student.html',{"enroll_objects":enroll_objects})

# report generaly to studnet
@login_required(login_url='/athentication/')
def report_general_student_view(request,id_enroll):
    # if user donat have any score so the dont have any record in sum_final
    try:
        # sum of emtiyazat
        sum_emtiyaz_for_all_session=get_object_or_404(SUM_final,enroll=id_enroll)
        # colculate the rank
        all_object_of_sum=SUM_final.objects.all().order_by('SUM')
        counter=1
        for object in all_object_of_sum:
            if object==sum_emtiyaz_for_all_session:
                break
            else:
                counter+=1
        #end calculate
        return render(request,'enroll/report.html',{"sum_emtiyaz_for_all_session":sum_emtiyaz_for_all_session,"rank":counter})
    except:
        messages.add_message(request, messages.INFO, "گزارشی برای شما تاکنون ثبت نشده است")
        return HttpResponseRedirect(reverse("enroll:my_class_student"))





# report point student
@login_required(login_url='/athentication/')
def report_point_detail_view(request):
    pass


def all_class_to_edit_view(request):
    klass_objects=klass.objects.all()
    return render(request,'enroll/all_class.html',{"klass_objects":klass_objects})


def edit_class_detail_view(request,id):
    if request.method=='GET':
        object_class=klass.objects.filter(id=id)[0]
        form_edit_class_object=klass_form(instance=object_class)
        return render(request,'enroll/edit_class.html',{"form_edit_class_object":form_edit_class_object})
    elif request.method == 'POST':
        object_class = klass.objects.filter(id=id)[0]
        form_edit_class_object = klass_form(request.POST,instance=object_class)
        if form_edit_class_object.is_valid():
            form_edit_class_object.save()
            messages.add_message(request,messages.SUCCESS, "اطلاعات با موفقیت ثبت شد")
            return HttpResponseRedirect(reverse("enroll:edit_class"))
        else:
            for field, errors in form_edit_class_object.errors.items():
                # نمایش خطای مربوط به هر فیلد
                for error in errors:
                    # ارسال خطا به پیام‌ها
                    messages.error(request, f'خطا در فیلد {field}: {error}')
            return HttpResponseRedirect(reverse("enroll:edit_class"))
    else:
        klass.objects.get(id=id).delete()
        messages.add_message(request, messages.SUCCESS, "با موفقیت حذف شد")
        print("حذف")
        return HttpResponseRedirect(reverse("enroll:edit_class"))



def report_present_or_absent_according_to_course_date_view(request):
    if request.method=='GET':
        report_according_to_data_and_course_form_object=report_according_to_data_and_course_form()
        return render(request,'enroll/present_absent_report_acording_to_date.html',{"form":report_according_to_data_and_course_form_object})

    else:
        try:
            date=request.POST.get("date")
            course=request.POST.get("course")
            type=request.POST.get("type")
            my_string = course
            # استخراج عدد با استفاده از regex
            number = re.findall(r'\d+', my_string)

            # تبدیل لیست به عدد صحیح
            if number:
                course = int(number[0])
            klass_objects=klass.objects.filter(course=course)
            enroll_objects=link_table.objects.filter(klass_id__in=klass_objects)
            if type=='present':
                presents_or_absent_object=presence_absence.objects.filter(date=date,enroll__in=enroll_objects,was_or_not_or='present')
                report_according_to_data_and_course_form_object = report_according_to_data_and_course_form(initial={'date':date,"course":course,"type":type})
                counter = presents_or_absent_object.count()
                return render(request, 'enroll/present_absent_report_acording_to_date.html',
                              {"presents_or_absent_object": presents_or_absent_object,"form":report_according_to_data_and_course_form_object,"counter":counter})

            else:
                presents_or_absent_object = presence_absence.objects.filter(Q(date=date, enroll__in=enroll_objects,
                                                                            was_or_not_or='absent_unwarranted') |Q(date=date, enroll__in=enroll_objects,
                                                                            was_or_not_or='absent_warranted'))
                counter=presents_or_absent_object.count()
                report_according_to_data_and_course_form_object = report_according_to_data_and_course_form(initial={'date':date,"course":course,"type":type})
                return render(request,'enroll/present_absent_report_acording_to_date.html',{"presents_or_absent_object":presents_or_absent_object,"form":report_according_to_data_and_course_form_object,"counter":counter})
        except:
            messages.add_message(request,messages.ERROR,"لطفا مقادیر رو به درستی وارد نمایید")
            return HttpResponseRedirect(reverse('enroll:report_present_or_absent_date'))
