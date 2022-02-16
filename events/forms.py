from django import forms
from django.forms import ModelForm
from .models import Comment, Event, EventRegistration


class AttendeeStatusForm(forms.ModelForm):

    class Meta:
        model = EventRegistration
        fields = ['rsvp', 'guests']


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['group', 'title', 'description',
                  'location', 'date', 'start_time', 'end_time', ]
        labels = {
            'date': "Date (yyyy-mm-dd hh:mm)"
        }

    delete = forms.BooleanField(label='Delete Event', required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {
            'body': 'Comment'
        }

        widgets = {
            'body': forms.TextInput(attrs={'class': 'form-control',
                                           'autocomplete': 'off'})}
