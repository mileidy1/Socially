from django.db import models
from django.contrib.auth.models import User

class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    socially = models.ForeignKey('Socially', on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    comment_time = models.DateTimeField(null=True)
    shared = models.BooleanField(default=False)
    shared_time = models.DateTimeField(null=True)
    saved = models.BooleanField(default=False)

class Socially(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user')
    interaction = models.ManyToManyField(User, through= Action)
    social_text = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add = True)
    like = models.ManyToManyField(User, related_name ='likes')
    
    def total_like(self):
        return self.like.count()

    def __str__(self):
        return self.social_text

