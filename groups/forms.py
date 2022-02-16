from django import forms
from django.contrib.auth.models import Group


class JoinForm(forms.Form):
    group_status = forms.NullBooleanField(widget=forms.widgets.Select(
        choices=[
            ('', '--'),
            (True, 'Join'),
            (False, 'Leave'),
        ]
        ))
