from django.db import models
from django.contrib.auth.models import BaseUserManager,PermissionsMixin,AbstractBaseUser
from django.conf import settings
from django.utils import timezone

class UserManager(BaseUserManager):

    def create_user(self,name,email,role,password,manager=None,agent=None):
        if not email:
            raise ValueError('Email has been provided')
        if not name:
            raise ValueError('Name has to be provided')
        if not password:
            raise ValueError('User must have a password')
        if not role:
            raise ValueError('Role has to be provided')
        if not manager or not agent:
            raise ValueError('User has to be connected to a manager or an agent')

        user = self.model (
            email = self.normalize_email(email),
            name=name,
            manager=manager,
            role=role,
            agent=agent 
        )
        user.set_password(password)
        user.save()
        return user 
    
    def create_superuser(self,name,email,password):
        if not email:
            raise ValueError('Email has been provided')
        if not name:
            raise ValueError('Name has to be provided')
        if not password:
            raise ValueError('User must have a password')
        
        user = self.model(
            email = self.normalize_email(email),
            name=name
        )
        user.set_password(password)
        user.is_staff, user.is_superuser, user.is_admin = True, True, True
        user.save()
        return user
    
class User(AbstractBaseUser,PermissionsMixin):
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
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()
    
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