from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core import serializers

from bards.models import *


def recall_category_list(request):
    return render_to_response('recall_category_list.html', {})


def entry_create(request):
    entry = serializers.deserialize("json", request.POST['json']).next()
    entry.object.id = None
    entry.save()
    return HttpResponse(
        serializers.serialize('json', [entry.object]),
        mimetype='application/json'
        )


def area_list(request):
    entries = AreaEntry.objects.all()
    return render_to_response('entrylist.html',
                              {'type':'areas', 'entries': entries})

def area_read(request, entryId):
    entry = AreaEntry.objects.get(id=entryId)
    return render_to_response('recall_entry.html',
                              {'entry': entry})

def armour_list(request):
    entries = ArmourEntry.objects.all()
    return render_to_response('entrylist.html',
                              {'type':'armours', 'entries': entries})

def armour_read(request, entryId):
    entry = ArmourEntry.objects.get(id=entryId)
    return render_to_response('recall_entry.html',
                              {'entry': entry})

def item_list(request):
    entries = ItemEntry.objects.all()
    return render_to_response('entrylist.html',
                              {'type':'items', 'entries': entries})

def item_read(request, entryId):
    entry = ItemEntry.objects.get(id=entryId)
    return render_to_response('recall_entry.html',
                              {'entry': entry})

def misc_list(request):
    entries = MiscEntry.objects.all()
    return render_to_response('entrylist.html',
                              {'type':'miscs', 'entries': entries})

def misc_read(request, entryId):
    entry = MiscEntry.objects.get(id=entryId)
    return render_to_response('recall_entry.html',
                              {'entry': entry})

def mob_list(request):
    entries = MobEntry.objects.all()
    return render_to_response('entrylist.html',
                              {'type':'mobs', 'entries': entries})

def mob_read(request, entryId):
    entry = MobEntry.objects.get(id=entryId)
    return render_to_response('recall_entry.html',
                              {'entry': entry})

def weapon_list(request):
    entries = WeaponEntry.objects.all()
    return render_to_response('entrylist.html',
                              {'type':'weapons', 'entries': entries})

def weapon_read(request, entryId):
    entry = WeaponEntry.objects.get(id=entryId)
    return render_to_response('recall_entry.html',
                              {'entry': entry})
