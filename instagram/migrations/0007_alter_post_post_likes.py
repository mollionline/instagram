# Generated by Django 4.0.3 on 2022-04-06 18:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instagram', '0006_delete_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='post', to=settings.AUTH_USER_MODEL),
        ),
    ]