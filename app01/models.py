from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class Profile(models.Model):
    badge = models.CharField(max_length=14,default="pas de badge !")
    classe = models.TextField(default="pas de classe !")
    password = models.TextField(default="pas de mot de passe !")
    matiere = models.TextField(default="pas de classe !")
    heure_de_reception = models.TextField(default=" Null (not defined yet) ")
    
    dm = models.TextField(default=".")
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f" Profile de {self.user.username} "
    

class Filiere01(models.Model):
    filiere = models.TextField(unique=True, default="Suppr_Error")
    
    
class classe01(models.Model):
    classe = models.TextField(unique=True, default="Suppr_Error")
    
    
class Matiere(models.Model):
    matiere = models.TextField(default="pas de matiere !")
    

class changement_nom_prernom(models.Model):
    nom_avant = models.CharField(max_length=25)
    prenom_avant = models.CharField(max_length=25)
    nom_apr = models.CharField(max_length=25)
    prenom_apr = models.CharField(max_length=25)
    
    
class posts(models.Model):
    titre=models.CharField(max_length=50)
    date=models.DateField()
    text=models.TextField()
    type=models.CharField(max_length=8 ,default=".")
    
    
class emplous_temps(models.Model):
    titre = models.CharField(max_length=80)
    emplois = models.TextField()
    
    
class certificat(models.Model):
    nom = models.CharField(max_length=25)
    prenom = models.CharField(max_length=25)
    heure = models.CharField(max_length=20)
    motif = models.TextField()
    dcr = models.TextField()
    
    
class pub0(models.Model):
    nom_complet = models.CharField(max_length=23)
    pub = models.ImageField()
    message = models.TextField()
    dcr = models.CharField(max_length=3,default="non")
    
    def delete(self, *args, **kwargs):
        if self.pub:
            if os.path.isfile(self.pub.path):
                os.remove(self.pub.path)
        super().delete(*args, **kwargs)
        

class contact01(models.Model):
    nom_complet = models.CharField(max_length=30)
    numero = models.CharField(max_length=10)
    message = models.TextField()
    qui = models.CharField(max_length=22 ,default="")
    
    
class Groupe(models.Model):
    membres = models.ManyToManyField(User,related_name="groupe")
    nom = models.CharField(max_length=50)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE ,related_name="groupes_crees")
    date_creation = models.DateTimeField(auto_now_add=True)
    
class Message(models.Model):
    text = models.TextField()
    image = models.ImageField(blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name="messages")
    signale = models.CharField(max_length=40 ,default='.')
    
    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
        
        
