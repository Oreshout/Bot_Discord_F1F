from config import logger, EMBED_COLOR_RED, EMBED_THUMBNAIL, EMBED_FOOTER_TEXT, EMBED_IMAGE
import discord
import asyncio
from datetime import timedelta,datetime
from config import os
import fastf1 as f1api
import classement as ldb
import json
import pandas as pd
from error_embed import info_embed, no_prono



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


async def visualisation(interaction: discord.Interaction):
    
    file_path = "../data/Pronos.json"
    df = pd.read_json(file_path)
    
    # Le pseudo que tu veux chercher — ici je suppose que c'est le pseudo Discord
    user = interaction.user.id # par exemple pour chercher avec le pseudo Discord exact
    
    resultat = False
    # Filtrer la DataFrame pour la ligne où la colonne 'Pseudo' correspond au pseudo recherché
    for user_id, info in df.items():
        if user_id == user:
            resultat = True
            premier = info['1']
            deuxieme = info['2']
            troisieme = info['3']
            best_lap = info['Best Lap']
    
    if resultat:
       
        embed = discord.Embed(
            title = f"🐐 Merci pour vos pronos {interaction.user} !",
            description="Voici tes pronostiques : ",
            color=discord.Color.red()
        )
        
        embed.add_field(name="Ton Premier 🥇 :", value=f"{premier}", inline=False)
        embed.add_field(name="Ton Deuxième 🥈 :", value=f"{deuxieme}", inline=False)
        embed.add_field(name="Ton Troisième 🥉 :", value=f"{troisieme}", inline=False)
        embed.add_field(name="Ton Meilleur Tour ⏱️ :", value=f"{best_lap}", inline=False) 
        
        embed.set_footer(text="Bot créé par F1F Team", icon_url="https://cdn.discordapp.com/attachments/1339299411360088226/1367477935392428083/Votre_texte_de_paragraphe_12.png")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1339299411360088226/1368544420504272987/Design_sans_titre_2.png")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)  
        
        logger.info(f"{interaction.user.name} a regarder ses pronos course")
        
    else:
        embed = discord.Embed(
            title = f"Désolé {interaction.user} !",
            description="On dirait que tu n'as pas encore fait de pronostique",
            color=discord.Color.red()
        )
        
        embed.set_footer(text="Bot créé par F1F Team", icon_url="https://cdn.discordapp.com/attachments/1339299411360088226/1367477935392428083/Votre_texte_de_paragraphe_12.png")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1339299411360088226/1368544420504272987/Design_sans_titre_2.png")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        logger.info(f"{interaction.user.name} a tenter de regarder ses pronos course alors qu'il n'en avais pas fais")
    






