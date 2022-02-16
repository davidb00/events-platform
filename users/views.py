from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import CreateMessageForm, CustomUserCreationForm, MessageForm, ProfileForm, SignUpForm, MessageForm2
from .models import Message, Profile
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .utils import paginate_messages, user_inbox
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.models import User


class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Account created successfully')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('edit-account')  # to become edit-account page

        else:
            messages.warning(
                request, 'An error has occurred during registration')

    context = {'form': form, 'page': page}
    return render(request, 'users/register.html', context)


def home(request):
    # if request.user.is_authenticated:
    return redirect('events')
    # return render(request,'events/events.html')


def profiles(request):
    profiles = Profile.objects.all().order_by('created')  # added created ordering
    context = {'profiles': profiles}
    print(profiles)
    return render(request, 'users/profiles.html', context)


def profile(request, pk):
    profileObj = Profile.objects.get(id=pk)
    context = {'profileObj': profileObj}
    print(profileObj)
    return render(request, 'users/profile.html', context)


def feed(request):
    return render(request, 'users/feed.html')


# add login_required decorator, post_save method
def editAccount(request):

    profile = request.user.profile

    if profile.username == 'johnsmith60':
        messages.warning(
            request, 'Cannot modify demo account, please register for the full experience!')
        return redirect('feed')

    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            #user.location = zip_to_city(user.location)

            user.save()
            return redirect('profiles')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


def userAccount(request):
    profile = request.user.profile
    groups = profile.group_set.filter(members=profile)
    registrations = profile.eventregistration_set.filter(rsvp='YES')
    print(registrations)

    context = {'profile': profile, 'groups': groups,
               'registrations': registrations}

    return render(request, 'users/account.html', context)


def inbox(request):
    profile = request.user.profile

    user_messages = profile.received_messages.all()

    sent_messages = profile.sent_messages.all()

    users = profile.received_messages.order_by().values_list('sender').distinct()
    users2 = profile.sent_messages.order_by().values_list('recipient').distinct()

    new_messages = []
    for user in users:
        new_messages.append(
            (user, profile.received_messages.filter(sender=user)[0]))

    new_messages2 = []
    for user in users2:
        new_messages2.append(
            (user, profile.sent_messages.filter(recipient=user)[0]))
    cleaned_messages = user_inbox(profile)
    context = {'user_messages': user_messages, 'new_messages': new_messages,
               'sent_messages': sent_messages, 'new_messages2': new_messages2, 'cleaned_messages': cleaned_messages}
    return render(request, 'users/inbox.html', context,)


def message(request, pk):
    profile = request.user.profile
    recipient = Profile.objects.get(id=pk)
    # user_messages2 = profile.messages.filter(sender=pk)
    user_messages = Message.objects.filter(Q(sender=pk, recipient=profile) | Q(
        recipient=pk, sender=profile)).order_by('created')

    read_messages = Message.objects.filter(sender=pk, recipient=profile)
    read_messages.update(is_read=True)
    # user_messages.update(is_read=True)
    # User.objects.all().order_by('-id')[:10]
    message_form = MessageForm()

    if request.method == 'POST':
        message_form = MessageForm(request.POST)

        if message_form.is_valid:
            message = message_form.save(commit=False)
            message.sender = profile
            message.recipient = recipient
            message.save()
            return redirect('message', pk=pk)

    user_messages2 = user_messages.reverse()
    paginated_messages = paginate_messages(request, user_messages2, 5)
    # print(paginated_messages)

    context = {'user_messages': user_messages, 'message_form': message_form,
               'recipient': recipient, 'paginated_messages': paginated_messages}

    return render(request, 'users/messages.html', context)


def sendMessage(request):
    form = CreateMessageForm()
    profile = request.user.profile
    if request.method == 'POST':
        form = CreateMessageForm(request.POST)
        if form.is_valid:
            form = form.save(commit=False)
            Message.objects.create(
                sender=profile, recipient=form.recipient, body=form.body)
            return redirect('inbox')
    context = {'form': form}
    return render(request, 'users/create_message.html', context)


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'home')
        else:
            messages.error(request, 'Username OR password is incorrect')
    return render(request, 'users/login_register.html')


def demoLogin(request):
    username = 'johnsmith60'
    password = 'fdjklfsd23423!'
    email = 'hello1001@email.com'

    try:

        a = User.objects.get(username=username)
        a.delete()

    except:
        pass

    User.objects.create_user(username=username, password=password, email=email)
    demo_account = Profile.objects.get(username=username)
    demo_account.first_name = "Johnny (Demo)"
    demo_account.last_name = "C"
    demo_account.email = "hello001@email.com"
    demo_account.save()
    user = authenticate(request, username=username, password=password,
                        backend='django.contrib.auth.backends.ModelBackend')
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return render(request, 'users/feed.html')
