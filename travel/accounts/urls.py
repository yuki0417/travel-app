from django.urls import path

from . import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('test_login/', views.test_login, name='test_login'),
    path('logout_confirm/', views.logout_confirm, name='logout_confirm'),
    path('logged_out/', views.logged_out, name='logged_out'),
]
