# Generated by Django 3.2.9 on 2022-03-09 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(blank=True, max_length=3000, null=True),
        ),
    ]
