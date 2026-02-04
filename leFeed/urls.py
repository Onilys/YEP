from django.contrib import admin
from django.urls import path
from news.views import leFeed, ajout, modifier_info, supprimer_info, custom_404

# Gestionnaire d'erreur 404 personnalisé
handler404 = custom_404

urlpatterns = [
    # Interface d'administration
    path('admin/', admin.site.urls, name='admin'),
    # Page d'accueil - affichage des infos visibles les plus recente
    path('', leFeed, name='leFeed'),
    # CRUD des infos
    path('ajout/', ajout, name='ajout'),  # Création
    path('modifier/<int:info_id>/', modifier_info, name='modifier_info'),  # Modification
    path('supprimer/<int:info_id>/', supprimer_info, name='supprimer_info'),  # Suppression
]
