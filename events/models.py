from django.db import models
import uuid
from users.models import Profile
from groups.models import Group
from django.db.models import Sum
from django.core.validators import MaxValueValidator


class Event(models.Model):
    organizer = models.ForeignKey(
        Profile, null=True, blank=False, on_delete=models.SET_NULL)
    title = models.CharField(
        max_length=200, default="", null=True, blank=False)
    description = models.TextField(null=True, blank=True)
    # featured_image= models.ImageField(null=True,blank=True, default="#")
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    start_time = models.CharField(max_length=6, null=True, blank=True)
    end_time = models.CharField(max_length=6, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    group = models.ForeignKey(
        Group, blank=False, null=True, on_delete=models.SET_NULL)
    img_url = models.URLField(max_length=200, blank=True, default=True)

    @property
    def guest_count(self):
        try:
            count = self.eventregistration_set.all().aggregate(Sum('guests'))[
                'guests__sum'] + self.eventregistration_set.filter(rsvp="YES").count()
        except:
            count = 0
        return count

    class Meta:
        ordering = ['date']

    def __str__(self) -> str:
        return str(self.title)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self) -> str:
        return str(self.name)


class EventRegistration(models.Model):
    GOING = 'YES'
    NOT_ATTENDING = 'NO'
    RSVP_CHOICES = [
        (GOING, 'Yes'), (NOT_ATTENDING, 'No')
    ]
    event = models.ForeignKey(Event, blank=False, on_delete=models.CASCADE)
    attendee = models.ForeignKey(
        Profile, null=True, blank=False, on_delete=models.CASCADE)
    time_registered = models.DateTimeField(auto_now=True)
    guests = models.PositiveSmallIntegerField(
        default=0, validators=[MaxValueValidator(8)])
    rsvp = models.CharField(
        max_length=3, choices=RSVP_CHOICES, default=NOT_ATTENDING)

    class Meta:
        unique_together = [['event', 'attendee']]
        ordering = ['rsvp', 'time_registered']

    def __str__(self):
        return str(self.event.title+": "+self.attendee.first_name)


class Comment(models.Model):
    attendee = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    body = models.TextField(max_length=250)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Profile, related_name='user_likes')

    def total_likes(self):
        return self.likes

    def __str__(self):
        return (self.attendee.username)
