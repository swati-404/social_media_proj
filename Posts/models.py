from django.db import models
from django.urls import reverse
from django.conf import settings
import datetime
# from django.utils.text import slugify
# Create your models here.
#import misaka
from Groups.models import Group
from django.contrib.auth import get_user_model
user = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(user, related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(datetime.datetime.now())
    message = models.TextField(max_length=100)
    group = models.ForeignKey(Group, related_name="posts", on_delete = models.CASCADE, null = True, blank= True)


    def __str__(self):
        return self.message

    # def save(self, *args,**kwargs):
        #     se

    def get_absolute_url(self):
        return reverse('posts:single',kwargs={'username':self.user.username,'pk':self.pk})

    
    class Meta:
        ordering = ['-created_at']
        unique_together =['user','message']




