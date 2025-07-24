# Gestion des pronostiques, écriture et lecture
import json
import os
import re
import discord
import fastf1 as f1
from datetime import datetime, timezone
import pandas as pd
from config import logger
import tools as tool


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


def pronos(id: int, pseudo: str, premier: str, second: str, troisieme: str, bt: str):

    country = country_fonction()
    file_path = f'data/pronos_{country}.json'

    if not os.path.exists(file_path):
        pronos_database = {
            str(id): {
                "Pseudo": pseudo,
                "1": premier,
                "2": second,
                "3": troisieme,
                "Best Lap": bt,
                "Modif": False
            }
        }
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            pronos_database = json.load(f)
            if str(id) not in pronos_database:
                pronos_database[str(id)] = {
                    "Pseudo": pseudo,
                    "1": premier,
                    "2": second,
                    "3": troisieme,
                    "Best Lap": bt,
                    "Modif": False
                }
            else:
                if pronos_database[str(id)]["Modif"]:
                    return False
                else:

                    pronos_database[str(id)]["Pseudo"] = pseudo
                    pronos_database[str(id)]["1"] = premier
                    pronos_database[str(id)]["2"] = second
                    pronos_database[str(id)]["3"] = troisieme
                    pronos_database[str(id)]["Best Lap"] = bt
                    pronos_database[str(id)]["Modif"] = True

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(pronos_database, f, ensure_ascii=False, indent=4)
    return True


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

    user_id = str(interaction.user.id)

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
            color=discord.Color.red()
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
            "Modif", True) else "✅ Tu peux modifier ton pronostic en relançant /pronos_course"
        embed.add_field(name="Droit de modification :",
                        value=modif_text, inline=False)

    # Cas : seulement prono qualif
    elif user_id in pronos_database_qualif and user_id not in pronos_database:
        prono = pronos_database_qualif[user_id]
        embed = discord.Embed(
            title=f"🐐 Merci pour vos pronos {interaction.user} !",
            color=discord.Color.red()
        )
        embed.description = "Voici tes pronostics de qualif :"
        embed.add_field(name="Ton Premier 🥇 :", value=prono.get(
            "1", "Non renseigné"), inline=False)
        embed.add_field(name="Ton Deuxième 🥈 :", value=prono.get(
            "2", "Non renseigné"), inline=False)
        embed.add_field(name="Ton Troisième 🥉 :", value=prono.get(
            "3", "Non renseigné"), inline=False)

        modif_text = "❌ Tu as déjà modifié ton pronostic par le passé" if prono.get(
            "Modif", True) else "✅ Tu peux modifier ton pronostic en relançant /pronos_qualif"
        embed.add_field(name="Droit de modification :",
                        value=modif_text, inline=False)

    # Cas : les deux pronos existent
    elif user_id in pronos_database and user_id in pronos_database_qualif:
        pr_course = pronos_database[user_id]
        pr_qualif = pronos_database_qualif[user_id]
        embed = discord.Embed(
            title=f"🐐 Merci pour vos pronos {interaction.user} !",
            color=discord.Color.red()
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
            "Modif", True) else "✅ Tu peux modifier ton prono Qualif (/pronos_qualif)"
        modif_c = "❌ Course déjà modifié" if pr_course.get(
            "Modif", True) else "✅ Tu peux modifier ton prono Course (/pronos_course)"
        embed.add_field(name="Droits de modification :",
                        value=f"{modif_q}\n{modif_c}", inline=False)

    # Cas : aucun prono
    else:
        embed = discord.Embed(
            title=f"Désolé {interaction.user} !",
            description="On dirait que tu n'as pas encore fait de pronostic.",
            color=discord.Color.red()
        )

    # Envoi final
    await interaction.followup.send(embed=embed, ephemeral=True)
    logger.info(f"{interaction.user} à visualisé ses pronos.")


def pronos_qualif(id: int, pseudo: str, premier: str, second: str, troisieme: str):

    country = country_fonction()
    file_path = f'data/pronos_{country}_qualifs.json'

    if not os.path.exists(file_path):
        pronos_database = {
            str(id): {
                "Pseudo": pseudo,
                "1": premier,
                "2": second,
                "3": troisieme,
                "Modif": False
            }
        }
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            pronos_database = json.load(f)
            if str(id) not in pronos_database:
                pronos_database[str(id)] = {
                    "Pseudo": pseudo,
                    "1": premier,
                    "2": second,
                    "3": troisieme,
                    "Modif": False
                }
            else:
                if pronos_database[str(id)]["Modif"]:
                    return False
                else:

                    pronos_database[str(id)]["Pseudo"] = pseudo
                    pronos_database[str(id)]["1"] = premier
                    pronos_database[str(id)]["2"] = second
                    pronos_database[str(id)]["3"] = troisieme
                    pronos_database[str(id)]["Modif"] = True

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(pronos_database, f, ensure_ascii=False, indent=4)
    return True
