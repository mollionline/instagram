from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView
from ..helpers import DeleteView
from instagram.forms import CommentForm
from instagram.models import Comment, Post
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostCommentCreateView(CreateView):
    model = Comment

    form_class = CommentForm
    template_name = 'post/detail_post_view.html'


    def get_success_url(self):
        return reverse('detail_post', kwargs={'pk': self.kwargs.get('pk')})


    def post(self, request, *args, **kwargs):
        post_pk = kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_pk)
        form = self.form_class(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = self.request.user
            comment.save()
            return redirect(self.get_success_url())
        return render(request, self.template_name,
                      context={
                          'post': post,
                          'form': form
                      })


class PostCommentUpdateView(PermissionRequiredMixin, UpdateView):
    model = Comment
    template_name = 'comment/post_comment_update.html'
    context_object_name = 'comment'
    form_class = CommentForm
    permission_required = 'post.change_comment'

    def has_permission(self):
        return (self.get_object().author == self.request.user or
                self.request.user.has_perm(self.permission_required))

    def get_success_url(self):
        return reverse('detail_post', kwargs={'pk': self.object.post.pk})


class PostCommentDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'comment/post_comment_delete.html'
    model = Comment
    confirm_deletion = True
    context_object_name = 'comment'
    permission_required = 'post.delete_comment'

    def test_func(self):
        return self.get_object().author == self.request.user or self.request.user.has_perm(
            self.permission_required)

    def get_success_url(self):
        return reverse('detail_post', kwargs={'pk': self.object.post.pk})