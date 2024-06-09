from django.contrib.auth.models import AbstractUser
from django.db import models

class Collaborateur(AbstractUser):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()

    def nom_complet(self):
        return f"{self.nom} {self.prenom}"

class Commercial(Collaborateur):
    class Meta:
        verbose_name = "Commercial"
        verbose_name_plural = "Commerciaux"

    def save(self, *args, **kwargs):
        self.role = 'commercial'
        super().save(*args, **kwargs)
        
    def create_client():
        pass
    
    def update_client():
        pass
    
    def update_contract():
        pass
    
    def filter_contract():
        pass
    
    def create_event():
        pass

class Support(Collaborateur):
    class Meta:
        verbose_name = "Support"
        verbose_name_plural = "Supports"

    def save(self, *args, **kwargs):
        self.role = 'support'
        super().save(*args, **kwargs)

    def filter_event():
        pass
    
    def update_event():
        pass
    
class Gestion(Collaborateur):
    class Meta:
        verbose_name = "Gestion"
        verbose_name_plural = "Gestions"

    def save(self, *args, **kwargs):
        self.role = 'gestion'
        super().save(*args, **kwargs)
        
    def create_collaborateur():
        pass
    
    def update_collaborateur():
        pass
    
    def delete_collaborateur():
        pass
    
    def create_contract():
        pass
    
    def update_contract():
        pass
    
    def filter_event():
        pass
    
    def update_event():
        pass