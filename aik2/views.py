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
    if request.method == 'POST':
        if request.is_ajax():
            id = int(request.POST['id'])
            template = 'aik2/chartform.html'
            if id == 1:
                template = 'aik2/statform.html'
            if id == 2:
                template = 'aik2/protform.html'
            if id == 3:
                return render(request, 'aik2/trendsform.html', {"ttype": 0})
            if id == 4:
                return render(request, 'aik2/sesform.html', {"mtype": 0})
            if id == 5:
                return render(request, 'aik2/sesform.html', {"mtype": 1})
            if id == 6:
                return render(request, 'aik2/trendsform.html', {"ttype": 1})
            return render(request, template, {})
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


def ai_json_fullstat(request):
    try:
        if request.method == 'POST':
            if request.is_ajax():
                st = request.POST['st']
                en = request.POST['en']
                return HttpResponse(json.dumps(DataForChart.get_json_fullstat(st, en)), content_type="application/json")
        return HttpResponse(json.dumps([]), content_type="application/json")
    except Exception as e:
        error = {'error': e}
        return HttpResponse(json.dumps(error), content_type="application/json")


def ai_json_protocol(request):
    try:
        if request.method == 'POST':
            if request.is_ajax():
                dt = request.POST['dt']
                dr = request.POST['dr']
                return HttpResponse(json.dumps(DataForChart.get_json_protocol(dr, dt)), content_type="application/json")
        return HttpResponse(json.dumps([]), content_type="application/json")
    except Exception as e:
        error = {'error': e}
        return HttpResponse(json.dumps(error), content_type="application/json")


def ai_json_trend(request):
    try:
        if request.method == 'POST':
            if request.is_ajax():
                idc = request.POST['id']
                ttype = int(request.POST['type'])
                return HttpResponse(json.dumps(DataForChart.get_json_thrend(idc, ttype)), content_type="application/json")
        return HttpResponse(json.dumps([]), content_type="application/json")
    except Exception as e:
        error = {'error': e}
        return HttpResponse(json.dumps(error), content_type="application/json")


def ai_json_grses(request):
    try:
        if request.method == 'POST':
            if request.is_ajax():
                ds = request.POST['ds']
                de = request.POST['de']
                type = int(request.POST['type'])
                mtype = int(request.POST['mtype'])
                return HttpResponse(json.dumps(DataForChart.get_json_stat_grses(ds, de, type, mtype)), content_type="application/json")
        return HttpResponse(json.dumps([]), content_type="application/json")
    except Exception as e:
        error = {'error': e}
        return HttpResponse(json.dumps(error), content_type="application/json")
