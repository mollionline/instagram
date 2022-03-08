from django.contrib import admin

# Register your models here.
from instagram.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'photo', 'text', 'created_at')
    list_filter = ['author']
    search_fields = ['text', 'author']
    fields = ['author', 'text', 'created_at', 'photo']
    readonly_fields = ['created_at']


admin.site.register(Post, PostAdmin)
