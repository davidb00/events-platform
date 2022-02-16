from users.models import Profile
from django.db import models
import uuid


class Group(models.Model):
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    name = models.CharField(max_length=50, unique=True)
    owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.SET_NULL)
    members = models.ManyToManyField(Profile,blank=True,related_name="members")
    img_url = models.URLField(max_length=200,blank=True)
    description = models.TextField(max_length=500,blank=True,null=True)
    
    def __str__(self) -> str:
        return str(self.name)
