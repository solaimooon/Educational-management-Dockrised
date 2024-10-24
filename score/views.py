from django.shortcuts import render
from datetime import datetime
from datetime import timedelta
from enroll.models import *
from .forms import *
from .models import *
import urllib
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import jdatetime
import re
# massage framwork
from django.contrib import messages
from django.shortcuts import redirect

@login_required(login_url='/athentication/')
def choose_date_view(request,id):
    # get the klass_id and save to session
    request.session["klass_id"]=request.GET.get("klass_id")
    # get the class object
    class_object=klass.objects.filter(id=id)[0]
    start_date=str(class_object.start_date)
    end_data=str(class_object.end_data)
    # create the datetime object
    date=datetime.strptime(start_date, "%Y-%m-%d")
    end_data=datetime.strptime(end_data, "%Y-%m-%d")
    list_date=[]
    while date<=end_data:
        # append the time to list and slice datetiem object form time
        list_date.append(str(date)[0:11])
        date=date + timedelta(days=7)
    # create sessoin "enroll"
    request.session["enroll"] = "هنوز حضوری ثبت نکرده اید"
    return render(request,'score/choose_date.html',{"dates":list_date})

# save the hozore and score
@login_required(login_url='/athentication/')
def post_score_view(request,id=None):
    # (GET method)show the form
    if request.method == 'GET':
        # get the date whene clik date
        date_temp = request.GET.get('date')
        if date_temp!=None:
            global date
            date=date_temp
        try:
            # convert sting date to jdate object
            date=date.split("-")
            date=jdatetime.date(int(date[0]),int(date[1]),int(date[2]))
        finally:
            # creat presence_absence object with apropriate enroll choose
            # show the class.student(enroll) to choose
            presence_absence_form_object=presence_absence_form(klass_id=request.session["klass_id"])
            # get the class object
            klass_object=klass.objects.filter(pk=request.session["klass_id"])[0]
            # creat pure emtiyaz form
            pure_emtiyaz_and_form_object = pure_emtiyaz_and_ons_form(klass_id=request.session["klass_id"])
            # show the basic_kosha_form
            if klass_object.level.name in ["روانخوانی متوسط","روانخوانی پایه","روانخوانی خوب"]:
                # get emtiyazat that saved before
                # call the retrive_score_saved
                list_of_scores = retrive_score_saved(request, date)
                print(list_of_scores)
                # get absent or present saved before
                # call retirve present function
                presents_objects=retrive_present_or_absent(request)
                basic_kosha_form_object=basic_kosha_form()
                return render(request,'score/basic_form_score.html',{"basic_kosha_form_object":basic_kosha_form_object,"presence_absence_form_object":presence_absence_form_object,"pure_emtiyaz_and_form_object":pure_emtiyaz_and_form_object,"list_of_scores":list_of_scores,"presents_objects":presents_objects})
            # show the tajvid form
            elif klass_object.level.name in["تجوید 1/1","تجوید1/2","تجوید2/1","تجوید2/2","تجوید3/1","تجوید3/2","تجوید4/1","تجوید4/2"]:
                # get emtiyazat that saved before
                # call the retrive_score_saved
                list_of_scores = retrive_score_saved(request, date)
                print(list_of_scores)
                # get absent or present saved before
                # call retirve present function
                presents_objects = retrive_present_or_absent(request)
                # create the tajvid form
                tajvid_kosha_form_object=tajvid_kosha_form()
                return render(request,'score/basic_form_score.html',{"tajvid_kosha_form_object":tajvid_kosha_form_object,"presence_absence_form_object":presence_absence_form_object,"pure_emtiyaz_and_form_object":pure_emtiyaz_and_form_object,"list_of_scores":list_of_scores,"presents_objects":presents_objects})
            else:
                # get absent or present saved before
                # call retirve present function
                presents_objects = retrive_present_or_absent(request)
                return render(request, 'score/basic_form_score.html',
                              {
                               "presence_absence_form_object": presence_absence_form_object,
                               "pure_emtiyaz_and_form_object": pure_emtiyaz_and_form_object,
                                 "presents_objects": presents_objects})
    # (POST method) creat new present and score object
    elif request.method == "POST":
        # creat presence object if "was" field in post request
        if "was_or_not_or" in request.POST:
            presence_absence_form_object = presence_absence_form(request.POST)
            # validation
            if presence_absence_form_object.is_valid():
                presence_absence.objects.create(
                    date=date,
                    time=presence_absence_form_object.cleaned_data['time'],
                    was_or_not_or=presence_absence_form_object.cleaned_data['was_or_not_or'],
                    enroll=presence_absence_form_object.cleaned_data['enroll']
                )
                request.session["enroll"]=presence_absence_form_object.cleaned_data['enroll'].id
                messages.add_message(request,messages.SUCCESS,"با موفقیت ثبت شد")
                return HttpResponseRedirect(reverse("score:post_score"))
            else:
                for field, errors in presence_absence_form_object.errors.items():
                    # نمایش خطای مربوط به هر فیلد
                    for error in errors:
                        # ارسال خطا به پیام‌ها
                        messages.error(request, f'خطا در فیلد {field}: {error}')
                return HttpResponseRedirect(reverse("score:post_score"))
        # creat score object for ravankhani
        elif "gheraat" in request.POST:
            # save score object
            new_score_pure_object = score.objects.create(enroll=link_table.objects.get(pk=request.POST.get('enroll')),
                                                         method='kosha_ravankhani', ons=request.POST.get('ons'),
                                                         date_for=date)
            basic_kosha_form_object = basic_kosha_form(request.POST)
            if basic_kosha_form_object.is_bound:
                if basic_kosha_form_object.is_valid():
                    print(basic_kosha_form_object.data.dict())
                    for name_field, amount_temp in basic_kosha_form_object.cleaned_data.items():
                        if amount_temp == None:
                            continue
                        new_score_amount_object = amount()
                        new_score_amount_object.score = new_score_pure_object
                        new_score_amount_object.number = amount_temp
                        new_score_amount_object.type = type.objects.filter(name=name_field)[0]
                        print("number", new_score_amount_object.number)
                        print("type", new_score_amount_object.type)
                        new_score_amount_object.save()
                    messages.add_message(request,messages.SUCCESS,"با موفقیت ثبت شد ")
                    return HttpResponseRedirect(reverse("score:post_score"))
                else:
                    for field, errors in basic_kosha_form_object.errors.items():
                        # نمایش خطای مربوط به هر فیلد
                        for error in errors:
                            # ارسال خطا به پیام‌ها
                            messages.error(request, f'خطا در فیلد {field}: {error}')
                    return HttpResponseRedirect(reverse("score:post_score"))
        # creat score object for tajvid
        else:
            # save score object
            new_score_pure_object = score.objects.create(enroll=link_table.objects.get(pk=request.POST.get('enroll')),
                                                         method='kosha_tajvid', ons=request.POST.get('ons'),
                                                         date_for=date)
            tajvid_kosha_form_object = tajvid_kosha_form(request.POST)
            if tajvid_kosha_form_object.is_valid():
                    print(tajvid_kosha_form_object.data.dict())
                    for name_field, amount_temp in tajvid_kosha_form_object.cleaned_data.items():
                        if amount_temp == None:
                            continue
                        new_score_amount_object = amount()
                        new_score_amount_object.score = new_score_pure_object
                        new_score_amount_object.number = amount_temp
                        new_score_amount_object.type = type.objects.filter(name=name_field)[0]
                        print("number", new_score_amount_object.number)
                        print("type", new_score_amount_object.type)
                        new_score_amount_object.save()
                    messages.add_message(request,messages.SUCCESS,'با موفقیت ثبت شد')
                    return HttpResponseRedirect(reverse("score:post_score"))
            else:
                for field, errors in tajvid_kosha_form_object.errors.items():
                    # نمایش خطای مربوط به هر فیلد
                    for error in errors:
                        # ارسال خطا به پیام‌ها
                        messages.error(request, f'خطا در فیلد {field}: {error}')
                return HttpResponseRedirect(reverse("score:post_score"))

# delete the scores
def delete_csore_view(request,id):
    if request.method == 'POST':
        print("delete:",id)
        score.objects.filter(id=id).delete()
        return HttpResponseRedirect(reverse("score:post_score"))


# delete present object
def delete_present_view(request,id):
    if request.method == 'POST':
        print("delete:",id)
        presence_absence.objects.filter(id=id).delete()
        return HttpResponseRedirect(reverse("score:post_score"))




# function , not view
def retrive_score_saved(request,date):
    enrolls = link_table.objects.filter(klass_id=request.session.get("klass_id"))
    scores = score.objects.filter(enroll_id__in=enrolls, date_for=date)
    amounts = amount.objects.filter(score_id__in=scores).order_by("score_id")

    print("amounts", amounts)

    # Initialize lists
    second_list = []
    first_list = []

    # Loop through amounts
    for idx, amont in enumerate(amounts):
        if idx == 0:  # For the first record
            first_list.append(amont)
            current_score_id = amont.score_id
        else:
            if amont.score_id == current_score_id:  # Same score_id
                first_list.append(amont)
            else:  # Different score_id, add the current list to second_list
                second_list.append(first_list)
                first_list = [amont]  # Reset first_list with the new amount
                current_score_id = amont.score_id
    # Don't forget to add the last grouped amounts
    if first_list:
        second_list.append(first_list)
    return second_list


def retrive_present_or_absent(request):
    enrolls = link_table.objects.filter(klass_id=request.session.get("klass_id"))
    present_object=presence_absence.objects.filter(enroll__in=enrolls,date=date)
    return present_object

# report score for operator Categorize by course
def report_sumed_score_for_operator_view(request):
    # retrive the distinct course
    course=klass.objects.all().values_list('course').distinct()
    print((course))
    # remove extra section from course ,example:(,39)
    course_list=[]
    for x in course:
        course_list.append(x[0])
    print(course_list)
    dict_course_sumeds={}
    for x in course_list:
        klass_object=klass.objects.filter(course=x)
        enroll_object=link_table.objects.filter(klass_id__in=klass_object)
        points_objects=SUM_final.objects.filter(enroll__in=enroll_object).order_by('SUM')
        dict_course_sumeds[x]=points_objects
    print(dict_course_sumeds)
    return render(request,'score/report_sumed_point_for_operator.html',{"dict_course_sumeds":dict_course_sumeds})


def report_detail_score_chart_view(request, enroll):
    try:

        scores_queryset = sum_emtiyazat.objects.filter(enroll=enroll).order_by('date_for')

        # دریافت شیء ثبت‌نام
        enroll_object = link_table.objects.get(id=enroll)
        klass_id = enroll_object.klass_id_id
        class_object = klass.objects.get(id=klass_id)

        start_date = str(class_object.start_date)
        end_date = str(class_object.end_data)

        # تبدیل تاریخ‌ها به datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        # لیست تاریخ‌های هفتگی
        list_date = []
        current_date = start_date
        while current_date <= end_date:
            list_date.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=7)

        # ایجاد لیستی از امتیازها بر اساس تاریخ‌ها
        scores = []
        for date in list_date:
            # بررسی اینکه آیا امتیازی برای این تاریخ وجود دارد یا نه
            score = scores_queryset.filter(date_for=date).first()
            if score:
                scores.append(float(score.sumed_emtiyaz))  # تبدیل امتیاز Decimal به float
            else:
                scores.append(0)
        print(scores)
        # ارسال داده‌ها به قالب
        return render(request, 'score/chart_student.html', {"dates": list_date, "scores": scores})
    except:
        messages.add_message(request,messages.INFO,"لطفا بعدا تلاش کنید")







