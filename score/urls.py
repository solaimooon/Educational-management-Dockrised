from django.urls import path
from .views import *
app_name='score'
urlpatterns = [
    path('<int:id>/',choose_date_view, name='choose_date'),
    path('post_score/',post_score_view,name='post_score'),
    path('delete_csore/<int:id>/',delete_csore_view,name='delete_score'),
    path('delete_present/<int:id>/',delete_present_view,name='delete_present'),
    path("report_sumed_emtyazat_operator/",report_sumed_score_for_operator_view,name='report_sumed_emtyazat_operator'),
    path('report_detail_score_chart/<int:enroll>/',report_detail_score_chart_view,name='report_detail_score_chart')

]