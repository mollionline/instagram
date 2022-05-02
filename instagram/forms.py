from django import forms

from instagram.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('photo', 'text')


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
