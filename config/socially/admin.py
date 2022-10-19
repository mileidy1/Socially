from django.contrib import admin
from .models import Action, FollowersCount, LikePost, Socially, Profile

admin.site.register(Socially)
admin.site.register(Profile)
admin.site.register(LikePost)
admin.site.register(Action)
admin.site.register(FollowersCount)