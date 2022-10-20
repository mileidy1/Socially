# Generated by Django 4.1 on 2022-10-19 22:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socially', '0004_followerscount_likepost_remove_action_comment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socially',
            name='number_of_likes',
        ),
        migrations.AddField(
            model_name='action',
            name='saved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='action',
            name='shared',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='action',
            name='shared_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='socially',
            name='like',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
