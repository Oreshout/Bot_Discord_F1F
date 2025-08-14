import os
import json
from datetime import datetime, timedelta, timezone
import discord
from discord import app_commands
import config as param

DATA_FILE = 'data/work/data_work.json'
DATA_FILE_COMPTE_COURANT = "data/eco/central_account.json"
DATA_FILE_COMPTE_PROTEGE = "data/eco/protect_account.json"


def charger_donnees():
    # S'assurer que le dossier existe
    dossier = os.path.dirname(DATA_FILE)
    if dossier and not os.path.exists(dossier):
        os.makedirs(dossier)

    # Si fichier absent, on le crée avec la structure initiale
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"offres": {}, "engagements": {}}, f, indent=4)

    # Chargement des données
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def sauvegarder_donnees(donnees):
    # S'assurer que le dossier existe avant d'écrire
    dossier = os.path.dirname(DATA_FILE)
    if dossier and not os.path.exists(dossier):
        os.makedirs(dossier)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=4)


def generer_date_expiration():
    return (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()


def offre_expiree(date_expiration):
    return datetime.now(timezone.utc) > datetime.fromisoformat(date_expiration)


def utilisateur_est_engage(user_id: int, donnees: dict) -> bool:
    """Vérifie si un utilisateur est déjà lié à une offre en cours."""
    return str(user_id) in donnees["engagements"]


def ajouter_offre(offre_id: str, type_offre: str, createur_name: str,createur_id: int, salaire: int, description: str, donnees: dict):
    """Ajoute une nouvelle offre dans la base JSON."""
    donnees["offres"][offre_id] = {
        "type": type_offre,  # "emploi" ou "service"
        "createur": createur_name,
        "createur_id": createur_id,
        "salaire": salaire,
        "description": description,
        "date_creation": datetime.now(timezone.utc).isoformat(),
        "expiration": generer_date_expiration(),
        "candidats": [],
        "candidats_id": [],
        "selectionne": None,
        "valide_createur": False,
        "valide_postulant": False,
        "etat": "en_cours"
    }
    donnees["engagements"][str(createur_id)] = {
        "createur_name": createur_name,
        "offre_id": offre_id,
        "role": "createur"
    }
    sauvegarder_donnees(donnees)


def supprimer_offres_expirees(donnees: dict):
    """Supprime les offres dépassées (30 jours) et libère les engagements."""
    a_supprimer = []
    for offre_id, offre in donnees["offres"].items():
        if offre_expiree(offre["expiration"]):
            a_supprimer.append(offre_id)

    for offre_id in a_supprimer:
        createur_id = str(donnees["offres"][offre_id]["createur"])
        selectionne_id = donnees["offres"][offre_id]["selectionne"]

        # Suppression des engagements du créateur
        if createur_id in donnees["engagements"]:
            del donnees["engagements"][createur_id]

        # Suppression de l'engagement du postulant sélectionné
        if selectionne_id and str(selectionne_id) in donnees["engagements"]:
            del donnees["engagements"][str(selectionne_id)]

        del donnees["offres"][offre_id]

    if a_supprimer:
        sauvegarder_donnees(donnees)
        
def get_solde_total(user_id: str) -> int:
    if not os.path.exists(DATA_FILE_COMPTE_COURANT):
        with open(DATA_FILE_COMPTE_COURANT, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)
    if not os.path.exists(DATA_FILE_COMPTE_PROTEGE):
        with open(DATA_FILE_COMPTE_PROTEGE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)

    with open(DATA_FILE_COMPTE_COURANT, "r", encoding="utf-8") as f:
        compte_courant = json.load(f)
    with open(DATA_FILE_COMPTE_PROTEGE, "r", encoding="utf-8") as f:
        compte_protege = json.load(f)

    solde_courant = compte_courant.get(user_id, {}).get("Solde", 0)
    solde_protege = compte_protege.get(user_id, {}).get("Solde", 0)

    return solde_courant + solde_protege

def effectuer_paiement(createur_id, postulant_id, montant):
    # Charger les deux fichiers
    comptes_courants = charger_donnees(DATA_FILE_COMPTE_COURANT)
    comptes_proteges = charger_donnees(DATA_FILE_COMPTE_PROTEGE)

    createur_id = str(createur_id)
    postulant_id = str(postulant_id)

    # Vérifier si le créateur a un compte protégé
    if createur_id not in comptes_proteges:
        raise ValueError("❌ Le créateur n'a pas de compte protégé.")

    # Vérifier solde suffisant
    if comptes_proteges[createur_id]["Solde"] < montant:
        raise ValueError("❌ Solde insuffisant sur le compte protégé du créateur.")

    # Retirer du compte protégé du créateur
    comptes_proteges[createur_id]["Solde"] -= montant

    # Ajouter au compte courant du postulant
    if postulant_id not in comptes_courants:
        # Si le compte n'existe pas, on le crée
        comptes_courants[postulant_id] = {
            "Pseudo": f"user_{postulant_id}",
            "Solde": 0,
            "last_claim": None
        }
    comptes_courants[postulant_id]["Solde"] += montant

    # Sauvegarder les fichiers
    sauvegarder_donnees(DATA_FILE_COMPTE_COURANT, comptes_courants)
    sauvegarder_donnees(DATA_FILE_COMPTE_PROTEGE, comptes_proteges)

    return True


# ----- Vue pour le bouton -----


class BoutonPostuler(discord.ui.View):
    def __init__(self, offre_id: str):
        super().__init__(timeout=None)
        self.offre_id = offre_id

    @discord.ui.button(label="Postuler", style=discord.ButtonStyle.green)
    async def postuler(self, interaction: discord.Interaction, button: discord.ui.Button):
        donnees = charger_donnees()
        offre = donnees["offres"].get(self.offre_id)

        if not offre:
            return await interaction.response.send_message("❌ Cette offre n'existe plus.", ephemeral=True)

        # Sécurité : pas de postule sur sa propre offre
        if offre["createur_id"] == interaction.user.id:
            return await interaction.response.send_message("❌ Vous ne pouvez pas postuler à votre propre offre.", ephemeral=True)

        # Sécurité : utilisateur libre
        if utilisateur_est_engage(interaction.user.id, donnees):
            return await interaction.response.send_message("❌ Vous êtes déjà engagé dans une autre offre.", ephemeral=True)

        # Ajouter le candidat
        offre["candidats"].append(interaction.user.name)
        offre["candidats_id"].append(interaction.user.id)
        sauvegarder_donnees(donnees)

        # MP au créateur
        createur = interaction.client.get_user(offre["createur_id"])
        if createur:
            await createur.send(f"📩 {interaction.user.name} est intéressé par ton offre d'emploi **{offre['description'][:30]}...**")

        await interaction.response.send_message("✅ Votre candidature a été envoyée au créateur de l’offre.", ephemeral=True)

# ----- Création de l'embed -----


def creer_embed_offre(user: discord.User, salaire: int, description: str):
    embed = discord.Embed(
        title=f"Recrutement de {user.name}",
        description=description,
        color=param.EMBED_COLOR_GREEN
    )
    embed.add_field(name="💰 Salaire", value=f"{salaire} 💵")
    embed.add_field(name="📅 Date", value=datetime.now(
        timezone.utc).strftime("%d/%m/%Y"))
    embed.add_field(name="⏳ Expire le", value=(datetime.now(
        timezone.utc) + timedelta(days=30)).strftime("%d/%m/%Y"))
    embed.set_footer(text="Appuyez sur le bouton ci-dessous pour postuler")
    return embed

async def work(interaction: discord.Interaction, salaire: int):
    donnees = charger_donnees()

    # Vérifier si l'utilisateur est libre
    if utilisateur_est_engage(interaction.user.id, donnees):
        return await interaction.response.send_message("❌ Vous avez déjà une offre active ou un engagement en cours.", ephemeral=True)

    # Vérifier argent sur le compte (compte courant + compte protégé)
    argent_total = get_solde_total(str(interaction.user.id))
    if argent_total < salaire:
        return await interaction.response.send_message("❌ Vous n'avez pas assez d'argent pour créer cette offre.", ephemeral=True)

    await interaction.response.send_message("📩 Je vous ai envoyé un MP pour la description de l'offre.", ephemeral=True)

    # Demander la description en MP
    try:
        await interaction.user.send("✏️ Veuillez entrer la description de votre offre d'emploi (vous avez 2 minutes) :")

        def check(m):
            return m.author == interaction.user and isinstance(m.channel, discord.DMChannel)

        msg = await param.bot.wait_for("message", check=check, timeout=120)
        description = msg.content.strip()
        if not description:
            return await interaction.user.send("❌ La description ne peut pas être vide. Recommencez la commande.")

    except TimeoutError:
        return await interaction.user.send("⏰ Temps écoulé. Recommencez la commande.")

    # Poster dans le forum
    forum_channel = interaction.guild.get_channel(1404481278778277909)  # ID du forum à mettre
    thread = await forum_channel.create_thread(
    name=f"Recrutement de {interaction.user.name}",
    content="Bienvenue dans ce thread de recrutement !"
    )
# thread = ThreadWithMessage ici
    real_thread = thread.thread  # On récupère l'objet Thread réel

    embed = creer_embed_offre(interaction.user, salaire, description)
    await real_thread.send(embed=embed, view=BoutonPostuler(str(real_thread.id)))

    # Sauvegarder l'offre
    ajouter_offre(str(real_thread.id), "emploi", interaction.user.name, interaction.user.id, salaire, description, donnees)

    await interaction.user.send("✅ Votre offre a été publiée avec succès.")
    
async def validation_work(interaction: discord.Interaction):
    donnees = charger_donnees()
    user_id = interaction.user.id

    # 1. Vérifier si l'utilisateur a un engagement
    if str(user_id) not in donnees["engagements"]:
        return await interaction.response.send_message(
            "❌ Vous n'avez pas de mission en cours.",
            ephemeral=True
        )

    # 2. Récupérer l'offre liée
    engagement = donnees["engagements"][str(user_id)]
    offre_id = engagement["offre_id"]
    offre = donnees["offres"][offre_id]

    if offre["etat"] != "en_cours":
        return await interaction.response.send_message(
            "❌ Cette mission n'est plus active.",
            ephemeral=True
        )

    # 3. Valider selon le rôle
    if engagement["role"] == "createur":
        offre["valide_createur"] = True
    elif engagement["role"] == "postulant":
        offre["valide_postulant"] = True
    else:
        return await interaction.response.send_message(
            "❌ Vous n'êtes pas impliqué dans cette mission.",
            ephemeral=True
        )

    sauvegarder_donnees(donnees)

    # 4. Vérifier si les deux ont validé
    if offre["valide_createur"] and offre["valide_postulant"]:
        # Paiement
        effectuer_paiement(offre["createur_id"], offre["selectionne_id"], offre["salaire"])

        # Suppression des engagements
        del donnees["engagements"][str(offre["createur_id"])]
        del donnees["engagements"][str(offre["selectionne_id"])]

        # Suppression de l'offre
        del donnees["offres"][offre_id]

        sauvegarder_donnees(donnees)
        return await interaction.response.send_message(
            "✅ Les deux parties ont validé. Paiement effectué et mission supprimée."
        )

    # 5. Si un seul a validé → indiquer qui manque
    parties_restantes = []
    if not offre["valide_createur"]:
        parties_restantes.append(offre["createur"])
    if not offre["valide_postulant"]:
        # On cherche le nom du sélectionné
        idx = offre["candidats_id"].index(offre["selectionne_id"])
        parties_restantes.append(offre["candidats"][idx])

    return await interaction.response.send_message(
        f"✅ Votre validation a été enregistrée. En attente de : {', '.join(parties_restantes)}"
    )
    
async def candidats_autocomplete(interaction: discord.Interaction, current: str):
    # Charger le JSON
    with open("data.json", "r") as f:
        data = json.load(f)

    # Trouver l'offre en cours créée par l'utilisateur
    offre = next(
        (o for o in data["offres"].values()
         if o["createur_id"] == interaction.user.id and o["etat"] == "en_cours"),
        None
    )

    if not offre:
        return []

    # Liste des IDs des candidats
    candidats_ids = offre.get("candidats_id", [])

    # Filtrer les membres selon le texte tapé
    options = []
    for member_id in candidats_ids:
        member = interaction.guild.get_member(member_id)
        if member and current.lower() in member.name.lower():
            options.append(app_commands.Choice(name=member.name, value=str(member.id)))

    return options[:25]  # max 25 résultats


async def contrat(interaction: discord.Interaction, candidat: discord.Member):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    # Trouver l'offre unique en cours
    offre_id, offre = next(
        ((oid, o) for oid, o in data["offres"].items()
         if o["createur_id"] == interaction.user.id and o["etat"] == "en_cours"),
        (None, None)
    )

    if not offre:
        await interaction.response.send_message(
            "Aucune offre en cours trouvée pour vous.", ephemeral=True
        )
        return

    # Vérifier que le candidat a postulé
    if candidat.id not in offre["candidats_id"]:
        await interaction.response.send_message(
            "Ce candidat n'a pas postulé à cette offre.", ephemeral=True
        )
        return

    # Bloquer les candidatures et enregistrer le candidat
    offre["etat"] = "ferme"
    offre["selectionne"] = candidat.id

    # Ajouter l'engagement
    data["engagements"][str(candidat.id)] = {
        "createur_name": interaction.user.name,
        "offre_id": offre_id,
        "role": "postulant"
    }

    # Sauvegarder
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    # Boutons d'acceptation ou refus
    class ContratView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

    @discord.ui.button(label="J'accepte", style=discord.ButtonStyle.green)
    async def accepter(self, interaction_btn, _):
        if interaction_btn.user.id != candidat.id:
            await interaction_btn.response.send_message("Ce n'est pas pour toi.", ephemeral=True)
            return

        offre["etat"] = "valide"
        offre["valide_postulant"] = True
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

        await interaction_btn.response.send_message("Contrat accepté ! 🎉", ephemeral=True)

        # 🔔 Prévenir le créateur de l'annonce
        createur = interaction_btn.client.get_user(offre["createur_id"])
        if createur:
            try:
                await createur.send(
                    f"✅ Le candidat **{candidat.name}** a accepté le contrat pour votre offre : **{offre['type']}**."
                )
            except discord.Forbidden:
                # Si le créateur a bloqué les MP
                await interaction_btn.followup.send(
                    f"Impossible d’envoyer un message au créateur {createur.mention}.",
                    ephemeral=True
                )

        self.stop()


    @discord.ui.button(label="Je refuse", style=discord.ButtonStyle.red)
    async def refuser(self, interaction_btn, _):
        if interaction_btn.user.id != candidat.id:
            await interaction_btn.response.send_message("Ce n'est pas pour toi.", ephemeral=True)
            return

        offre["etat"] = "refuse"
        offre["selectionne"] = None
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

        await interaction_btn.response.send_message("Contrat refusé. ❌", ephemeral=True)

        # 🔔 Prévenir le créateur de l'annonce
        createur = interaction_btn.client.get_user(offre["createur_id"])
        if createur:
            try:
                await createur.send(
                    f"❌ Le candidat **{candidat.name}** a refusé le contrat pour votre offre : **{offre['type']}**."
                )
            except discord.Forbidden:
                await interaction_btn.followup.send(
                    f"Impossible d’envoyer un message au créateur {createur.mention}.",
                    ephemeral=True
                )

        self.stop()
        # Envoi du MP au candidat
        await candidat.send(
            f"Vous avez été sélectionné pour l'offre : {offre['type']} (créée par {offre['createur']})\n"
            "Acceptez-vous le contrat ?",
            view=ContratView()
        )

        await interaction.response.send_message(
            f"Le candidat {candidat.mention} a été sélectionné et a reçu le MP.",
            ephemeral=True
        )
    
async def supprimer_offre(interaction: discord.Interaction):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    # Trouver l'offre en cours de l'utilisateur
    offre_id, offre = next(
        ((oid, o) for oid, o in data["offres"].items()
         if o["createur_id"] == interaction.user.id and o["etat"] == "en_cours"),
        (None, None)
    )

    if not offre:
        await interaction.response.send_message(
            "Vous n'avez aucune offre en cours à supprimer.", ephemeral=True
        )
        return

    # 1️⃣ Supprimer l'offre dans `offres`
    del data["offres"][offre_id]

    # 2️⃣ Supprimer l'engagement du créateur lié à cette offre
    engagements_a_supprimer = [
        uid for uid, e in data["engagements"].items()
        if e["offre_id"] == offre_id
    ]
    for uid in engagements_a_supprimer:
        del data["engagements"][uid]

    # Sauvegarder le JSON
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    await interaction.response.send_message(
        f"L'offre **{offre_id}** a été supprimée avec succès ✅",
        ephemeral=True
    )