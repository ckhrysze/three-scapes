from django.conf.urls.defaults import *

urlpatterns = patterns(
    'areas.views',
    (r'^map/view/(?P<mapId>\d+)/', 'renderMap'),
    (r'^map/edit/(?P<mapId>\d+)/', 'editMap'),
    (r'^map/move/(?P<mapId>\d+)/(?P<direction>\w+)/', 'move'),
    (r'^map/', 'newMap'),

    (r'^area/list/', 'area_list'),
    (r'^area/create/', 'area_create'),
    (r'^area/read/(?P<areaId>\d+)/', 'area_read'),
    (r'^area/update/(?P<areaId>\d+)/', 'area_update'),
    (r'^area/delete/(?P<mapId>\d+)/', 'area_delete'),

    (r'^wizard/get_or_create/(?P<name>\w+)/', 'wizard_get_or_create'),
    (r'^realm/get_or_create/(?P<name>\w+)/', 'realm_get_or_create'),

)
