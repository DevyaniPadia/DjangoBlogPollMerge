from django.urls import path, include
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<slug:slug>', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('add_category/', views.add_category,name="add_category"),
    path('category_detail/<slug:slug>', views.category_detail,name="category_detail"),
    path('add_tag/', views.tagged,name="add_tag"),
    path('tag_detail/<slug:slug>', views.tag_detail,name="tag_detail"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('update/', views.update, name='update'),
    path('profile/', views.profile, name='profile'),

]