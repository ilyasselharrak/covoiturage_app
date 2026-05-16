"""
URL configuration for projet_python project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from covoiturage import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('MesTrajets/', views.MesTrajets_view, name='MesTrajets'),
    path('AjouterTrajet/', views.AjouterTrajet_view, name='AjouterTrajet'),
    path('SupprimerTrajet/<int:id>/', views.SupprimerTrajet_view, name='SupprimerTrajet'),
    path('ModifierTrajet/<int:id>/', views.ModifierTrajet_view, name='ModifierTrajet'),
    path('trajets/', views.Trajets_view, name='trajets'),
    path('trajets/ReserverTrajet/<int:id>/', views.ReserverTrajet_view, name='ReserverTrajet'),
    path('MesReservations/', views.MesReservations_view, name='MesReservations'),
    path('AnnulerReservation/<int:id>/', views.AnnulerReservation_view, name='AnnulerReservation'),
    path('DetailReservation/<int:id>/', views.DetailReservation_view, name='DetailReservation'),
    path('DetailTrajet/<int:id>/', views.DetailTrajet_view, name='DetailTrajet'),
    path('Apropos/', views.Apropos_view, name='Apropos'),
    path('rechercheTrajets/', views.rechercheTrajets_view, name='rechercheTrajets')
]

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
