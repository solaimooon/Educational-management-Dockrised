from athentication.models import *
from .forms import *
from django.contrib.auth.models import User

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage,InvalidPage
from django.contrib import messages


@login_required(login_url='/athentication/')
def dashbord(request):
    # render oprator page if usre be staff
    if request.user.is_staff==True:
        extra_data=extra_user_data.objects.filter(forign_key=request.user.pk)[0]
        # keep the picture of user in session_for save the adress of picture we must save the url
        request.session["picture"] =extra_data.image.url
        return render(request, 'dashbord_opratoe/oprator_index.html',{"extra_data":extra_data})
    # render student base page if usre not be staff
    else:
        extra_data = extra_user_data.objects.filter(forign_key=request.user.pk)[0]
        request.session["picture"] = extra_data.image.url
        return render(request, 'dashbord_student/student_index.html', {"extra_data": extra_data})


# Create your views here.


@login_required(login_url='/athentication/')
def student_info_list(request):

    students=User.objects.filter(is_staff=False)
    students_extra_data=extra_user_data.objects.raw(
            "select * from athentication_extra_user_data where forign_key_id in(select id from auth_USER where is_staff=False)")
    # integrate the element of first itrable to element of second iterable as tuple -first element of first list to first element of second list
    zip_student=list(zip(students, students_extra_data))

    # paginating
    paginating_object = Paginator(zip_student, 10)
    try:
        page_number_requested = request.GET.get('page_number')
        the_page_requested=paginating_object.page(page_number_requested)
    except InvalidPage:
        the_page_requested = paginating_object.page(1)
    print(list(zip_student))
    contex={"zip_student":the_page_requested}
    return render(request, 'dashbord_opratoe/oprator_student_list.html', contex)

# edit profile
@login_required(login_url='/athentication/')
def profile(request,pk=None):
    #the staff profile
    if request.user.is_staff == True:
        # get data of user
        student = User.objects.filter(id=pk)[0]
        student_extra_data = extra_user_data.objects.filter(forign_key=pk)[0]
        # find object of the student phone in phone tabel to creat form with  previous data if there isnt any data we undrestand by ty/exeptin and create
        # form without previous data
        try:
            # get phone of user
            phone_of_student = phone.objects.filter(forign_key=pk)[0]
            # creat form with privose data
            phone_form_object = phone_form(instance=phone_of_student)
        except:
            phone_form_object = phone_form()
        # create the form with previous user data
        user_form_object = UserForm(instance=student)
        extra_data_form = update_extra_user_data(instance=student_extra_data)
        contex = {"user_data": student, "extra_user_data": student_extra_data, "user_form": user_form_object,
                  'form': extra_data_form, "phone_form": phone_form_object}
        return render(request, 'dashbord_opratoe/operator_profile.html', contex)
    # the student profile
    else:
        # show profile
        if request.method=='GET':
            # get data of user
            student = User.objects.filter(id=pk)[0]
            student_extra_data = extra_user_data.objects.filter(forign_key=pk)[0]
            # find object of the student phone in phone tabel to creat form with  previous data if there isnt any data we undrestand by ty/exeptin and create
            # form without previous data
            try:
                # get phone of user
                phone_of_student=phone.objects.filter(forign_key=pk)[0]
                # creat form with privose data
                phone_form_object = phone_form(instance=phone_of_student)
            except:
                phone_form_object = phone_form()
            # create the form with previous user data
            user_form_object=UserForm(instance=student)
            extra_data_form=update_extra_user_data(instance=student_extra_data)
            contex={"user_data": student, "extra_user_data": student_extra_data,"user_form":user_form_object,'form':extra_data_form,"phone_form":phone_form_object}
            return render(request, 'dashbord_student/student_profile.html',contex)
        # update profile
        else:
            # find the pk of user in extra_user_data tabel if there isnt we undrestand by ty/exeptin and create new record for it
            # creatث form object for user and extra user data and phone to save it
            # for crete form with file data such as image we must add request.files
            UserForm_object = UserForm(request.POST)
            extra_user_data_form=update_extra_user_data(request.POST,request.FILES)
            phone_form_object=phone_form(request.POST)
            if  UserForm_object.is_valid() and extra_user_data_form.is_valid() and phone_form_object.is_valid():
                # update user and extra tabel
                User.objects.filter(id=request.user.id).update(**UserForm_object.cleaned_data)
                extra_user_data.objects.filter(forign_key=request.user).update(**extra_user_data_form.cleaned_data)
                # update image sepratly ( i dont khow but image dosnt update automaticly )
                image_user = extra_user_data.objects.filter(forign_key=request.user)[0]
                image_user.image=extra_user_data_form.cleaned_data["image"]
                image_user.save()
                messages.add_message(request,messages.SUCCESS,"اطلاعات با موفقیت ثبت شد")
                #
                if phone_form_object.cleaned_data['phone_number'] != "":
                    phone_object=phone()
                    phone_object.phone_number=phone_form_object.cleaned_data['phone_number']
                    phone_object.owner=phone_form_object.cleaned_data['owner']
                    phone_object.forign_key=request.user
                    phone_object.save()
                else:
                    print("user didnt sent phone form")
                # update the url of picture in session
                request.session["picture"]=extra_user_data.objects.filter(forign_key=request.user)[0].image.url
                return HttpResponseRedirect(reverse("dashbord:profile",kwargs={'pk':request.user.id}))
            else:
                for field, errors in extra_user_data_form.errors.items():
                    # نمایش خطای مربوط به هر فیلد
                    for error in errors:
                        # ارسال خطا به پیام‌ها
                        messages.error(request, f'خطا در فیلد {field}: {error}')
                print("سلام ",extra_user_data_form.errors.as_data())  # here you print errors to terminal
                return HttpResponseRedirect(reverse('dashbord:profile',kwargs={"pk":pk}))