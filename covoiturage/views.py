from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from httpx import request
from django.db.models import Count, F
from covoiturage.models import Etudiant, Trajet,Reservation

def register_view(request):
    if request.method == 'POST':

        nom = request.POST['nom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        password = request.POST['password']
        filiere = request.POST['filiere']
        telephone = request.POST['telephone']

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email déjà utilisé")
            return redirect('register')

        user = User.objects.create_user(
            username=email,
            first_name=prenom,
            last_name=nom,
            email=email,
            password=password
        )

        Etudiant.objects.create(
            user=user,
            filiere=filiere,
            telephone=telephone
        )

        messages.success(request, "Compte créé avec succès")
        return redirect('login')
    
    return render(request, 'auth/register.html')


def login_view(request):

    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        else:

            messages.error(
                request,
                "Email ou mot de passe incorrect"
            )
            return redirect('login')

    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):

    trajet = Trajet.objects.annotate(

        nb_reservations=Count('reservations'),

        places_restantes=F('nb_place') - Count('reservations')

    ).filter(

        places_restantes__gt=0

    ).exclude(

        conducteur_ref__user=request.user

    ).order_by('?').first()

    if trajet:

        trajet.place_disponible = (
            trajet.nb_place -
            trajet.reservations.count()
        )

        trajet.est_reserver = Reservation.objects.filter(
            etudiant=Etudiant.objects.get(user=request.user),
            trajet=trajet
        ).exists()

        trajet.est_complet = (
            trajet.place_disponible <= 0
        )

    total_Etudiants = Etudiant.objects.count()

    total_trajets = Trajet.objects.count()

    total_reservations = Reservation.objects.count()

    return render(

        request,

        'acceuil/acceuil.html',

        {
            'trajet': trajet,

            'total_Etudiants': total_Etudiants,

            'total_trajets': total_trajets,

            'total_reservations': total_reservations
        }
    )
def is_authenticated_view(request):

    if request.user.is_authenticated:

        return render(request, 'acceuil/acceuil.html')

    else:

        return redirect('login')

@login_required
def profile_view(request):

    etudiant = Etudiant.objects.get(user=request.user)
    etudiant.total_reservations = etudiant.reservations.count()
    etudiant.total_trajets = etudiant.trajets_crees.count()
    if request.method == 'POST':

        request.user.first_name = request.POST['prenom']

        request.user.last_name = request.POST['nom']

        request.user.email = request.POST['email']

        etudiant.telephone = request.POST['telephone']

        etudiant.filiere = request.POST['filiere']

        if request.FILES.get('photo'):

            etudiant.photo = request.FILES.get('photo')

        request.user.save()

        etudiant.save()

        messages.success(
            request,
            "Profil mis à jour avec succès"
        )

        return redirect('profile')

    return render(
        request,
        'etudiant/profile.html',
        {
            'etudiant': etudiant
        }
    )
@login_required
def MesTrajets_view(request):
    trajets = Etudiant.objects.get(user=request.user).trajets_crees.all()
    return render(request, 'etudiant/MesTrajets.html', {'trajets': trajets})

@login_required
def AjouterTrajet_view(request):
    if request.method == 'POST':
        ville_depart = request.POST['ville_depart']
        ville_arrivee = request.POST['ville_arrivee']
        date = request.POST['date']
        heure_depart = request.POST['heure_depart']
        nb_place = request.POST['nb_place']
        prix = request.POST['prix']
        Trajet.objects.create(
            conducteur_ref=Etudiant.objects.get(user=request.user),
            ville_depart=ville_depart,
            ville_arrivee=ville_arrivee,
            date=date,
            heure_depart=heure_depart,
            nb_place=nb_place,
            prix=prix
        )
        messages.success(request, "Trajet ajouté avec succès")
        return redirect('MesTrajets')  
    
    return render(request, 'etudiant/AjouterTrajet.html')

@login_required
def SupprimerTrajet_view(request, id):

    trajet = Trajet.objects.get(
        id=id,
        conducteur_ref__user=request.user
    )

    trajet.delete()

    messages.success(request, "Trajet supprimé avec succès")
    return redirect('MesTrajets')

@login_required
def ModifierTrajet_view(request, id):
    trajet = Trajet.objects.get(
        id=id,
        conducteur_ref__user=request.user
    )

    if request.method == 'POST':

        trajet.ville_depart = request.POST['ville_depart']
        trajet.ville_arrivee = request.POST['ville_arrivee']
        trajet.date = request.POST['date']
        trajet.heure_depart = request.POST['heure_depart']
        trajet.nb_place = request.POST['nb_place']
        trajet.prix = request.POST['prix']

        trajet.save()
        messages.success(request, "Trajet mis à jour avec succès")
        return redirect('MesTrajets')

    return render(request, 'etudiant/ModifierTrajet.html', {'trajet': trajet})

@login_required
def Trajets_view(request):

    etudiant = Etudiant.objects.get(user=request.user)

    trajets = Trajet.objects.exclude(
        conducteur_ref__user=request.user
    )
    for trajet in trajets:

        trajet.place_disponible = (
            trajet.nb_place - trajet.reservations.count()
        )
        trajet.est_reserver = Reservation.objects.filter(
        etudiant=etudiant,
        trajet=trajet
        ).exists()

        trajet.est_complet = (
            trajet.place_disponible <= 0
        )

    return render(
        request,
        'trajet/trajet.html',
        {
            'trajets': trajets
        }
    )

@login_required
def ReserverTrajet_view(request, id):
    trajet = Trajet.objects.get(id=id)

    etudiant = Etudiant.objects.get(user=request.user)


    if trajet.conducteur_ref == etudiant:
        messages.error(request, "Vous ne pouvez pas réserver votre propre trajet")
        return redirect('trajets')

    if trajet.reservations.count() >= trajet.nb_place:
        messages.error(request, "Ce trajet est complet")
        return redirect('trajets')
    if Reservation.objects.filter(etudiant=etudiant, trajet=trajet).exists():
        messages.error(request, "Vous avez déjà réservé ce trajet")
        return redirect('trajets')
    Reservation.objects.create(
        etudiant=etudiant,
        trajet=trajet
    )

    messages.success(request, "Trajet réservé avec succès")
    return redirect('trajets')

@login_required
def MesReservations_view(request):
    etudiant = Etudiant.objects.get(user=request.user)
    reservations = etudiant.reservations.select_related('trajet').all()
    return render(request, 'reservation/MesReservation.html', {'reservations': reservations})

@login_required
def AnnulerReservation_view(request, id):
    reservation = Reservation.objects.get(id=id, etudiant__user=request.user)
    reservation.delete()
    messages.success(request, "Réservation annulée avec succès")
    return redirect('MesReservations')

@login_required
def DetailReservation_view(request, id):

    reservation = Reservation.objects.get(

        id=id,

        etudiant__user=request.user
    )

    reservation.trajet.place_disponible = (

        reservation.trajet.nb_place -

        reservation.trajet.reservations.count()

    )

    return render(

        request,

        'reservation/detailReservation.html',

        {
            'reservation': reservation
        }
    )
