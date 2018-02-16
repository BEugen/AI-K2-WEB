from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ai_json_graph', views.ai_json_graph, name='ai_json_graph'),
]
