from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .forms import UserLoginForm

urlpatterns = [
    # path('login/',views.loginUser,name="login"),
    path('', views.home, name='home'),
    path('register/', views.registerUser, name='register'),
    path('profiles/', views.profiles, name='profiles'),
    path('profiles/u/<str:pk>/', views.profile, name='profile'),
    #path('feed/', views.feed,  name='feed'),
    path('edit-account/', views.editAccount, name="edit-account"),
    path('account/', views.userAccount, name="account"),
    path('register2/', views.UserRegisterView.as_view(), name='register2'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.message, name='message'),
    path('send_message/', views.sendMessage, name='send-message'),
    path('login2/', auth_views.LoginView.as_view(authentication_form=UserLoginForm), name='login'),
    path('login/', views.loginUser, name="custom_login"),
    path('demo-login', views.demoLogin, name='demo_login'),
]
