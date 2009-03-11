# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('gheat.views',
    url(
        # Example : today/fire/12/3,2.png
        regex = r'^(?P<color_scheme>\w+)/(?P<zoom>\d+)/(?P<x>\d+),(?P<y>\d+).png$',
        view = 'serve_tile',
        name = 'serve_tile',
       ),
    )
