from django.db import models
from django.contrib.auth.models import User

class Etudiant(models.Model) : 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    filiere = models.CharField(max_length=150)
    telephone = models.CharField(max_length=150)
    photo = models.ImageField(
        upload_to='profiles/',
        default='profiles/default.png'
    )
    def __str__(self):
        return self.user.username

class Trajet(models.Model) : 
    conducteur_ref = models.ForeignKey(
        Etudiant, 
        on_delete=models.CASCADE, 
        related_name='trajets_crees'
    )
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    date = models.DateField()
    heure_depart = models.TimeField() 
    nb_place = models.IntegerField()
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return f"{self.ville_depart} to {self.ville_arrivee} on {self.date} at {self.heure_depart}"

class Reservation(models.Model):
    date_reservation = models.DateTimeField(auto_now_add=True)
    
    etudiant = models.ForeignKey(
        Etudiant, 
        on_delete=models.CASCADE, 
        related_name='reservations'
    )
    trajet = models.ForeignKey(
        Trajet, 
        on_delete=models.CASCADE, 
        related_name='reservations'
    )
    def __str__(self):
        return f"Reservation {self.id} for {self.etudiant.user.username} on trajet {self.trajet}"