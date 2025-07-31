import os 
import json
import discord
from datetime import datetime

from config import SALAIRE_JOURNALIER

file_path = 'data/eco/central_account.json'
file_path_protect = 'data/eco/protect_account.json'

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
    
async def virement(interaction: discord.Interaction, somme_a_retirer: int, cible: discord.Member):
    user_id = str(interaction.user.id)
    cible_id = str(cible.id)

    if not os.path.exists(file_path):
        await interaction.followup.send("❌ Tu n'as pas encore de compte. Fais `/salaire` pour commencer.", ephemeral=True)
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        soldes = json.load(f)

    if user_id not in soldes:
        await interaction.followup.send("❌ Ton compte n'existe pas.", ephemeral=True)
        return

    if cible_id not in soldes:
        await interaction.followup.send("❌ Le compte du destinataire n'existe pas.", ephemeral=True)
        return

    if soldes[user_id]["Solde"] < somme_a_retirer:
        await interaction.followup.send("❌ Tu n'as pas assez d'argent.", ephemeral=True)
        return

    # Effectuer le virement
    soldes[user_id]["Solde"] -= somme_a_retirer
    soldes[cible_id]["Solde"] += somme_a_retirer

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(soldes, f, indent=4, ensure_ascii=False)

    await interaction.followup.send(f"✅ Tu as envoyé **{somme_a_retirer}€** à **{cible.display_name}**.", ephemeral=True)
    # Supposons que cible_id est un int (id du membre cible)
    cible = await interaction.client.fetch_user(cible_id)

    try:
        await cible.send(f"{interaction.user.mention} t'a viré **{somme_a_retirer}€** 💸")
    except discord.Forbidden:
        # Si la personne a ses MP fermés
        await interaction.followup.send(
            f"⚠️ Impossible d'envoyer un message privé à {cible.mention}.",
            ephemeral=True
        )


async def retrait(interaction: discord.Interaction, somme_a_retirer: int, cible: discord.Member):
    user_id = str(interaction.user.id)
    cible_id = str(cible.id)

    if not os.path.exists(file_path):
        await interaction.followup.send("❌ Tu n'as pas encore de compte. Fais `/salaire` pour commencer.", ephemeral=True)
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        soldes = json.load(f)

    if user_id not in soldes:
        await interaction.followup.send("❌ Ton compte n'existe pas.", ephemeral=True)
        return

    if cible_id not in soldes:
        await interaction.followup.send("❌ Le compte du destinataire n'existe pas.", ephemeral=True)
        return

    if soldes[cible_id]["Solde"] < somme_a_retirer:
        await interaction.followup.send("❌ Il n'a pas assez d'argent", ephemeral=True)
        return

    # Effectuer le virement
    soldes[user_id]["Solde"] += somme_a_retirer
    soldes[cible_id]["Solde"] -= somme_a_retirer

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(soldes, f, indent=4, ensure_ascii=False)

    await interaction.followup.send(f"✅ Tu as retiré **{somme_a_retirer}€** à **{cible.display_name}**.", ephemeral=True)
    # Supposons que cible_id est un int (id du membre cible)
    cible = await interaction.client.fetch_user(cible_id)

    try:
        await cible.send(f"{interaction.user.mention} t'a retiré **{somme_a_retirer}€** 💸")
    except discord.Forbidden:
        # Si la personne a ses MP fermés
        await interaction.followup.send(
            f"⚠️ Impossible d'envoyer un message privé à {cible.mention}.",
            ephemeral=True
        )

async def top(interaction: discord.Interaction):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            comptes = json.load(f)
    except FileNotFoundError:
        await interaction.followup.send("❌ Aucun compte trouvé.", ephemeral=True)
        return

    # Tri des comptes par solde décroissant
    comptes_tries = sorted(comptes.items(), key=lambda x: x[1].get("Solde", 0), reverse=True)
    top_comptes = comptes_tries[:10]

    # Construction du message
    description = ""
    for i, (user_id, data) in enumerate(top_comptes, start=1):
        pseudo = data.get("Pseudo", f"Utilisateur inconnu ({user_id})")
        solde = data.get("Solde", 0)
        description += f"**{i}.** `{pseudo}` — **{solde}€**\n"

    embed = discord.Embed(
        title="💰 Top 10 des plus riches",
        description=description or "Aucun compte à afficher.",
        color=discord.Color.green()
    )

    await interaction.followup.send(embed=embed)    
    
async def virement_compte_courant_to_protect(interaction: discord.Interaction, somme_a_verser: int):
    user_id = str(interaction.user.id)
    user_pseudo = str(interaction.user)

    # Vérification du montant
    if somme_a_verser <= 0:
        await interaction.followup.send("❌ Le montant doit être supérieur à 0.", ephemeral=True)
        return

    # Chargement du fichier du compte courant
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        await interaction.followup.send("❌ Ton compte courant n'existe pas. Fais `/salaire` pour commencer.", ephemeral=True)
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        soldes = json.load(f)

    # Chargement ou création du fichier du compte protégé
    if not os.path.exists(file_path_protect) or os.path.getsize(file_path_protect) == 0:
        soldes_protect = {}
    else:
        with open(file_path_protect, 'r', encoding='utf-8') as f:
            soldes_protect = json.load(f)

    # Vérification ou création du compte protégé pour l'utilisateur
    if user_id not in soldes_protect:
        soldes_protect[user_id] = {
            "Pseudo": user_pseudo,
            "Solde": 0,
            "last_claim": datetime.today().strftime('%Y-%m-%d')
        }

    # Vérification de l'existence du compte courant
    if user_id not in soldes:
        await interaction.followup.send("❌ Ton compte courant n'existe pas.", ephemeral=True)
        return

    # Vérification du solde disponible
    solde_disponible = soldes[user_id].get("Solde", 0)
    if solde_disponible < somme_a_verser:
        await interaction.followup.send("❌ Tu n'as pas assez d'argent sur ton compte courant.", ephemeral=True)
        return

    # Transfert
    soldes[user_id]["Solde"] -= somme_a_verser
    soldes_protect[user_id]["Solde"] += somme_a_verser

    # Sauvegarde
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(soldes, f, indent=4, ensure_ascii=False)
    with open(file_path_protect, 'w', encoding='utf-8') as f:
        json.dump(soldes_protect, f, indent=4, ensure_ascii=False)

    # Message de confirmation
    await interaction.followup.send(
        f"✅ Tu as transféré **{somme_a_verser}€** sur ton compte protégé.", ephemeral=False
    )
    
    
async def voir_solde_proteger(interaction: discord.Interaction):
    user_id = str(interaction.user.id)

    if not os.path.exists(file_path_protect):
        message = "Désolé, mais tu n'as rien sur ton compte protégé. Fais la commande `/deposit` pour verser de l'argent dessus."
    else:
        with open(file_path_protect, 'r', encoding='utf-8') as f:
            soldes = json.load(f)

        user_data = soldes.get(user_id)
        if user_data is None:
            message = "Désolé, mais tu n'as rien sur ton compte protégé. Fais la commande `/deposit` pour verser de l'argent dessus."
        else:
            solde = user_data.get("Solde", 0)
            message = f"💰 Ton solde protégé est de **{solde}** coins."
            
    await interaction.followup.send(message, ephemeral=True)

async def virement_compte_protege_to_courant(interaction: discord.Interaction, somme_a_verser: int):
    user_id = str(interaction.user.id)
    user_pseudo = str(interaction.user)

    # Vérification du montant
    if somme_a_verser <= 0:
        await interaction.followup.send("❌ Le montant doit être supérieur à 0.", ephemeral=True)
        return

    # Chargement du fichier du compte courant
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        await interaction.followup.send("❌ Ton compte courant n'existe pas. Fais `/salaire` pour commencer.", ephemeral=True)
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        soldes = json.load(f)

    # Chargement ou création du fichier du compte protégé
    if not os.path.exists(file_path_protect) or os.path.getsize(file_path_protect) == 0:
        soldes_protect = {}
    else:
        with open(file_path_protect, 'r', encoding='utf-8') as f:
            soldes_protect = json.load(f)

    # Vérification ou création du compte protégé pour l'utilisateur
    if user_id not in soldes_protect:
        soldes_protect[user_id] = {
            "Pseudo": user_pseudo,
            "Solde": 0,
            "last_claim": datetime.today().strftime('%Y-%m-%d')
        }

    # Vérification de l'existence du compte courant
    if user_id not in soldes_protect:
        await interaction.followup.send("❌ Ton compte courant n'existe pas.", ephemeral=True)
        return

    # Vérification du solde disponible
    solde_disponible = soldes_protect[user_id].get("Solde", 0)
    if solde_disponible < somme_a_verser:
        await interaction.followup.send("❌ Tu n'as pas assez d'argent sur ton compte courant.", ephemeral=True)
        return

    # Transfert
    soldes[user_id]["Solde"] += somme_a_verser
    soldes_protect[user_id]["Solde"] -= somme_a_verser

    # Sauvegarde
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(soldes, f, indent=4, ensure_ascii=False)
    with open(file_path_protect, 'w', encoding='utf-8') as f:
        json.dump(soldes_protect, f, indent=4, ensure_ascii=False)

    # Message de confirmation
    await interaction.followup.send(
        f"✅ Tu as transféré **{somme_a_verser}€** sur ton compte courant.", ephemeral=False
    )
