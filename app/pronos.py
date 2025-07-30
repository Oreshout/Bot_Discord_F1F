# Gestion des pronostiques, écriture et lecture
import json
import os
import re
import discord
import fastf1 as f1
from fastf1 import get_session
from datetime import datetime, timezone
import pandas as pd
from config import logger, EMBED_COLOR_RED, EMBED_IMAGE, EMBED_THUMBNAIL, EMBED_FOOTER_TEXT
import tools as tool

def get_session_name():
    # Lecture des infos de session depuis le fichier JSON
    with open('data/Session.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    saison = data['Saison']
    location = data['Location']
    statue = data['Session']  # ex: "Qualifying", "Race", etc.

    try:
        session = get_session(saison, location, statue)
        session.load()  # Nécessaire pour avoir SessionName
        return session.session_name  # ex: "QUALIFYING", "RACE", "SPRINT"
    except Exception as e:
        print(f"Erreur lors du chargement de la session : {e}")
        return "Session inconnue"

def sanitize_filename(name):
    return re.sub(r'[^\w\-]', '_', name)


def country_fonction():
    year = datetime.now(timezone.utc).year
    calendar = f1.get_event_schedule(year)
    now = datetime.now(timezone.utc)

    for row in calendar.itertuples():
        if pd.isna(row.Session5DateUtc):
            continue
        elif now <= row.Session5DateUtc.replace(tzinfo=timezone.utc):
            return sanitize_filename(row.Country)

    return "Unknown"  # fallback par défaut si rien trouvé



def pronos_generic(pseudo, premier, second, troisieme, statue, best_lap=None):
    country = country_fonction()

    if statue == "qualif":
        file_path = f'data/pronos_{country}_qualifs.json'
    elif statue == "sprint":
        file_path = f'data/pronos_{country}_sprint.json'
    elif statue == "sprint_qualif":
        file_path = f'data/pronos_{country}_qualifsprint.json'
    else:
        file_path = f'data/pronos_{country}.json'

    if not os.path.exists(file_path):
        pronos_database = {}
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            pronos_database = json.load(f)

    user_key = pseudo  # ou id si tu as

    # Si l'utilisateur a déjà un prono enregistré
    if user_key in pronos_database:
        # Si Modif est déjà True, on bloque la modif
        if pronos_database[user_key].get("Modif", False) is True:
            return False  # modification refusée

        # Sinon on autorise la modif et on passe Modif à True
        pronos_database[user_key]["1"] = premier
        pronos_database[user_key]["2"] = second
        pronos_database[user_key]["3"] = troisieme
        pronos_database[user_key]["Modif"] = True
        if statue in ["course", "sprint"]:
            pronos_database[user_key]["Best Lap"] = best_lap

    else:
        # Premier prono, Modif = False par défaut
        pronos_database[user_key] = {
            "Pseudo": pseudo,
            "1": premier,
            "2": second,
            "3": troisieme,
            "Modif": False
        }
        if statue in ["course", "sprint"]:
            pronos_database[user_key]["Best Lap"] = best_lap

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(pronos_database, f, ensure_ascii=False, indent=4)

    return True  # prono pris en compte


async def visualisation(interaction: discord.Interaction):

    try:
        country = country_fonction()
        file_path_course = f'data/pronos_{country}.json'
        file_path_qualif = f'data/pronos_{country}_qualifs.json'

        tool.ensure_file_exists(file_path_course)
        tool.ensure_file_exists(file_path_qualif)

        with open(file_path_course, 'r', encoding='utf-8') as f:
            pronos_database = json.load(f)

        with open(file_path_qualif, 'r', encoding='utf-8') as f:
            pronos_database_qualif = json.load(f)

    except Exception as e:
        await interaction.followup.send(
            content=f"❌ Une erreur est survenue lors du chargement des fichiers : {e}",
            ephemeral=True
        )
        return

    user_id = interaction.user.name

    # Protection si le JSON est vide ou corrompu
    if not isinstance(pronos_database, dict):
        pronos_database = {}

    if not isinstance(pronos_database_qualif, dict):
        pronos_database_qualif = {}

    # Cas : seulement prono course
    if user_id in pronos_database and user_id not in pronos_database_qualif:
        prono = pronos_database[user_id]
        embed = discord.Embed(
            title=f"🐐 Merci pour vos pronos {interaction.user} !",
            color=EMBED_COLOR_RED
        )
        embed.description = "Voici tes pronostics de course :"
        embed.add_field(name="Ton Premier 🥇 :", value=prono.get(
            "1", "Non renseigné"), inline=False)
        embed.add_field(name="Ton Deuxième 🥈 :", value=prono.get(
            "2", "Non renseigné"), inline=False)
        embed.add_field(name="Ton Troisième 🥉 :", value=prono.get(
            "3", "Non renseigné"), inline=False)
        embed.add_field(name="Ton Meilleur Tour ⏱️ :", value=prono.get(
            "Best Lap", "Non renseigné"), inline=False)

        modif_text = "❌ Tu as déjà modifié ton pronostic par le passé" if prono.get(
            "Modif", True) else "✅ Tu peux modifier ton pronostic en relançant /pronos"
        embed.add_field(name="Droit de modification :",
                        value=modif_text, inline=False)
        
        embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url=EMBED_IMAGE)

    # Cas : seulement prono qualif
    elif user_id in pronos_database_qualif and user_id not in pronos_database:
        prono = pronos_database_qualif[user_id]
        embed = discord.Embed(
            title=f"🐐 Merci pour vos pronos {interaction.user} !",
            color=EMBED_COLOR_RED
        )
        embed.description = "Voici tes pronostics de qualif :"
        embed.add_field(name="Ton Premier 🥇 :", value=prono.get(
            "1", "Non renseigné"), inline=False)
        embed.add_field(name="Ton Deuxième 🥈 :", value=prono.get(
            "2", "Non renseigné"), inline=False)
        embed.add_field(name="Ton Troisième 🥉 :", value=prono.get(
            "3", "Non renseigné"), inline=False)

        modif_text = "❌ Tu as déjà modifié ton pronostic par le passé" if prono.get(
            "Modif", True) else "✅ Tu peux modifier ton pronostic en relançant /pronos"
        embed.add_field(name="Droit de modification :",
                        value=modif_text, inline=False)
        
        embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url=EMBED_IMAGE)

    # Cas : les deux pronos existent
    elif user_id in pronos_database and user_id in pronos_database_qualif:
        pr_course = pronos_database[user_id]
        pr_qualif = pronos_database_qualif[user_id]
        embed = discord.Embed(
            title=f"🐐 Merci pour vos pronos {interaction.user} !",
            color=EMBED_COLOR_RED
        )

        embed.description = "Voici tes pronostics complets :"

        embed.add_field(name="**Qualif - Premier 🥇**",
                        value=pr_qualif.get("1", "Non renseigné"), inline=False)
        embed.add_field(name="**Qualif - Deuxième 🥈**",
                        value=pr_qualif.get("2", "Non renseigné"), inline=False)
        embed.add_field(name="**Qualif - Troisième 🥉**",
                        value=pr_qualif.get("3", "Non renseigné"), inline=False)

        embed.add_field(name="**Course - Premier 🥇**",
                        value=pr_course.get("1", "Non renseigné"), inline=False)
        embed.add_field(name="**Course - Deuxième 🥈**",
                        value=pr_course.get("2", "Non renseigné"), inline=False)
        embed.add_field(name="**Course - Troisième 🥉**",
                        value=pr_course.get("3", "Non renseigné"), inline=False)
        embed.add_field(name="**Meilleur Tour ⏱️**",
                        value=pr_course.get("Best Lap", "Non renseigné"), inline=False)

        modif_q = "❌ Qualif déjà modifié" if pr_qualif.get(
            "Modif", True) else "✅ Tu peux modifier ton prono Qualif (/pronos)"
        modif_c = "❌ Course déjà modifié" if pr_course.get(
            "Modif", True) else "✅ Tu peux modifier ton prono Course (/pronos)"
        embed.add_field(name="Droits de modification :",
                        value=f"{modif_q}\n{modif_c}", inline=False)
        
        embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url=EMBED_IMAGE)

    # Cas : aucun prono
    else:
        embed = discord.Embed(
            title=f"Désolé {interaction.user} !",
            description="On dirait que tu n'as pas encore fait de pronostic.",
            color=EMBED_COLOR_RED
        )

    # Envoi final
    await interaction.followup.send(embed=embed, ephemeral=True)
    logger.info(f"{interaction.user} à visualisé ses pronos.")
