from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

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


class LikesViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostLikesSerializer
    permission_classes = [IsAuthenticated]

