from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework.authtoken.models import Token

# Create your models here.

    
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
    
    
class Tournee(models.Model):
    id_tournee = models.AutoField(primary_key=True )
    livreur = models.ForeignKey(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return f"{self.livreur.username}"


class Commande(models.Model):
    id_commande = models.AutoField(max_length=50, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    default = models.BooleanField(default=False)
    est_modifie = models.BooleanField(default=False)
    tournee = models.ForeignKey(Tournee, on_delete=models.CASCADE)
    est_livre = models.BooleanField(default=False)
    
    def __str__(self):
        return   f"commande : {self.id_commande}"  

class Article(models.Model):
    id_article = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255 )
    taille = models.CharField(max_length=1, choices=[('S', 'Small'), ('M' , 'Medium'), ('L' , 'Large')], null=True) 
    types = models.CharField(max_length=1, choices=[('C', 'Caisse'), ('U' , 'Unite')]) # C = caisse  , U = unite

    def __str__(self):
        return f"Article {self.id_article} - Nom: {self.nom}, Taille: {self.taille}, Type: {self.types}"
    

class Caisse(models.Model):
    id_caisse = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    nbr_articles = models.IntegerField()
    test = models.IntegerField(default=0)

    def __str__(self):
        return self.id_caisse   

class Caisse_commande(models.Model):
    id_caisse_commande = models.AutoField(primary_key=True)
    
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, unique=True)
    caisse = models.ForeignKey(Caisse, on_delete=models.CASCADE, unique=True)
    nbr_caisses = models.DecimalField(max_digits=5, decimal_places=2)
    unite = models.IntegerField(default=0)

    def __str__(self):
        return self.id_caisse_commande