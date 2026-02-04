from django.db import models
from django.utils import timezone

class Info(models.Model):
    titre = models.CharField(max_length=200) #titre de l'info
    lien = models.URLField()#lien obligatoire vers l'info
    commentaire = models.CharField(null=True, blank=True, max_length=1000) 
    #commentaire non obligatoire
    visible = models.BooleanField(default=False) # visibilité de l'info
    created_at = models.DateTimeField(default=timezone.now)  
    # Utilise timezone.now pour mettre le created_at au moment de creation

    def __str__(self):
        return self.titre  # Added string representation method

