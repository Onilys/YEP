# Image de base vide 
FROM scratch

# Utilise l'image officielle Python 3.13 comme base pour l'étape de construction
FROM python:3.13 AS builder

# Crée un répertoire "/leFeed" dans l'image pour stocker le projet
RUN mkdir /leFeed

# Définit "/leFeed" comme répertoire de travail
WORKDIR /leFeed

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Met à jour pip vers la dernière version
RUN pip install --upgrade pip

# Copie le fichier "requirements.txt" vers "/leFeed/" dans l'image
COPY /leFeed/requirements.txt /leFeed/

# Met à jour la liste des paquets et installe Git
RUN apt-get update && apt-get install -y git

# Installe les dépendances Python listées dans "requirements.txt" sans utiliser de cache
RUN pip install --no-cache-dir -r requirements.txt

# Crée une nouvelle image finale en repartant de Python 3.13
FROM python:3.13

# Crée un utilisateur non privilégié, recrée le répertoire "/leFeed" et attribue les droits à l'utilisateur
RUN useradd -m -r appuser && \
     mkdir /leFeed && \
     chown -R appuser /leFeed

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 

 # Copie les dépendances Python installées dans l'étape "builder" vers l'image finale
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/

# Copie les binaires depuis l'étape "builder" vers l'image finale
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Définit "/leFeed" comme répertoire de travail pour les commandes suivantes
WORKDIR /leFeed

# Copie tous les fichiers du projet local vers "/leFeed/" dans l'image, en attribuant la propriété à "appuser"
COPY --chown=appuser:appuser . .

# Définit "appuser" comme utilisateur par défaut pour les commandes suivantes
USER appuser

# Indique que le conteneur écoutera sur le port 9111 
EXPOSE 9111

# Définit "/leFeed" comme répertoire de travail
WORKDIR /leFeed
#CMD ["ls"]
#l#ancement du serveur de développement Django sur le port 9111
#CMD ["python","manage.py","runserver","0.0.0.0:9111"]
CMD ["gunicorn","leFeed.wsgi","--bind","0.0.0.0:9111","--workers","3"]
