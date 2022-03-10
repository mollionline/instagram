

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, ListView
from instagram.helpers import FormView as CustomFormView, SearchView, DetailView
from instagram.forms import PostForm, SearchForm
from django.urls import reverse

from django.views.generic import RedirectView

from instagram.models import Post, Comment


def like_view(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.post_likes.add(request.user)
    return HttpResponseRedirect(reverse('detail_post', args=[str(pk)]))


class PostDetailView(DetailView):
    context_object_name = 'post'
    template_name = 'post/detail_post_view.html'
    model = Post

    def get_context_data(self, **kwargs):
        kwargs['post'] = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return super().get_context_data(**kwargs)


class DeleteView(RedirectView):
    pattern_name = 'list_post'

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get('pk'))
        post.delete()
        return redirect(self.get_redirect_url())


class PostListView(LoginRequiredMixin, ListView):
    template_name = 'post/list_post_view.html'
    model = Post
    ordering = ('-created_at',)
    context_object_name = 'posts'


class PostCreateView(LoginRequiredMixin, CustomFormView):
    template_name = 'post/create_post_view.html'
    form_class = PostForm
    redirect_url = ''

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=self.request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('list_post')
        return render(request, self.template_name,
                      context={
                          'form': form
                      })



