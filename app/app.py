import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import pandas as pd
import logging

from race import visualisation_pronos_course_logic, pronos_course_logic, modify_course
from qualif import pronos_qualif_logic, visualisation_pronos_qualif_logic, modify_qualif_logic

LOG_LEVEL = logging.INFO
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

file_handler = logging.FileHandler("../log/app.log", mode="a", encoding="utf-8")
file_handler.setLevel(LOG_LEVEL)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN_F1F")

# Activer les intents (obligatoire)
intents = discord.Intents.default()
intents.message_content = True  # Nécessaire pour lire les messages

#Commande de préfix
bot = commands.Bot(command_prefix="/", intents=intents)

tree = bot.tree 

@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Connecté en tant que {bot.user} !")
    logger.info("BOT LANCER")
 
#_______________________________________________________________________________________________________________________________
   
@tree.command(name="ping", description="Répond avec Pong !")
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong !")
    
#_______________________________________________________________________________________________________________________________
   
@tree.command(name="say", description="Répète ton message")
@app_commands.describe(message="Le message à répéter")
async def say_slash(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"💬 {message}")
    
 #_______________________________________________________________________________________________________________________________
   
@tree.command(name="salut", description="Salue quelqu’un")
#@app_commands.describe(user_name="Le nom à saluer (facultatif)")
async def salut_slash(interaction: discord.Interaction):
    await interaction.response.send_message(f"👋 Salut {interaction.user.mention} !")

#_______________________________________________________________________________________________________________________________
  
@tree.command(name="clear", description="Supprime des messages (admin uniquement)")
@app_commands.describe(nombre="Nombre de messages à supprimer")
async def clear_slash(interaction: discord.Interaction, nombre: int):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("🚫 Tu n’as pas la permission.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)  # On indique qu'on va répondre plus tard

    deleted = await interaction.channel.purge(limit=nombre + 1)
    
    await interaction.followup.send(f"🧹 {len(deleted)} messages supprimés !", ephemeral=True)
    
    logger.info(f"{interaction.user.name} à clear {nombre} lignes dans {interaction.channel.name}")

#_______________________________________________________________________________________________________________________________
 
@tree.command(name="help", description="Gives you all the commands you can use with this bot")
#@app_commands.describe(nombre="Commande Help de Base")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📜 Help - Liste des commandes",
        description=f"Salut {interaction.user.mention} ! Voici les commandes que tu peux utiliser :",
        color=discord.Color.red()
    )
    
    embed.add_field(name="/ping", value="Répond avec Pong ! 🏓", inline=False)
    embed.add_field(name="/say", value="Répète ton message 💬", inline=False)
    embed.add_field(name="/salut", value="Salue quelqu’un 👋", inline=False)
    embed.add_field(name="/clear", value="Supprime des messages (admin uniquement) 🧹", inline=False)
    embed.add_field(name="/pronos_qualifs", value="Enregistre ton pronostique pour les qualifications", inline=False)
    embed.add_field(name="/pronos_course", value="Enregistre ton pronostique pour les qualifications",inline=False)
    
    embed.set_footer(text="Bot créé par F1F Team", icon_url="https://cdn.discordapp.com/attachments/1339299411360088226/1367477935392428083/Votre_texte_de_paragraphe_12.png?ex=6871ac52&is=68705ad2&hm=a63fd375a9f30130247df80b936c43e1d93b3a5b16c3415f7a63cac72614058e&")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
    logger.info(f"{interaction.user.name} à demander help dans le salon {interaction.channel.name}")
    
#_______________________________________________________________________________________________________________________________
@tree.command(name="pronos_course", description="Pronostiques Course de Formule 1")
@app_commands.describe(premier = "Le premier", deuxieme = "Le deuxième", troisieme = "Le troisième", meilleur_tour = "Meilleur Tour")
async def prono_race(interaction: discord.Interaction,premier: str, deuxieme: str, troisieme: str, meilleur_tour: str):
    await pronos_course_logic(interaction, premier, deuxieme, troisieme, meilleur_tour)
 
#_______________________________________________________________________________________________________________________________
@tree.command(name="pronos_qualifs", description="Pronostiques Qualification de Formule 1")
@app_commands.describe(premier = "Le premier", deuxieme = "Le deuxième", troisieme = "Le troisième")
async def pronostique_qualification(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str):
    await pronos_qualif_logic(interaction, premier, deuxieme, troisieme)
#_______________________________________________________________________________________________________________________________
@tree.command(name="visualisation_pronos_course", description="Voir mon pronostique de course")
async def voir_pronos_course(interaction: discord.Interaction):
    await visualisation_pronos_course_logic(interaction) 
#_______________________________________________________________________________________________________________________________ 
@tree.command(name="visualisation_pronos_qualif", description="Voir mon pronostique de qualif")
async def voir_pronos_qualif(interaction: discord.Interaction):
    await visualisation_pronos_qualif_logic(interaction)

#_______________________________________________________________________________________________________________________________
@tree.command(name="modify_course", description="Modifie ton pronostique pour la course")
@app_commands.describe(premier = "Le premier", deuxieme = "Le deuxième", troisieme = "Le troisième", meilleur_tour = "Meilleur Tour")
async def modifier_pronos(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str, meilleur_tour: str):
    await modify_course(interaction, premier, deuxieme, troisieme, meilleur_tour)  # 👈 Appel ici

#_______________________________________________________________________________________________________________
@tree.command(name="modify_qualif", description="Modifie ton pronostique pour la qualification")
@app_commands.describe(premier = "Le premier", deuxieme = "Le deuxième", troisieme = "Le troisième")
async def modifier_qualif(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str):
    await modify_qualif_logic(interaction, premier, deuxieme, troisieme)

bot.run(TOKEN)

