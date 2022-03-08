from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from instagram.models import Like, Post


@method_decorator(login_required, name='dispatch')
class LikeView(View):
    def get_success_url(self):
        return reverse('detail_post', kwargs={"pk": self.kwargs.get("pk")})

    def get(self, request, *args, **kwargs):
        like = Like()
        like.post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        like.user = self.request.user
        like.save()
        return redirect(self.get_success_url())

    def get_like_url(self):
        return reverse('like', kwargs={"pk": self.id})
