from django.shortcuts import render
from aik2.models import Getdata
from django.shortcuts import render, redirect, HttpResponse, render_to_response, HttpResponseRedirect
import json

# Create your views here.
DataForGraph = Getdata()


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
