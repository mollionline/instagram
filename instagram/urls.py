from django.urls import path


from instagram.views.like_view import LikeView
from instagram.views.post_view import PostCreateView, PostDetailView, PostListView, DeleteView

urlpatterns = []

post_urls = [
    path('post/add', PostCreateView.as_view(), name='create_post'),
    path('post/<int:pk>', PostDetailView.as_view(), name='detail_post'),
    path('posts', PostListView.as_view(), name='list_post'),
    path('post/<int:pk>/delete', DeleteView.as_view(), name='delete_post'),
    path('post/like/<int:pk>', LikeView.as_view(), name='like')
]


urlpatterns += post_urls

