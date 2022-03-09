from django.contrib.auth import get_user_model
from django.db import models

from accounts.models import Profile


class CustomModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Entity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания", blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = CustomModelManager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save(update_fields=['is_deleted', ])

    class Meta:
        abstract = True


class Post(Entity):
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.SET_DEFAULT,
                               default=1,
                               related_name='posts',
                               verbose_name='Автор'
                               )
    photo = models.ImageField(upload_to='posts/photos',
                              verbose_name='Фото',
                              null=False,
                              blank=False)
    text = models.TextField(max_length=3000,
                            null=True,
                            blank=True)

    def __str__(self):
        return f"{self.pk}. {self.author}"

    class Meta:
        unique_together = (('author', 'text'), )
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        permissions = [
            ('can_use_it', 'Можно использовать это')
        ]


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="likes")

    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name="likes")

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name="unique_like"),
        ]

class Comment(Entity):
    post = models.ForeignKey('instagram.Post',
                             related_name='comments',
                             on_delete=models.CASCADE,
                             verbose_name='Пост')
    text = models.TextField(max_length=400,
                            verbose_name='Комментарий')
    author = models.ForeignKey(
                            get_user_model(),
                            on_delete=models.SET_DEFAULT,
                            related_name='comments',
                            default=1,
                            verbose_name='Автор'
                            )

    def __str__(self):
        return self.text[:20]
