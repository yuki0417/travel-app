from django.contrib import admin
from django.urls import path
from django.conf.urls import include
import decouple
from setting import settings_dev

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('travel/', include('travel.urls')),
]

try:
    if settings_dev.DEBUG:
        import debug_toolbar
        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
except decouple.UndefinedValueError:
    pass
