import re
from mockworld import World
from django.utils import simplejson
import urllib, urllib2
from urllib2 import URLError

world = World()

class Area(object):
    def __init__(self, creators, name, realms, closed, defunct):
        self.creators = creators
        self.name = name
        self.realms = realms
        self.is_closed = closed
        self.is_defunct = defunct

    def to_django_json(self):
        obj = [{"pk":0,
                "model": "areas.area",
                "fields": {
                    "name": self.name,
                    }}]
        return simplejson.dumps(obj)

    def submit(self):
        creators = self.submitCreators()
        realms = self.submitRealms()
        self.submitArea(creators, realms)

    def submitCreators(self):
        creators = []
        for wizard in self.creators:
            json = simplejson.dumps([{
                        "pk": 0, "model": "areas.wizard",
                        "fields": {"name": wizard,} } ])
            response = self.sendRequest(
                json,
                "http://localhost:8000/areas/wizard/get_or_create/%s/" % (wizard))
            if response:
                obj = simplejson.loads(response.readline())[0]
                creators.append(obj['pk'])
        return creators

    def submitRealms(self):
        realms = []
        for realm in self.realms:
            json = simplejson.dumps([{
                        "pk": 0, "model": "areas.realm",
                        "fields": {"name": realm,} } ])
            response = self.sendRequest(
                json,
                "http://localhost:8000/areas/realm/get_or_create/%s/" % (realm))
            if response:
                obj = simplejson.loads(response.readline())[0]
                realms.append(obj['pk'])
        return realms

    def submitArea(self, creators, realms):
        obj = [{"pk":0,
                "model": "areas.area",
                "fields": {
                    "name": self.name,
                    "creators": creators,
                    "realms": realms,
                    "defunct": self.is_defunct,
                    "closed": self.is_closed,
                    }}]
        json = simplejson.dumps(obj)
        response = self.sendRequest(json, "http://localhost:8000/areas/area/create/")

    def sendRequest(self, json, url):
        params = urllib.urlencode({"json": json})
        req = urllib2.Request(url = url, data = params)

        response = None
        try:
            response = urllib2.urlopen(req)
        except URLError, e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
                fo = open("error_log.html", "w")
                for line in e.readlines():
                    fo.write(line)
        return response

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.__str__()

def parse(lines):
    num = creators = name = realms = ""
    closed = defunct = False
    for line in lines:
        num += line[0:8]
        creators += line[8:28] + " "
        name += line[29:64] + " "
        realms += line[65:] + " "

    area_creators = [creator.strip() for creator in re.split("\W+", creators.strip())]
    while 'and' in area_creators: area_creators.remove('and')

    area_realms = [realm.strip() for realm in realms.strip().split()]
    while 'and' in area_realms: area_realms.remove('and')

    if '(CLOSED)' in area_realms:
        area_realms.remove('(CLOSED)')
        closed = True
    if '(DEFUNCT)' in area_realms:
        area_realms.remove('(DEFUNCT)')
        defunct = True

    return Area(area_creators, name.strip(), area_realms, closed, defunct)

def scan(lines):
    entry = re.compile("^\s*\d+\.\s+\w+.*$")
    more = re.compile("^More: \d+-\d+\(\d+\).*$")
    end = re.compile("^>\s+$")

    areas = []
    area_lines = []
    for line in lines:
        if end.match(line) or more.match(line):
            if len(area_lines) > 0: areas.append(parse(area_lines))
        elif entry.match(line):
            if len(area_lines) > 0: areas.append(parse(area_lines))
            area_lines = [line]
        else:
            if len(area_lines) > 0: area_lines.append(line)
    return areas
