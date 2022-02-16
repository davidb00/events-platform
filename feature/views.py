from django.shortcuts import render
from feature.models import UserPost


def feed(request):

    user_posts = UserPost.objects.all()

    context = {"user_posts": user_posts}

    return render(request, 'feature/feed.html', context)
