from config import logger, EMBED_COLOR_RED, EMBED_THUMBNAIL, EMBED_FOOTER_TEXT, EMBED_IMAGE
import discord
import asyncio
from datetime import timedelta,datetime
from config import os
import fastf1 as f1api
import error_embed as embed
import classement as ldb
import json
from error_embed import info_embed



async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📜 Help - Liste des commandes",
        description=f"Salut {interaction.user.mention} ! Voici les commandes que tu peux utiliser :",
        color=EMBED_COLOR_RED
    )

    embed.add_field(name="/ping", value="Répond avec Pong ! 🏓", inline=False)
    embed.add_field(name="/say", value="Répète ton message 💬", inline=False)
    embed.add_field(name="/salut", value="Salue quelqu’un 👋", inline=False)
    embed.add_field(
        name="/clear", value="Supprime des messages (admin uniquement) 🧹", inline=False)
    embed.add_field(name="/pronos_qualifs",
                    value="Enregistre ton pronostique pour les qualifications", inline=False)
    embed.add_field(name="/pronos_course",
                    value="Enregistre ton pronostique pour les qualifications", inline=False)
    embed.add_field(name="/visualisation_pronos_course",
                    value="Te montre ton pronostique actuel de course", inline=False)
    embed.add_field(name="/visualisation_pronos_qualif",
                    value="Te montre ton pronostique actuel de qualif", inline=False)
    embed.add_field(name="/modify_course",
                    value="Modifie ton pronostique pour la course", inline=False)
    embed.add_field(name="/modify_qualif",
                    value="Modifie ton pronostique pour la qualif", inline=False)

    embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_image(url=EMBED_IMAGE)

    await interaction.response.send_message(embed=embed, ephemeral=True)

    logger.info(
        f"{interaction.user.name} à demander help dans le salon {interaction.channel.name}")


async def clear_slash(interaction: discord.Interaction, nombre: int):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("🚫 Tu n’as pas la permission.", ephemeral=True)
        return

    # On indique qu'on va répondre plus tard
    await interaction.response.defer(ephemeral=True)

    deleted = await interaction.channel.purge(limit=nombre + 1)

    await interaction.followup.send(f"🧹 {len(deleted)} messages supprimés !", ephemeral=True)

    logger.info(
        f"{interaction.user.name} à clear {nombre} lignes dans {interaction.channel.name}")
    
    

                
def Wait():
    try:
        with open('data/Session.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return 1
    delta_t = (datetime.strptime(
        data["Date"], "%d/%m/%Y,%H:%M:%S")-datetime.now()-timedelta(hours=5)).total_seconds()
    return delta_t


async def start_Session(interaction: discord.Interaction, duration: float):
    await info_embed(f"Les pronos sont lancés pour {str(float(duration*60))} minutes ! \n Pensez à voter !", interaction)
    await asyncio.sleep(timedelta(hours=duration).total_seconds())


