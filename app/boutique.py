import discord
import os
import json
import asyncio
from config import logger, EMBED_BOUTIQUE_OFFICEL, EMBED_COLOR_RED, EMBED_THUMBNAIL, EMBED_FOOTER_TEXT, JOUR

DATA_FILE = 'data/eco/central_account.json'

# --------- Gestion des données ---------
def charger_donnees():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def sauvegarder_donnees(donnees):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=4)

def ajouter_argent(user_id: int, montant: int):
    donnees = charger_donnees()
    user_id = str(user_id)

    if user_id not in donnees:
        donnees[user_id] = {
            "Pseudo": "Inconnu",
            "Solde": 0,
            "last_claim": ""
        }

    donnees[user_id]["Solde"] += montant
    sauvegarder_donnees(donnees)
    
def retirer_argent(user_id: int, montant: int) -> bool:
    donnees = charger_donnees()
    user_id = str(user_id)

    if user_id not in donnees:
        donnees[user_id] = {
            "Pseudo": "Inconnu",
            "Solde": 0,
            "last_claim": ""
        }

    solde_actuel = donnees[user_id]["Solde"]
    if solde_actuel < montant:
        return True  # Pas assez d'argent
    else:
        donnees[user_id]["Solde"] -= montant
        donnees["F1FACCOUNT"]["Solde"] += montant
        sauvegarder_donnees(donnees)
        return False
    
async def ajouter_role(member: discord.Member, role_id: int):
    role = member.guild.get_role(role_id)
    if role is None:
        logger.warning(f"❌ Rôle introuvable : {role_id}")
        return
    try:
        await member.add_roles(role)
        logger.info(f"✅ Rôle '{role.name}' ajouté à {member.display_name}")
    except discord.Forbidden:
        logger.warning("❌ Le bot n'a pas la permission d'ajouter ce rôle.")
    except discord.HTTPException as e:
        logger.error(f"❌ Une erreur est survenue : {e}")
        
async def ajouter_role_temporaire(membre: discord.Member, role_id: int, duree_sec: int):
    role = membre.guild.get_role(role_id)
    if not role:
        return

    await membre.add_roles(role, reason="Rôle temporaire ajouté via la boutique")
    logger.info(f"Rôle {role.name} ajouté à {membre.display_name} pour {duree_sec} secondes.")

    await asyncio.sleep(duree_sec)

    # Vérification que le rôle n'a pas été retiré entre-temps
    if role in membre.roles:
        await membre.remove_roles(role, reason="Durée du rôle temporaire expirée")
        logger.info(f"Rôle {role.name} retiré de {membre.display_name} après expiration.")


    

# --------- Messages personnalisés ---------
def get_item_message(valeur):
    messages = {
        "role_GdG": {
            "confirmation":"Veux tu obtenir le ROLE ULTIME le GOAT des GOATs pour **200 000 pièces** ?",
            "success": "Te voici maintenant **le GOAT des GOATs**"
        },
        "boost24h": {
            "confirmation":"Veux tu vraiment acheter un boost de 24h pour **35 000 pièces** ?",
            "success": "Tu as obtenue ton boost xp fois 2 pendant 24h !"
        },
        "MS": {
            "confirmation":"Veux tu obtenir le ROLE Mention Suprême parle trop pour **150 000 pièces**",
            "success":"Tu as obtenue le ROLE Mention Suprême parle trop félicitation !"
        }
        
    }
    return messages.get(valeur, {
        "confirmation": "❓ Article inconnu. Tu veux quand même continuer ?",
        "success": "❌ Article inconnu."
    })

# --------- Vue de confirmation ---------
class ConfirmView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, valeur: str):
        super().__init__(timeout=30)
        self.interaction = interaction
        self.valeur = valeur
        
    @discord.ui.button(label="✅ Confirmer", style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.interaction.user:
            await interaction.response.send_message("❌ Tu ne peux pas confirmer cette action.", ephemeral=True)
            return

        # Valeur par défaut
        success_text = get_item_message(self.valeur)["success"]
        erreur = None

        if self.valeur == "role_GdG":
            if retirer_argent(interaction.user.id, 200000):
                erreur = "❌ Tu n'as pas assez d'argent sur ton compte."
            else:
                await ajouter_role(interaction.user, 1339978184594034802)
                
        if self.valeur == "MS":
            if retirer_argent(interaction.user.id, 150000):
                erreur = "❌ Tu n'as pas assez d'argent sur ton compte."
            else:
                await ajouter_role(interaction.user, 1339978383244656753)

        elif self.valeur == "boost24h":
            if retirer_argent(interaction.user.id, 35000):
                erreur = "❌ Tu n'as pas assez d'argent sur ton compte."
            else:
                # On lance la coroutine de façon "background" (non bloquante)
                asyncio.create_task(ajouter_role_temporaire(interaction.user, 1400473431782330528, JOUR)) #24
                
        # Une seule réponse à l'interaction
        if erreur:
            await interaction.response.send_message(erreur, ephemeral=True)
        else:
            await interaction.response.edit_message(content=success_text, view=None)

        self.stop()

    @discord.ui.button(label="❌ Annuler", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.interaction.user:
            await interaction.response.send_message("❌ Tu ne peux pas annuler cette action.", ephemeral=True)
            return

        await interaction.response.edit_message(content="❌ Achat annulé.", view=None)
        self.stop()

# --------- Menu de la boutique ---------
class BoutiqueMenu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="=== Rôles ==="),
            discord.SelectOption(label="🟥 Role GOAT des GOATs", description="Reçois le rôle GOAT des GOATs", value="role_GdG"),
            discord.SelectOption(label="🟧 Mention Suprême parle trop", description="Tu parles tellement que tu as besoin d'un role", value="MS"),
            discord.SelectOption(label="=== Boost ==="),
            discord.SelectOption(label="🔮 Boost 24H", description="Reçois un rôle qui boost ton xp pendant 24h", value="boost24h")
        ]
        super().__init__(placeholder="Choisis un article...", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        valeur = self.values[0]
        message = get_item_message(valeur)["confirmation"]
        view = ConfirmView(interaction, valeur)
        await interaction.response.send_message(message, view=view, ephemeral=True)

# --------- Vue principale ---------
class BoutiqueView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(BoutiqueMenu())

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.response.is_done():
            await interaction.followup.send("❌ Commande annulée.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Commande annulée.", ephemeral=True)
        self.stop()

# --------- Commande principale ---------
async def boutique(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🛒 Bienvenue dans la Boutique Officielle F1F",
        description="La boutique te permet de dépenser les pièces que tu as gagnées sur le serveur pour obtenir toutes sortes d’avantages !\n"
                    "Utilise le menu déroulant ci-dessous pour parcourir les options disponibles.\n"
                    "Une fois ton choix fait, une double validation te sera proposée pour éviter toute erreur.\n\n"
                    "🎯 Gagne des récompenses, fais évoluer ton profil, et distingue-toi des autres membres !\n"
                    "💡 Des nouveautés seront ajoutées régulièrement, alors n'hésite pas à revenir souvent.",
        color=EMBED_COLOR_RED
    )
    embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_image(url=EMBED_BOUTIQUE_OFFICEL)

    await interaction.followup.send(embed=embed, view=BoutiqueView(), ephemeral=False)
