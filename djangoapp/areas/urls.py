from django.conf.urls.defaults import *

urlpatterns = patterns(
    'areas.area_views',
    (r'^map/view/(?P<mapId>\d+)/', 'renderMap'),
    (r'^map/edit/(?P<mapId>\d+)/', 'editMap'),
    (r'^map/move/(?P<mapId>\d+)/(?P<direction>\w+)/', 'move'),
    (r'^map/', 'newMap'),
    (r'^', 'index'),
)
