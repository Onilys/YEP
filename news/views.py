from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from news.models import Info
import requests
from bs4 import BeautifulSoup
from news.form import Formulaire

def custom_404(request, exception):
    #Gestionnaire personnalisé pour les erreurs 404.
    return render(request, 'news/404.html', status=404)

# Associe le gestionnaire 404 personnalisé à Django
handler404 = custom_404

def leFeed(request):
    # Récupère les 5 dernières infos visibles
    infos = Info.objects.filter(visible=True).order_by('-created_at')[:5]

    # Pour chaque info, tente de récupérer une image de prévisualisation si un lien est présent
    for info in infos:
        if info.lien:
            info.meta_image = get_meta_image(info.lien)

    return render(request, 'news/leFeed.html', {
        'infos': infos,
        'user': request.user  # Passe l'utilisateur courant au template pour gérer l'affichage conditionnel
    })

def get_meta_image(url):
    #Récupère l'URL de l'image de prévisualisation d'une page web.
    try:
        # Effectue une requête HTTP avec un timeout pour éviter les blocages
        response = requests.get(url, timeout=5)
        # Parse le HTML de la page
        soup = BeautifulSoup(response.text, 'html.parser')
        # Recherche la balise meta pour l'image
        meta_tag = soup.find('meta', property='og:image')
        if meta_tag:
            return meta_tag.get('content', '')
    except Exception as e:
        # Log l'erreur mais ne la propage pas pour ne pas interrompre l'affichage
        print(f"Erreur lors de la récupération de l'image pour {url}: {e}")
    return None

@user_passes_test(lambda u: u.is_superuser)
def ajout(request):
    #Vue pour ajouter une nouvelle info
    if request.method == 'POST':
        form = Formulaire(request.POST)
        if form.is_valid():
            # Récupère les données validées du formulaire
            titre = form.cleaned_data['titre']
            lien = form.cleaned_data['lien']
            commentaire = form.cleaned_data['commentaire']
            visible = form.cleaned_data['visible']

            # Crée et sauvegarde la nouvelle info
            info = Info(titre=titre, lien=lien, commentaire=commentaire, visible=visible)
            info.save()

            return redirect(leFeed)  # Redirige vers la page principale après ajout
    else:
        form = Formulaire()  # Crée un formulaire vide pour un GET

    return render(request, 'news/formulaire.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def modifier_info(request, info_id):    
    info = get_object_or_404(Info, id=info_id)  # 404 si l'info n'existe pas

    if request.method == 'POST':
        form = Formulaire(request.POST)
        if form.is_valid():
            # Met à jour chaque champ de l'info avec les données du formulaire
            info.titre = form.cleaned_data['titre']
            info.lien = form.cleaned_data['lien']
            info.commentaire = form.cleaned_data['commentaire']
            info.visible = form.cleaned_data['visible']
            info.save()
            return redirect(leFeed)  # Redirige vers la page principale après modification
    else:
        # Préremplit le formulaire avec les données existantes
        form = Formulaire(initial={
            'titre': info.titre,
            'lien': info.lien,
            'commentaire': info.commentaire,
            'visible': info.visible,
        })

    # Passe l'ID de l'info au template pour gérer le cas de la modification
    return render(request, 'news/formulaire.html', {'form': form, 'info_id': info_id})

@user_passes_test(lambda u: u.is_superuser)
def supprimer_info(request, info_id):

    info = get_object_or_404(Info, id=info_id)  # 404 si l'info n'existe pas
    info.delete()  # Supprime l'info de la base de données
    return redirect(leFeed)  # Redirige vers la page principale après suppression