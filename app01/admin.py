from django.contrib import admin
from .models import pub0, contact01 , Message # Importez votre modèle

# Enregistrement simple
admin.site.register(pub0)

admin.site.register(contact01)

admin.site.register(Message)