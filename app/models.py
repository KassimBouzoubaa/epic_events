from django.db import models
from collaborateur.models import Commercial, Support, Gestion


class Client(models.Model):
    information = models.CharField(max_length=200)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    nom_entreprise = models.CharField(max_length=200)
    date_de_creation = models.DateTimeField(auto_now_add=True)
    derniere_maj = models.DateTimeField(auto_now=True)
    commercial_id = models.ForeignKey(Commercial,on_delete=models.CASCADE , related_name='clients')
    
    def commercial_name(self):
        return self.commercial_id.nom_complet

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"
    
    @property
    def contact(self):
        return f"{self.email} {self.telephone}"

class Contract(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE ,related_name='contracts')
    commercial_id = models.ForeignKey(Commercial,on_delete=models.CASCADE , related_name='contracts')
    montant_total = models.IntegerField(default=0)
    montant_restant = models.IntegerField(default=0)
    date_de_creation = models.DateTimeField(auto_now_add=True)
    statut = models.BooleanField(default=False)
    
    def commercial_name(self):
        return self.commercial_id.nom_complet
    

class Event(models.Model):
    name = models.CharField(max_length=200)
    contract_id = models.ForeignKey(Contract, on_delete=models.CASCADE ,related_name='events')
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='events')
    date_de_debut = models.DateTimeField()
    date_de_fin = models.DateTimeField()
    support_id = models.ForeignKey(Support,on_delete=models.CASCADE , related_name='events')
    lieu = models.CharField(max_length=100)
    participants = models.IntegerField()
    notes = models.CharField(max_length=100)
    
    def client_name(self):
        return self.client.nom_complet

    def client_contact(self):
        return self.client.contact
    
    def support_contact(self):
        return self.support_id.nom_complet