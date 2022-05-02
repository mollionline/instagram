from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from instagram.models import Post
from api_v1.serializers import PostSerializer, PostLikesSerializer
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from api_v1.permissions import IsPostUsers


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsPostUsers]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return super().get_permissions()


class LikesViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin,
                   mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostLikesSerializer
    permission_classes = [IsAuthenticated]


class LogoutView(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user.auth_token.delete()
        return Response({'status': 'ok'})


class LikesPostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    model = Post

    def post(self, request, *args, **kwargs):
        post_pk = kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_pk)
        if self.request.user not in post.post_likes.all():
            post.post_likes.add(self.request.user.pk)
            return JsonResponse({'like': '+'})
        else:
            post.post_likes.remove(self.request.user.pk)
            return JsonResponse({'like': '-'})
