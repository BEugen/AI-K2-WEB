from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ai_json_graph', views.ai_json_graph, name='ai_json_graph'),
    url(r'^ai_json_recognize', views.ai_json_recognize, name='ai_json_recognize'),
    url(r'^ai_json_day_chart', views.ai_json_day_chart, name='ai_json_day_chart'),
    url(r'^ai_json_ses_chart', views.ai_json_ses_chart, name='ai_json_ses_chart'),
    url(r'^ai_json_stat', views.ai_json_stat, name='ai_json_stat'),

]
