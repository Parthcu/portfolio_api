"""
URL configuration for blogger project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from virtual import views
from virtual.views import SuperuserLoginView 
from django.contrib.auth import views as auth_views
from virtual.views import (
    create_profile_pic, get_all_profile_pics, delete_profile_pic,
    create_blog_post, get_all_blog_posts, delete_blog_post,
    create_research_post, get_all_research_posts, delete_research_post,
    create_text_post, get_all_text_posts, delete_text_post,send_email,SuperuserLoginView
)

urlpatterns = [
    # ProfilePic URLs
    path('profile-pic/create/', create_profile_pic, name='create_profile_pic'),
    path('profile-pic/all/', get_all_profile_pics, name='get_all_profile_pics'),
    path('profile-pic/delete/<int:pk>/', delete_profile_pic, name='delete_profile_pic'),

    # BlogPost URLs
    path('blog-post/create/', create_blog_post, name='create_blog_post'),
    path('blog-post/all/', get_all_blog_posts, name='get_all_blog_posts'),
    path('blog-post/all/<int:post_id>/',get_all_blog_posts, name='get_single_blog_post'),
    path('blog-post/delete/<int:pk>/', delete_blog_post, name='delete_blog_post'),

    # ResearchPost URLs
    path('research-post/create/', create_research_post, name='create_research_post'),
    path('research-post/all/', get_all_research_posts, name='get_all_research_posts'),
    path('research-post/all/<int:post_id>/', get_all_blog_posts, name='get_single_blog_post'),
    path('research-post/delete/<int:pk>/', delete_research_post, name='delete_research_post'),

    # TextPost URLs
    path('text-post/create/', create_text_post, name='create_text_post'),
    path('text-post/all/', get_all_text_posts, name='get_all_text_posts'),
    path('text-post/delete/<int:pk>/', delete_text_post, name='delete_text_post'),

    # Superuser login URL
    path('api/login/', SuperuserLoginView.as_view(), name='superuser_login'),
    path('admin/', admin.site.urls),
    path('api/send-email/', send_email, name='send-email'),
]
