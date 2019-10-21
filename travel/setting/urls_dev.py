from django.urls import path
from django.conf.urls import include
from setting import settings_dev

from .urls import *


if settings_dev.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
