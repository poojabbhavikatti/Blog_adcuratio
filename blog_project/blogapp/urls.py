from django.urls import path 
from blogapp import views
app_name="blogapp"

from .views import (
    blog_post_list,
    blog_post_detail,
    blog_post_create,
    blog_post_update,
    blog_post_delete,
    UserRegistrationAPIView,
)

urlpatterns = [
    path('posts/', blog_post_list, name='blog_post_list'),
    path('posts/<int:pk>/', blog_post_detail, name='blog_post_detail'),
    path('posts/create/', blog_post_create, name='blog_post_create'),
    path('posts/<int:pk>/update/', blog_post_update, name='blog_post_update'),
    path('posts/<int:pk>/delete/', blog_post_delete, name='blog_post_delete'),
    path('register/', UserRegistrationAPIView.as_view(), name='user_registration'),
]

