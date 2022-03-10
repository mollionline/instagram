from django.urls import path

from instagram.views.comment_view import PostCommentCreateView, PostCommentUpdateView, PostCommentDeleteView

from instagram.views.post_view import like_view, PostCreateView, PostDetailView, PostListView, DeleteView

urlpatterns = []

post_urls = [
    path('post/add', PostCreateView.as_view(), name='create_post'),
    path('post/<int:pk>', PostDetailView.as_view(), name='detail_post'),
    path('', PostListView.as_view(), name='list_post'),
    path('post/<int:pk>/delete', DeleteView.as_view(), name='delete_post'),
    path('like/<int:pk>', like_view, name='like_post'),
]

comment_urls = [
    path('post/<int:pk>/comment', PostCommentCreateView.as_view(), name='create_comment'),
    path('post/comment/<int:pk>/update', PostCommentUpdateView.as_view(), name='update_comment'),
    path('post/comment/<int:pk>/delete', PostCommentDeleteView.as_view(), name='delete_comment')
]

urlpatterns += post_urls
urlpatterns += comment_urls
