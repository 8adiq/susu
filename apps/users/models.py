from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission


class User(AbstractUser):
    username = models.TextField(unique=True)
    email = models.EmailField(unique=True)
    role = models.TextField(max_length=10, 
        choices=[ 
        ('agent', 'Agent'),
        ('trader', 'Trader'),
        ])
    created_at = models.DateTimeField()

    def __str__(self):
        return self.username