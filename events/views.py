from django.http import HttpResponseRedirect
from events.forms import AttendeeStatusForm, CommentForm, EventForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, EventRegistration, Comment
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def likeComment(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('event', args=[str(pk)]))

    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    if comment.likes.filter(id=request.user.profile.id).exists():
        comment.likes.remove(request.user.profile)
    else:
        comment.likes.add(request.user.profile)
    return HttpResponseRedirect(reverse('event', args=[str(pk)]))

# render all events


def events(request):
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'events/events.html', context)


# render event page and make instance for user to attend or not attend
# @login_required(login_url='/login')
def event(request, pk):
    event_obj = Event.objects.get(id=pk)
    user_obj = request.user

    try:
        registration = get_object_or_404(
            EventRegistration, attendee=user_obj.profile, event=event_obj)
    except:
        registration = None

# Need to update template to use choices field instead of Going boolean

    comment_form = CommentForm()
    rsvp_form = AttendeeStatusForm(instance=registration)
    if request.method == "POST":

        if 'RSVP' in request.POST:
            rsvp_form = AttendeeStatusForm(request.POST)
            if rsvp_form.is_valid():
                new_reg = EventRegistration.objects.update_or_create(
                    attendee=user_obj.profile, event=event_obj)[0]
                new_reg.rsvp = rsvp_form.cleaned_data['rsvp']
                new_reg.guests = rsvp_form.cleaned_data['guests']
                if new_reg.rsvp == 'NO':
                    new_reg.guests = 0
                new_reg.save()
                messages.success(request, ("Registration Updated!"))
        if 'comment' in request.POST:
            if not user_obj.is_authenticated:
                messages.info(request, 'Please login to add a comment!')
                return HttpResponseRedirect(reverse('event', args=[str(pk)]))
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.cleaned_data['body']
                comment = Comment.objects.create(
                    attendee=user_obj.profile, event=event_obj, body=comment)
                return HttpResponseRedirect(reverse('event', args=[str(pk)]))

    else:
        comment_form = CommentForm()

    attendees = EventRegistration.objects.filter(event=pk)
    comments = Comment.objects.filter(event=pk)
    context = {'event': event_obj, 'comment_form': comment_form,
               'comments': comments, 'rsvp_form': rsvp_form, 'attendees': attendees}

    return render(request, 'events/single-event.html', context)


# create an event using form
def createEvent(request):
    profile = request.user.profile
    form = EventForm()

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid:
            event = form.save(commit=False)
            event.organizer = profile
            event.save()
            EventRegistration.objects.create(event=event, attendee=profile)

    context = {'form': form}
    return render(request, "events/event_form.html", context)


# Pass instance of existing event to form for update
def updateEvent(request, pk):
    profile = request.user.profile
    event = Event.objects.get(id=pk)
    event_ref = event
    group = event.group
    print(group)
    form = EventForm(instance=event)

    if request.method == 'POST':

        form = EventForm(request.POST, instance=event)

        if form.is_valid():
            delete = form.cleaned_data['delete']
            event = form.save(commit=False)

            if group == event.group and profile == event.organizer:
                event.save()
                if delete:
                    event_ref.delete()
            else:
                messages.info(request, "Validation error")

        return redirect('events')

    context = {'form': form, 'event': event}
    return render(request, "events/event_form.html", context)
