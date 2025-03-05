from django.shortcuts import render
from .models import ramazan_point as r
from django.contrib.auth.models import User
from athentication.models import *
from django.db.models.functions import Cast
import jdatetime
from django.db.models import F, IntegerField, Value, Case, When, ExpressionWrapper, Q
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from .form import *
from django.urls import reverse
from django.http import HttpResponseRedirect


def chose_peried_of_ramazan(request):
    periods_of_remazan=Time_period.objects.all()
    return render (request,'ramazan/choose_period_of_ramazan.html',{"periods_of_ramazan":periods_of_remazan})



def choose_student(request, peried):
    request.session["period"] = peried

    current_year = jdatetime.date.today().year
    users = extra_user_data.objects.annotate(
        birth_year=ExtractYear(F("age"))
    ).annotate(
        calculated_age=current_year - F("birth_year")  # Rename to avoid conflict
    ).filter(
        sex="male",
        calculated_age__lt=16  # Use new annotation name
    )
    print(users)
    return render(request, 'ramazan/choose_studnet.html', {"users": users})


def register_point(request,id=None):
    if request.method == 'GET':
        request.session["student_id"]=id
        form_ramazan_register = ramazan_point_register()
        student_selected_object=User.objects.get(id=id)
        points = r.objects.filter(
            user_register=request.user,
            Time_period=Time_period.objects.get(id=request.session.get('period')),own_user=User.objects.get(id=request.session["student_id"]))
        return render (request,'ramazan/register_emtyazat.html',{"student_selected_object":student_selected_object,"points":points,"form_ramazan_register":form_ramazan_register})
    # SAVE POINT
    elif request.method == 'POST':
        form_ramazan_register = ramazan_point_register(request.POST)
        if form_ramazan_register.is_valid():
            ramazan_point = form_ramazan_register.save(commit=False)
            ramazan_point.own_user = User.objects.get(id=request.session['student_id'])
            ramazan_point.user_register = User.objects.get(id=request.user.id)
            ramazan_point.Time_period = Time_period.objects.get(id=request.session['period'])
            ramazan_point.save()
            messages.success(request, "امتیاز با موفقیت ثبت شد.")
            return  HttpResponseRedirect(reverse("ramazan:choose_student",kwargs={"id":request.session["student_id"]}))
def delete_point(request,id):
    if request.method == 'POST':
        r.objects.filter(id=id).delete()
        return HttpResponseRedirect(reverse("ramazan:register_point" ,kwargs={"id":request.session["student_id"]}))

        
 
        
        
    