# Generated by Django 4.1 on 2022-10-04 22:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socially', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Social',
            new_name='Socially',
        ),
    ]
