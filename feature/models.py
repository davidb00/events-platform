from django.db import models
from users.models import Profile
import uuid


class UserPost(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post_image = models.ImageField(blank=True, null=True)
    caption = models.CharField(max_length=50)
    body = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.body[0:20]


class PostLike(models.Model):
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name="liker")
    created = models.DateTimeField(auto_now_add=True)
