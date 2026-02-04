from rest_framework import serializers
from news.models import Info

class InfoDetailSerializer(serializers.ModelSerializer):

    #Sérialiseur détaillé pour le modèle Info.
    #Utilisé pour les opérations nécessitant tous les champs (création, mise à jour, affichage détaillé).
    
    class Meta:
        model = Info  # Modèle Django associé
        fields = ['titre', 'lien', 'commentaire', 'visible']  # Champs à inclure dans la sérialisation
