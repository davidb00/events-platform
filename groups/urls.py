from django.urls import path
from . import views

urlpatterns = [
    path('', views.groups, name="groups"),
    path('gr/<str:pk>/', views.group, name="group"),
    path('join/<str:pk>',views.joinGroup, name='join-group'),
   # path('gr/<int:pk>/') #not using uuid for this
]