from django.shortcuts import render
from django.contrib.auth.mixins import(LoginRequiredMixin,PermissionRequiredMixin)
from django.urls import reverse
from django.views import generic  
from django.contrib import messages  
from . import models 
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
# from django.views.generic import ListView, DetailView, CreateView
# Create your views here.


class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields =('name', 'description')
    model = models.Group

    def form_invalid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class SingleGroup(generic.DetailView):
    model = models.Group

   

    


class ListGroups(generic.ListView):
    model = models.Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('Group:SingleGroup', kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args,**kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        
        try:
            GroupMember.object.create(user = self.request.user, group=group)

        except IntegrityError:
            messages.warning(self.request,('warning aleady member!'))
        else:
            messages.success(self.request,'You are now member!')
        
        return super().get(request,*args,**kwargs)


class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('Group:SingleGroup', kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        
        try:
            membership = Group.GroupMember.object.filter(
                user = self.request.user,
                Group_slug = self.kwargs.get('slug')
            ).get()

        except Group.GroupMember.DoesNotExist:
            messages.warning(self.request,'Sorry you are ot in this group')
        
        else:
            membership.delete()
            messages.success(self.request,'You have left the group!')

        return super().get(request,*args,**kwargs)