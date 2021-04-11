"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from user_profile.views import  follow_view, profile_view, unfollow_view, error_404_view, error_500_view
from django.contrib import admin
from django.urls import path
from authentication import views as auth
from post import views as post

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', post.homepage, name='homepage'),
    path('signup/', auth.SignUpView.as_view(), name='signup'),
    path('login/', auth.LoginView.as_view(), name='login'),
    path('logout/', auth.LogoutView.as_view(), name='logout'),
    path('profile/<int:user_id>/', profile_view, name='profile'),
    path('follow/<int:user_id>/', follow_view, name='follow'),
    path('unfollow/<int:user_id/', unfollow_view, name='unfollow'),
    path('404/',error_404_view, name='404'),
    path('500/',error_500_view, name='500'),
]



auth_handler404 = 'authentication.views.error_404_view'
notify_handler404 = 'notification.views.error_404_view'
post_handler404 = 'post.views.error_404_view'
user_handler404 = 'user_profile.views.error_404_view'
auth_handler500 = 'authentication.views.error_500_view'
notify_handler500 = 'notification.views.error_500_view'
post_handler500 = 'post.views.error_500_view'
user_handler500 = 'user_profile.views.error_500_view'