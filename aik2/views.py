from django.shortcuts import render
from aik2.models import Getdata, Getstat, GetStatForChart, GetDataRecognize
from django.shortcuts import render, redirect, HttpResponse, render_to_response, HttpResponseRedirect
import json

# Create your views here.
DataForGraph = Getdata()
DataForStat = Getstat()
DataForChart = GetStatForChart()
DataRecognize = GetDataRecognize()


def index(request):
    return render(request, 'aik2/index.html', {})


def ai_json_graph(request):
    try:
        if request.method == 'POST':
            if request.is_ajax():
                return HttpResponse(json.dumps(DataForGraph.get_json_data()), content_type="application/json")
        return HttpResponse(json.dumps([]), content_type="application/json")
    except Exception as e:
        error = {'error': e}
        return HttpResponse(json.dumps(error), content_type="application/json")


def ai_json_recognize(request):
    try:
        if request.method == 'POST':
            if request.is_ajax():
                dumps = json.dumps(DataRecognize.get_json_data())
                return HttpResponse(dumps, content_type="application/json")
        return HttpResponse(json.dumps([]), content_type="application/json")
    except Exception as e:
        error = {'error': e}
        return HttpResponse(json.dumps(error), content_type="application/json")


def ai_json_stat(request):
    try:
        if request.method == 'POST':
            if request.is_ajax():
                return HttpResponse(json.dumps(DataForStat.get_json_stat('')), content_type="application/json")
        return HttpResponse(json.dumps([]), content_type="application/json")
    except Exception as e:
        error = {'error': e}
        return HttpResponse(json.dumps(error), content_type="application/json")


def ai_json_day_chart(request):
    try:
        if request.method == 'POST':
            if request.is_ajax():
                return HttpResponse(json.dumps(DataForChart.get_json_stat_day()), content_type="application/json")
        return HttpResponse(json.dumps([]), content_type="application/json")
    except Exception as e:
        error = {'error': e}
        return HttpResponse(json.dumps(error), content_type="application/json")


def ai_json_ses_chart(request):
    try:
        if request.method == 'POST':
            if request.is_ajax():
                id = int(request.POST['id'])
                return HttpResponse(json.dumps(DataForChart.get_json_stat_ses(id)), content_type="application/json")
        return HttpResponse(json.dumps([]), content_type="application/json")
    except Exception as e:
        error = {'error': e}
        return HttpResponse(json.dumps(error), content_type="application/json")
