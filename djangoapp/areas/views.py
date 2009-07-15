from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from areas.models import *

def index(request):
    areas = Area.objects.all()
    return render_to_response('areas.html', {'areas': areas})
