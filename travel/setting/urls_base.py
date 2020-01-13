from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('travel/', include('travel.urls')),
    path('', RedirectView.as_view(url='accounts/login', permanent=True)),
]
