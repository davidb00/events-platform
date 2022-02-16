
from django.db.models.signals import post_save
from .models import Message, Profile

from django.contrib.auth.models import User


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        user.username = user.username.lower()
        profile = Profile.objects.create(
            user=user, username=user.username.lower(), email=user.email, first_name=user.first_name, last_name=user.last_name,
        )
        welcome_message = Message.objects.create(sender=Profile.objects.get(
            username='coffeeadmin'), recipient=user.profile, body='Welcome to Coffee-ConX!')


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.first_name
        user.last_name = profile.last_name
        user.username = profile.username
        user.email = profile.email
        user.save()


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
