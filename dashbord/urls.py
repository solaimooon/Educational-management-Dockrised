from django.urls import path
from .views import *
app_name='dashbord'
urlpatterns = [
    path('',dashbord, name='operator'),
    path('student_info/',student_info_list,name='student_info'),
    path('profile/<int:pk>/',profile,name='profile'),

]