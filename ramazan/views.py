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
    users = extra_user_data.objects.filter(
        sex="male",
        forign_key__is_staff=False  # Use new annotation name
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
            return  HttpResponseRedirect(reverse("ramazan:choose_student",kwargs={"peried":request.session["period"]}))
def delete_point(request,id):
    if request.method == 'POST':
        r.objects.filter(id=id).delete()
        return HttpResponseRedirect(reverse("ramazan:register_point" ,kwargs={"id":request.session["student_id"]}))

        
 # show point to student 
 
def choose_period_student(request):
    period=Time_period.objects.all()
    return render (request,'ramazan/choose_period_ramazan_student.html',{"period":period})

     
def show_ramazan_point (request,period):
    try:
        request.session["period"]=period
        #point=ramazan_final.objects.get(own_user_id=request.user,Time_period_id=period)
        #return render (request,'ramazan/ramazan_show_point.html',{"point":point})
        messages.info(request, "اعلام نتیجه نهایی در جشن اختتامیه")
        return HttpResponseRedirect(reverse("ramazan:choose_period_student"))
    except:
        messages.info(request, "برای شما امتیازی ثبت نشده است")
        return HttpResponseRedirect(reverse("ramazan:choose_period_student"))
        

def list_ramazan_emtiyaz_student(request):
    point=ramazan_final.objects.all()
    messages.info(request, "اعلام نتیجه نهایی در جشن اختتامیه")
    return render (request,'dashbord_student/student_index.html',{"points":point})
    #return render (request,'ramazan/ramazan_list_point_student.html',{"points":point})

    
            
def detail_score (request):
    period_id = request.session.get("period")
    print("period_id",period_id)
    scores=ramazan_point.objects.filter(own_user=request.user,Time_period__id=period_id)
    return render(request,'ramazan/ramazan_detail_score.html',{"scores":scores})



from datetime import date

def list_ramazan_emtiyaz_operator(request):
    points = ramazan_final.objects.prefetch_related("own_user__extra_user_data_set").all()

    # لیست جدید برای ذخیره داده‌ها همراه با سن محاسبه‌شده
    points_with_age = []
    
    # گرفتن تاریخ امروز به شمسی
    today = jdatetime.date.today()

    for point in points:
        user_data = point.own_user.extra_user_data_set.first()  # دریافت اولین رکورد extra_user_data

        if user_data and user_data.age:
            birth_date = user_data.age  # مقدار تاریخ تولد شمسی
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        else:
            age = "نامشخص"

        points_with_age.append({
            "rotbe": point.rotbe,
            "name": point.own_user.get_full_name(),
            "age": age,
            "total_amount": point.total_amount,
        })

    return render(request, 'ramazan/ramazan_list_point_operator.html', {"points": points_with_age})


    