import urllib, urllib2

params = urllib.urlencode(
    {"json":
         '[{"pk": 0, "model": "areas.area", "fields": {"name": "external source"}}]'
     })

req = urllib2.Request(
    url = "http://localhost:8000/areas/area/create/",
    data = params
    )
#data = area_json

for line in urllib2.urlopen(req).readlines():
    print line

#try:
#    response = urlopen(req)
#except URLError, e:
#    if hasattr(e, 'reason'):
#        print 'We failed to reach a server.'
#        print 'Reason: ', e.reason
#    elif hasattr(e, 'code'):
#        print 'The server couldn\'t fulfill the request.'
#        print 'Error code: ', e.code
#else:
#    # everything is fine
