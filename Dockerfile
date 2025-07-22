FROM python:3.13.5

# Définit le dossier de travail dans le container
WORKDIR /PRIVATE_BOT_DISCORD_F1F

# Copie le fichier requirements.txt dans le container
COPY requirements.txt .

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le contenu du projet (y compris le dossier app) dans le container
COPY . .

# Commande pour lancer le bot
CMD ["python", "app/app.py"]
