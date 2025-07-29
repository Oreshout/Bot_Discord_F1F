import os 
import json
import discord
from datetime import datetime

from config import SALAIRE_JOURNALIER

file_path = 'data/eco/central_account.json'

def salaire(interaction: discord.Interaction):
    
    # Chargement ou création du fichier
    if not os.path.exists(file_path):
        central_account = {}
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            central_account = json.load(f)
    
    user_id = str(interaction.user.id)
    username = interaction.user.name
    today = datetime.now().date()

    # Si l'utilisateur est nouveau, on initialise son compte
    if user_id not in central_account:
        central_account[user_id] = {
            "Pseudo": username,
            "Solde": SALAIRE_JOURNALIER,
            "last_claim": str(today)
        }
        message = f"💸 Premier salaire reçu ! Tu as obtenu {SALAIRE_JOURNALIER} 💰."
    else:
        # Récupération de la dernière date de versement
        last_claim_str = central_account[user_id].get("last_claim", "2000-01-01")
        last_claim = datetime.strptime(last_claim_str, "%Y-%m-%d").date()

        if last_claim < today:
            # L'utilisateur peut réclamer son salaire
            central_account[user_id]["Solde"] += SALAIRE_JOURNALIER
            central_account[user_id]["last_claim"] = str(today)
            message = f"💰 Salaire journalier reçu ! +{SALAIRE_JOURNALIER} 💸"
        else:
            # Il a déjà réclamé aujourd'hui
            message = "⏳ Tu as déjà reçu ton salaire aujourd’hui. Reviens demain !"

    # Sauvegarde
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(central_account, f, indent=4, ensure_ascii=False)

    return message    


async def voir_solde(interaction: discord.Interaction):
    user_id = str(interaction.user.id)

    if not os.path.exists(file_path):
        message = "Désolé, mais tu n'as rien sur ton compte. Fais la commande `/salaire` pour obtenir ton premier salaire."
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            soldes = json.load(f)

        user_data = soldes.get(user_id)
        if user_data is None:
            message = "Désolé, mais tu n'as rien sur ton compte. Fais la commande `/salaire` pour obtenir ton premier salaire."
        else:
            solde = user_data.get("Solde", 0)
            message = f"💰 Ton solde actuel est de **{solde}** coins."
            
    await interaction.followup.send(message, ephemeral=True)