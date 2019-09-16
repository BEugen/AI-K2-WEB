from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ai_json_graph', views.ai_json_graph, name='ai_json_graph'),
    url(r'^ai_json_recognize', views.ai_json_recognize, name='ai_json_recognize'),
    url(r'^ai_json_day_chart', views.ai_json_day_chart, name='ai_json_day_chart'),
    url(r'^ai_json_ses_chart', views.ai_json_ses_chart, name='ai_json_ses_chart'),
    url(r'^ai_json_fullstat', views.ai_json_fullstat, name='ai_json_fullstat'),
    url(r'^ai_json_stat', views.ai_json_stat, name='ai_json_stat'),
    url(r'^ai_json_protocol', views.ai_json_protocol, name='ai_json_protocol'),
    url(r'^ai_json_dt_protocol', views.ai_json_dt_protocol, name='ai_json_dt_protocol'),
    url(r'^ai_json_trend', views.ai_json_trend, name='ai_json_trend'),
    url(r'^ai_json_grses', views.ai_json_grses, name='ai_json_grses'),
]
