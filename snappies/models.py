from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework.authtoken.models import Token

# Create your models here.

class Commande(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    value = models.CharField(max_length=100)


    def __str__(self):
        return self.value
    
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Le nom d'utilisateur doit être spécifié.")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        user = self.create_user(username, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id_user = models.AutoField( primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username



def create_token_for_user(sender, instance, created, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)

models.signals.post_save.connect(create_token_for_user, sender=User)
        
        
        
        
class Client(models.Model):
    id_client = models.AutoField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    numero_telephone = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)

    def __str__(self):
        return self.name