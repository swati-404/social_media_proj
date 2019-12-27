from django.contrib import admin
from django.urls import path,include
from . import views

app_name='Group'

urlpatterns =[
    path('',views.ListGroups.as_view(), name='all'),
    path('new/', views.CreateGroup.as_view(), name='CreateGroup'),
    path('post/in/<int:pk2>/',views.SingleGroup.as_view(), name='SingleGroup'),
    path('join',views.JoinGroup.as_view(), name='JoinGroup'),
    path('leave',views.LeaveGroup.as_view(), name='LeaveGroup')

]

