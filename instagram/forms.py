from django import forms

from instagram.models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('author', 'photo', 'text')


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)


