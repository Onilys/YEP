from django import forms
#form universel pour l'ajout et la modification des données
class Formulaire(forms.Form):
    titre = forms.CharField()
    lien = forms.URLField()
    commentaire = forms.CharField(required=False)
    visible = forms.BooleanField()





