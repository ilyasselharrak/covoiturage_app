from django.contrib import admin
from .models import Etudiant
from .models import Trajet
from .models import Reservation

# Register your models here.
admin.site.register(Etudiant)
admin.site.register(Trajet)
admin.site.register(Reservation)
