from django.contrib import messages
from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse


def all_compattions(request):
    if not request.user.first_name:
        messages.add_message(request, messages.INFO,"ابتدا اطلاعات خود را تکمیل نمایید")
        return HttpResponseRedirect(reverse("dashbord:profile" ,args=[request.user.id]))
    else:
        all_compattions=compattions.objects.all().order_by('creat_at')
        return render(request,"compattions/index_compattions.html",{"all_compattions":all_compattions})
def celected_competions(request,id):
    celected_competion=compattions.objects.filter(pk=id)[0]
    return render(request,"compattions/celected_competions.html",{"celected_competion":celected_competion})

def success_submit(request):
    messages.add_message(request, messages.SUCCESS, "با موفقیت ثبت شد")
    all_compattions=compattions.objects.all().order_by('creat_at')
    return render(request,"compattions/index_compattions.html",{"all_compattions":all_compattions})