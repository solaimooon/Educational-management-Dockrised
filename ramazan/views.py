from django.shortcuts import render
from .models import*
def chose_peried_of_ramazan(request):
    periods_of_remazan=Time_period.objects.all()
    return render (request,{"periods_of_ramazan":periods_of_remazan},)

# Create your views here.

