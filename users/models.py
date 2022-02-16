from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Q


# Create your models here.
class Profile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(
        max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField(
        max_length=100, blank=False, null=False, default="", unique=True)
    location = models.CharField(
        max_length=200, blank=False, null=False, default="California")
    social_website = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=True)
    short_intro = models.TextField(max_length=200, blank=True, null=True)
    img_url = models.URLField(max_length=200, null=True, blank=True)
    user_code = models.CharField(max_length=10, blank=True, null=True)

    @property
    def last_initial(self):
        try:
            name = self.first_name + " " + self.last_name[0] + "."
            return name
        except:
            return "St Er."

    def __str__(self) -> str:
        return str(self.last_initial)

    def unread_count(self) -> str:
        unread_amt = (self.received_messages.filter(is_read=False).count())
        if unread_amt == 0:
            return ""
        else:
            unread_str = "(" + str(unread_amt)+")"
            return unread_str


class Message(models.Model):

    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, related_name="sent_messages")
    recipient = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, related_name="received_messages")
    subject = models.CharField(max_length=30, null=True, blank=True)
    body = models.TextField(max_length=500)
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.body[:10]

    @property
    def conversation(self, sender):
        messages = Message.objects.filter(Q(sender=sender, recipient=self) | Q(
            recipient=self, sender=sender)).order_by('created')
        return messages

    class Meta:
        ordering = ['is_read', '-created']
