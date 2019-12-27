from django.shortcuts import render
# from django.contrib.auth.models import User
#from django.core.urls import reverse_lazy
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views import generic
from braces.views import SelectRelatedMixin
from . import models
from . import forms
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
user = get_user_model

# Create your views here.
 
class PostList(SelectRelatedMixin,generic.ListView):
    models = models.Post
    select_related = ('user','Group')


class UsrPosts(generic.ListView):
    models = models.Post
    template_name ='posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = user.objects.prefetch_related('post').get(username__iexact = self.kwargs.getme)
            
        except user.DoesNotExist:
            raise Http404
        
        else:
            return self.post_user.posts.all()


        def get_context_data(self,**kwargs):
            context = super().get_context_data(**kwargs)
            context['post_user'] = self.post_user
            return context


class PostDetail(SelectRelatedMixin,generic.DetailView):
    models = models.Post
    select_related=('user','group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(use_username__iexact = self.kwargs.get('username'))


class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    fields =('message','group')
    models = models.Post
    
    def form_invalid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    models = models.Post
    select_related = ('user','Group')
    success_url = reverse_lazy('Post:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)