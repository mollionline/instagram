# Generated by Django 3.2.9 on 2022-03-10 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0005_alter_post_unique_together'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Like',
        ),
    ]
