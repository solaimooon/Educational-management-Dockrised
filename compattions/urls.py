from django.urls import path
from .views import *
app_name='compattions'
urlpatterns = [
    path('',all_compattions, name='all_compattions'),
    path('copetions/<int:id>',celected_competions, name='celected_competions'), 
    path('success_submit/',success_submit, name='success_submit')
    
    

]