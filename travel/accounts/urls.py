from django.urls import path

from . import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.AccountLoginView.as_view(), name='login'),
]
