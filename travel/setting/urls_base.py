from django.contrib import admin
from django.urls import path
from django.conf.urls import include
import decouple

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('travel/', include('travel.urls')),
]
