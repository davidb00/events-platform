from django.contrib import admin

# Register your models here.
from .models import Event, Tag, EventRegistration, Comment

admin.site.register(Event)
admin.site.register(Tag)
admin.site.register(EventRegistration)
admin.site.register(Comment)