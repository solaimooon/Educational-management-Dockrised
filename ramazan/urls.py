
from django.urls import path
from .views import *
app_name='ramazan'
urlpatterns = [
    path('chose_peried_of_ramazan/',chose_peried_of_ramazan,name='chose_peried_of_ramazan'),
    path('choose_student/<int:peried>',choose_student,name='choose_student'),
    path('register_point/<int:id>',register_point,name='register_point'),
    path('register_point/',register_point,name='register_point'),
    path('delete_point/<int:id>',delete_point,name='delete_point'),
    path('choose_period_student/',choose_period_student,name='choose_period_student'),
    path('show_ramazan_point/<int:period>',show_ramazan_point,name='show_ramazan_point'),
    path('list_ramazan_emtiyaz_student/',list_ramazan_emtiyaz_student,name='list_ramazan_emtiyaz_student'),
    path('ramazan_detail_score/',detail_score,name='detail_score')
    

]