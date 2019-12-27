from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
#import misaka
from django.contrib.auth import get_user_model
user = get_user_model()

from django import template
register = template.Library()

class Group(models.Model):
    name = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    #description_html = models.TextField(editable=False, default='',blank=True)
    members = models.ManyToManyField(user, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        #self.description_html = misaka.html(self.description)
        super().save(*args,**kwargs)
    
    def get_absolute_url(self):
        return reverse('Group:SingleGroup',)

    class Meta:
        ordering= ['name']


class GroupMember(models.Model):
    Group = models.ForeignKey(Group,related_name='memberships',on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(user, related_name='user_groups', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.user.username


    class Meta:
        unique_together = ('Group','user')
