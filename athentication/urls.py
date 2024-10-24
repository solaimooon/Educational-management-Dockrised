from django.urls import path
from .views import *

app_name='athentication'

urlpatterns = [
path('', login_form, name='log in'),
path("log_out/",log_out_view,name="log_out") ,
path('sign_up/', sign_up_form, name='sign up'),
path('reset_password/',reset_password_form,name='reset_password'),
path('verification/',verification,name='verification'),
path('update_password',update_password_view,name='update_password')
]