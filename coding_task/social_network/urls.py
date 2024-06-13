from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.user_signup, name='user_signup'),
    path('login/', views.user_login, name='user_login'),
    path('users/', views.list_users, name='list_users'),
    path('users/update/', views.update_user, name='update_user'),
    path('users/delete/', views.delete_user, name='delete_user'),
    path('users/search/', views.search_users, name='search_users'),
    path('users/follow/', views.follow_user, name='follow_user'),
    path('users/unfollow/', views.unfollow_user, name='unfollow_user'),
    path('discussions/', views.create_discussion, name='create_discussion'),
    path('discussions/update/', views.update_discussion, name='update_discussion'),
    path('discussions/delete/', views.delete_discussion, name='delete_discussion'),
    path('discussions/tags/', views.list_discussions_by_tag, name='list_discussions_by_tag'),
    path('discussions/search/', views.list_discussions_by_text, name='list_discussions_by_text'),
    path('discussions/detail/', views.get_discussion_detail, name='get_discussion_detail'),
    path('comments/add/', views.add_comment, name='add_comment'),
    path('comments/update/', views.update_comment, name='update_comment'),
    path('comments/delete/', views.delete_comment, name='delete_comment'),
    path('discussions/like/', views.like_discussion, name='like_discussion'),
    path('comments/like/', views.like_comment, name='like_comment'),
]