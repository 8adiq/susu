from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.conf import settings
from django.utils import timezone

class User(AbstractUser):
    MANAGER = 'manager'
    AGENT = 'agent'
    CLIENT = 'client'

    ROLE_CHOICE = [
        (MANAGER,'manager'),
        (AGENT,'agent'),
        (CLIENT,'client')
    ]

    name = models.TextField(unique=True,null=False,max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10,choices=ROLE_CHOICE)
    manager= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name='agents',null=True,limit_choices_to={'role':MANAGER},help_text='manager oversees this client or agent')
    agent = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name='clients',null=True,limit_choices_to={'role':AGENT}, help_text='agent oversees this client')
    job = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = ['name']
    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        """custom save function that checks for manager or agent assignment before a new user is created"""
        if self.role == self.AGENT and not self.MANAGER:
            raise ValueError('A manager has to be assigned to an agent')
        if self.role == self.CLIENT and not (self.AGENT or self.MANAGER):
            raise ValueError('A manager or agent has to be assigned to the client')
        super().save(*args,**kwargs)

    def __str__(self):
        return f' name :{self.username}, role: {self.role}'