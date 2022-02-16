from .models import Message
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q


def paginate_messages(request, messages, results):

    try:
        page = request.GET['page']
    except:
        page = paginate_messages

    paginator = Paginator(messages, results)
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)
    return messages


def user_inbox(user):

    messages = Message.objects.filter(
        Q(sender=user) | Q(recipient=user)).order_by('created')
    reverse_user = set()

    for message in messages:
        reverse_user.add(message.sender.id)
        reverse_user.add(message.recipient.id)

    reverse_user.remove(user.id)

    cleaned_messages = []

    for reverse_user in reverse_user:
        cleaned_messages.append(Message.objects.filter(
            Q(sender=user, recipient=reverse_user) | Q(recipient=user, sender=reverse_user))[0])

    result = sorted(cleaned_messages, key=lambda x: x.created, reverse=True)

    return result
