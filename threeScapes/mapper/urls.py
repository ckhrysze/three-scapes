from django.conf.urls.defaults import *

urlpatterns = patterns('mapper.views',
    (r'^map', 'index'),
)
