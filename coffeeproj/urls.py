from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('adminx/', admin.site.urls),
    path('events/', include('events.urls')),
    path('', include('users.urls')),
    path('feed/', include('feature.urls')),
    path('groups/', include('groups.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),

]
