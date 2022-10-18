
from django.db import models
from django.contrib.auth.models import User

class Friendship (models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend1_set')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend2_set')
    created = models.DateTimeField(auto_now_add= True)


