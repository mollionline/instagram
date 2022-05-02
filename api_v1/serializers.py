from rest_framework import serializers
from instagram.models import Post


class PostSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(
        max_length=None, allow_empty_file=False,
        use_url=True, required=False
    )

    class Meta:
        model = Post
        fields = ['id', 'author', 'photo', 'text', 'post_likes']
        read_only_fields = ['id']


class PostLikesSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(
        max_length=None, allow_empty_file=False,
        use_url=True, required=False
    )

    class Meta:
        model = Post
        fields = ['id', 'photo', 'post_likes']
        read_only_fields = ['id']
