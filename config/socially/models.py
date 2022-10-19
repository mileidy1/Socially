from django.db import models
from django.contrib.auth.models import User

class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    socially = models.ForeignKey('Socially', on_delete=models.CASCADE)


class Socially(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user')
    interaction = models.ManyToManyField(User, through= Action)
    social_text = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add = True)
    number_of_likes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.social_text

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


