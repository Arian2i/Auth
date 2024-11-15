from django.urls import path, include
from . import views


app_name = 'account'
urlpatterns = [

    path('', views.index, name='index'),
    path('login', views.UserLogin.as_view(), name='user_login'),
    path('otpLogin', views.OtpLoginView.as_view(), name='user_otpLogin'),
    path('checkotp', views.CheckOtpView.as_view(), name='check_otp'),
    path('logout', views.user_logout, name='user_logout'),
]
