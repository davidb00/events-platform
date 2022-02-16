from django.urls import path
from . import views

urlpatterns = [
    #path('',views.home,name="home"),
    path('', views.events, name="events"),
    path('ev/<str:pk>/', views.event, name="event"),
    path('create-event/',views.createEvent, name="create-event"),
    path('update-event/<str:pk>/',views.updateEvent,name='update-event'),
    path('like/<str:pk>',views.likeComment, name='like_comment'),
]