import discord
import json
import os
import random
import config as param

INVENTAIRE_FILE = "data/inventaire_object/personnal_inventaire.json"
COMPTE_FILE = "data/eco/central_account.json"

cartes_par_rarete = {
    "commune": [
        param.JACK_DOOHAN
    ],
    "rare": [
        param.CHARLES_LECLERC,
        param.OSCAR_PIASTRI
    ]
    # Tu peux rajouter "epique", "légendaire", etc.
}



def charger_donnees(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def sauvegarder_donnees(donnees, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=4)


def retirer_argent(user_id: int, montant: int) -> bool:
    donnees = charger_donnees(COMPTE_FILE)
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
        sauvegarder_donnees(donnees, COMPTE_FILE)
        return False

async def donner_starter_pack(interaction: discord.Interaction):

    # 🟩 1 carte commune
    carte_commune = random.choice(cartes_par_rarete["commune"])

    # 🎲 2 cartes aléatoires (on peut mélanger toutes les raretés)
    toutes_les_cartes = (
        cartes_par_rarete["commune"]
        + cartes_par_rarete["rare"]
        + cartes_par_rarete["epique"]
        + cartes_par_rarete["legendaire"]
    )
    cartes_random = random.sample(toutes_les_cartes, 2)

    # 📦 Ajout des cartes à l'inventaire
    await ajouter_carte_in_inventaire(interaction, carte_commune)
    for carte in cartes_random:
        await ajouter_carte_in_inventaire(interaction, carte)

    # ✅ Feedback
    await interaction.response.send_message("🎉 Ton Pack Starter a été ouvert avec succès !", ephemeral=True)
    

async def ajouter_carte_in_inventaire(interaction: discord.Interaction, carte_id: str):
    user_id = str(interaction.user.id)
    username = interaction.user.name

    # Charger ou initialiser l'inventaire
    if not os.path.exists(INVENTAIRE_FILE):
        inventaire = {}
    else:
        with open(INVENTAIRE_FILE, 'r', encoding='utf-8') as f:
            inventaire = json.load(f)

    # Créer un inventaire vide si utilisateur inexistant
    if user_id not in inventaire:
        inventaire[user_id] = {
            "Pseudo": username,
            "Cartes": []
        }

    # Ajouter la carte si pas déjà présente (facultatif, selon ton design)
    if carte_id in inventaire[user_id]["Cartes"]:
        await interaction.followup.send(f"⚠️ Tu possèdes déjà la carte `{carte_id}`.", ephemeral=True)
        return

    inventaire[user_id]["Cartes"].append(carte_id)

    # Sauvegarder l’inventaire
    with open(INVENTAIRE_FILE, 'w', encoding='utf-8') as f:
        json.dump(inventaire, f, indent=4, ensure_ascii=False)

    await interaction.followup.send(f"🃏 La carte `{carte_id}` a été ajoutée à ton inventaire avec succès !", ephemeral=True)


class InventairePaginationView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, cartes: list, username: str):
        super().__init__(timeout=60)
        self.interaction = interaction
        self.cartes = cartes
        self.username = username
        self.index = 0

        self.message = None  # sera défini plus tard

    async def update_embed(self):
        embed = discord.Embed(
            title="🃏 Carte obtenue",
            description=f"{self.interaction.user.mention}, voici ta carte **{self.index + 1} / {len(self.cartes)}** :",
            color=param.EMBED_COLOR_RED
        )
        embed.set_image(url=self.cartes[self.index])
        embed.set_footer(text=f"{self.username} • Inventaire")

        await self.message.edit(embed=embed, view=self)

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.interaction.user.id:
            await interaction.response.send_message("❌ Tu ne peux pas interagir avec cet inventaire.", ephemeral=True)
            return

        self.index = (self.index - 1) % len(self.cartes)
        await interaction.response.defer()
        await self.update_embed()

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.interaction.user.id:
            await interaction.response.send_message("❌ Tu ne peux pas interagir avec cet inventaire.", ephemeral=True)
            return

        self.index = (self.index + 1) % len(self.cartes)
        await interaction.response.defer()
        await self.update_embed()

async def afficher_cartes_inventaire(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    username = interaction.user.name

    # Chargement de l'inventaire
    if not os.path.exists(INVENTAIRE_FILE):
        await interaction.followup.send("❌ Aucun inventaire trouvé pour l’instant.", ephemeral=True)
        return

    with open(INVENTAIRE_FILE, 'r', encoding='utf-8') as f:
        inventaire = json.load(f)

    if user_id not in inventaire:
        await interaction.followup.send("📭 Tu n’as pas encore d’inventaire. Utilise la commande d’obtention pour en créer un !", ephemeral=True)
        return

    cartes = inventaire[user_id].get("Cartes", [])

    if not cartes:
        await interaction.followup.send("🕳️ Ton inventaire est vide. Obtiens des cartes pour commencer ta collection !", ephemeral=True)
        return

    # Permet de traiter l'envoi en plusieurs messages
    await interaction.response.defer(ephemeral=True)

     # Déclenche l'affichage avec pagination
    view = InventairePaginationView(interaction, cartes, username)

    embed = discord.Embed(
        title="🃏 Carte obtenue",
        description=f"{interaction.user.mention}, voici ta carte **1 / {len(cartes)}** :",
        color=discord.Color.orange()
    )
    embed.set_image(url=cartes[0])
    embed.set_footer(text=f"{username} • Inventaire")

    view.message = await interaction.followup.send(embed=embed, view=view)


def get_item_message(valeur):
    messages = {
        "starter": {
            "confirmation": "Souhaites-tu vraiment acheter un Pack Starter pour 20 000 goats ?",
            "success": "Félicitations, tu viens d’ouvrir un Pack Starter !"
        },
        "random": {
            "confirmation": "Souhaites-tu vraiment acheter un Pack Random pour 60 000 goats ?",
            "success": "Félicitations, tu viens d’ouvrir un Pack Random !"
        },
        "elite": {
            "confirmation": "Souhaites-tu vraiment acheter un Pack Elite pour 100 000 goats ?",
            "success": "Félicitations, tu viens d’ouvrir un Pack Elite !"
        },
        "legende": {
            "confirmation": "Souhaites-tu vraiment acheter un Pack Légende pour 250 000 goats ?",
            "success": "Félicitations, tu viens d’ouvrir un Pack Légende !"
        },
        "JD": {
            "confirmation": "Souhaites-tu vraiment acheter une Carte Commune pour 10 000 goats ?",
            "success": "Félicitations, tu viens d’obtenir une Carte Commune!"
        },
        "CL": {
            "confirmation": "Souhaites-tu vraiment acheter une Carte Commune pour 10 000 goats ?",
            "success": "Félicitations, tu viens d’obtenir une Carte Commune!"
        }
    }
    return messages.get(valeur, {
        "confirmation": "❓ Article inconnu. Tu veux quand même continuer ?",
        "success": "❌ Article inconnu."
    })

# --------- Vue de confirmation ---------


class ConfirmView(discord.ui.View):
    def __init__(self, valeur: str, user_id: int, username: str, timeout: float = 30):
        super().__init__(timeout=timeout)
        self.add_item(ConfirmButton(valeur, user_id, username))
        self.add_item(CancelButton())


class ConfirmButton(discord.ui.Button):
    def __init__(self, valeur: str, user_id: int, username: str):
        super().__init__(label="✅ Confirmer", style=discord.ButtonStyle.success)
        self.valeur = valeur
        self.user_id = str(user_id)
        self.username = username

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        # Définir le coût de l’objet
        prix_objets = {
            "starter": 20000,
            "random": 60000,
            "elite": 100000,
            "legende": 250000,
            "JD": 10000,
            "CL": 10000
        }
        prix = prix_objets.get(self.valeur, 0)

        # Vérifier si l'utilisateur a assez d'argent
        pas_assez_argent = retirer_argent(self.user_id, prix)
        if pas_assez_argent:
            await interaction.followup.send("💸 Tu n’as pas assez de goats pour acheter cet objet !", ephemeral=True)
            return

        # 🎁 Logique d'achat selon l'objet
        if self.valeur == "starter":
            await ajouter_carte_in_inventaire(interaction, "carte_commune_1")
            await ajouter_carte_in_inventaire(interaction, "carte_random_1")
            await ajouter_carte_in_inventaire(interaction, "carte_random_2")
        if self.valeur == "random":
            for i in range(5):
                await ajouter_carte_in_inventaire(interaction, f"carte_random_{i+1}")
        if self.valeur == "elite":
            for i in range(4):
                await ajouter_carte_in_inventaire(interaction, f"carte_random_{i+1}")
            await ajouter_carte_in_inventaire(interaction, "carte_epique")
        if self.valeur == "legende":
            await ajouter_carte_in_inventaire(interaction, "carte_legendaire_1")
            await ajouter_carte_in_inventaire(interaction, "carte_legendaire_2")
            await ajouter_carte_in_inventaire(interaction, "carte_mythique")
        if self.valeur == "JD":
            await ajouter_carte_in_inventaire(interaction, param.JACK_DOOHAN)
        if self.valeur == "CL":
            await ajouter_carte_in_inventaire(interaction, param.CHARLES_LECLERC)
        else:
            await interaction.followup.send("❌ Objet non reconnu.", ephemeral=True)
            return

        # Message de succès
        success_msg = get_item_message(self.valeur)["success"]
        await interaction.followup.send(success_msg, ephemeral=True)


class CancelButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="❌ Annuler", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("❌ Action annulée.", ephemeral=True)
        self.view.stop()
# --------- Menu de la boutique ---------


class BoutiqueMenu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="=== Packs ==="),
            discord.SelectOption(label="🎁 Starter",
                                 description="Reçois un Pack Starter (1 commune + 2 aléatoires) pour 20 000", value="starter"),
            discord.SelectOption(label="🎲 Random",
                                 description="Reçois un Pack Random (5 cartes aléatoires) pour 60 000 goats .", value="random"),
            discord.SelectOption(label="🏆 Pack Elite",
                                 description="Reçois un Pack Elite (5 cartes, au moins 1 épique) pour 100 000 goats.", value="elite"),
            discord.SelectOption(
                label="🔥 Pack Légende", description="Reçois un Pack Légende (3 cartes légendaires ou mythiques) pour 250 000 goats.", value="legende"),
            discord.SelectOption(label="=== Cartes Individuelles ==="),
            discord.SelectOption(label="=== 🟢 Commune 🟢 ===",
                                 description="Reçois une Carte Commune pour 10 000 goats."),
            discord.SelectOption(label="Jack Doohan", value="JD"),
            discord.SelectOption(label="Charles Leclerc", value="CL")
        ]
        super().__init__(placeholder="Choisis un article...",
                         options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        valeur = self.values[0]
        message = get_item_message(valeur)["confirmation"]
        view = ConfirmView(valeur, interaction.user.id, interaction.user.name)

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
            await interaction.followup.send("❌ Commande annulée.", ephemeral=True)
        self.stop()

# --------- Commande principale ---------


async def boutique_carte(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🛒 Bienvenue dans la Boutique Officielle F1F",
        description="La boutique te permet de dépenser les pièces que tu as gagnées sur le serveur pour obtenir toutes sortes d’avantages !\n"
                    "Utilise le menu déroulant ci-dessous pour parcourir les options disponibles.\n"
                    "Une fois ton choix fait, une double validation te sera proposée pour éviter toute erreur.\n\n"
                    "🎯 Gagne des récompenses, fais évoluer ton profil, et distingue-toi des autres membres !\n"
                    "💡 Des nouveautés seront ajoutées régulièrement, alors n'hésite pas à revenir souvent.",
        color=param.EMBED_COLOR_RED
    )
    embed.set_footer(text=param.EMBED_FOOTER_TEXT,
                     icon_url=param.EMBED_THUMBNAIL)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_image(url=param.EMBED_BOUTIQUE_OFFICEL)

    await interaction.followup.send(embed=embed, view=BoutiqueView(), ephemeral=False)
