from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    nom = models.CharField(max_length=100)
    date_de_creation = models.DateTimeField(auto_now_add=True)
    derniere_maj = models.DateTimeField(auto_now=True)


class Collaborateur(AbstractUser):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name="collaborateurs", null=True
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["nom"]

    def nom_complet(self):
        return f"{self.nom} {self.prenom}"
