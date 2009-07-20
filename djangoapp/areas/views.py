from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core import serializers

from areas.models import *

def index(request):
    return render_to_response('areas.html', {'areas': areas})

def area_list(request):
    areas = Area.objects.all()
    return render_to_response('arealist.html', {'areas': areas})

def area_create(request):
    for area in serializers.deserialize("json", request.POST['json']):
        area.object.id = None
        area.save()
    return HttpResponse(
        serializers.serialize('json', [area.object]),
        mimetype='application/json'
        )

def area_read(request):
    return

def area_update(request):
    return

def area_delete(request):
    return
