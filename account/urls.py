from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
# from django.contrib.auth.views.LoginView
# from django.contrib.auth.views.LogoutView

app_name = 'account'

urlpatterns = [ 
    path('', auth_views.LoginView.as_view(template_name='account/login.html'),name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'),name='login'),
    # default Logout
    # path('logout',  auth_views.LogoutView.as_view(), name ='logout'),
    path('logout',  auth_views.LogoutView.as_view(template_name='account/logout.html'), name ='logout'),
    path('signup/', views.SignUp.as_view(template_name='account/signup.html'),name='signup'),
]
