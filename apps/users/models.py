from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.TextField(unique=True)
    email = models.EmailField(unique=True)
    role = models.TextField() # client, agent
    created_at = models.DateTimeField()


    def __str__(self):
        return self.username