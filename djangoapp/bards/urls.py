from django.conf.urls.defaults import *

urlpatterns = patterns(
    'bards.views',
    (r'^recall/category/list/', 'recall_category_list'),

    (r'^recall/entry/create/', 'entry_create'),

    (r'^recall/areas/list/', 'area_list'),
    (r'^recall/areas/read/(?P<entryId>\d+)/', 'area_read'),

    (r'^recall/armours/list/', 'armour_list'),
    (r'^recall/armours/read/(?P<entryId>\d+)/', 'armour_read'),

    (r'^recall/items/list/', 'item_list'),
    (r'^recall/items/read/(?P<entryId>\d+)/', 'item_read'),

    (r'^recall/miscs/list/', 'misc_list'),
    (r'^recall/miscs/read/(?P<entryId>\d+)/', 'misc_read'),

    (r'^recall/mobs/list/', 'mob_list'),
    (r'^recall/mobs/read/(?P<entryId>\d+)/', 'mob_read'),

    (r'^recall/weapons/list/', 'weapon_list'),
    (r'^recall/weapons/read/(?P<entryId>\d+)/', 'weapon_read'),

)
