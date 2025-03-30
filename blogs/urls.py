from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    MyDraftListView,
    MyPostListView,
    UserPostListView,
    CommentUpdateView,
    CommentDeleteView,
    Search,
    FeedbackCreateView,
    Topic
    )
from users import views as user_views

urlpatterns = [
    path('', PostListView.as_view(), name='blogs-index'),
    path('s/',Search.as_view(),name='search'),
    path('topic/<topic>',Topic.as_view(),name='topic'),
    path('post/<int:pk>/',PostDetailView.as_view(),name='post-details'),
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/confirm_publish/',views.confirm_publish,name='post-publish'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
    path('post/<int:pk>/',PostDetailView.as_view(),name='post-details'),
    path('<username>/draft_list/',MyDraftListView.as_view(),name='draft-list'),
    path('<username>/post_list/',MyPostListView.as_view(),name='post-list'),
    path('<username>/profile/',user_views.user_profile,name='user-profile'),
    path('<username>/posts/',UserPostListView.as_view(),name='user-post-list'),
    path('post/<int:pk>/add_comment',views.AddComment,name='add-comment'),
    path('post/<int:pk>/update_comment',CommentUpdateView.as_view(),name='update-comment'),
    path('post/<int:pk>/delete_comment/',CommentDeleteView.as_view(),name='comment-delete'),
    path('<int:pk>/preference/<int:user_preference>/', views.post_preference, name='post-preference'),
    path('post/<int:blog_id>/<int:comment_id>/preference/<int:user_preference>/', views.comment_preference, name='comment-preference'),
    path('post/<int:blog_id>/feedback',FeedbackCreateView.as_view(),name='post-feedback')
]
