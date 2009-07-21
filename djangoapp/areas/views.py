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
    area = serializers.deserialize("json", request.POST['json']).next()
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

def wizard_get_or_create(request, name):
    wizard, isNew = Wizard.objects.get_or_create(name=name)
    wizard.save()
    return HttpResponse(
        serializers.serialize('json', [wizard]),
        mimetype='application/json'
        )

def realm_get_or_create(request, name):
    realm, isNew = Realm.objects.get_or_create(name=name)
    realm.save()
    return HttpResponse(
        serializers.serialize('json', [realm]),
        mimetype='application/json'
        )
