import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from datetime import datetime
import os
import pandas as pd
import logging

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
bot = commands.Bot(command_prefix="!", intents=intents)

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

@tree.command(name="pronos_qualifs", description="Pronostiques Qualification de Formule 1")
@app_commands.describe(premier = "Le premier", deuxieme = "Le deuxième", troisieme = "Le troisième")
async def pronos_qualif(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str):
    
    data = []
    tab = {}
    
    file_path = "../data/Result_Course_Pronos_F1F_DEMO.xlsx"
    df = pd.read_excel(file_path)
    
    # Le pseudo que tu veux chercher — ici je suppose que c'est le pseudo Discord
    pseudo_recherche = str(interaction.user)  # par exemple pour chercher avec le pseudo Discord exact
    
    # Filtrer la DataFrame pour la ligne où la colonne 'Pseudo' correspond au pseudo recherché
    resultat = df[df['Pseudo'] == pseudo_recherche]
    
    if resultat.empty:
        embed = discord.Embed(
            title = f"🐐 Merci pour vos pronos {interaction.user} !",
            description="Voici tes pronostiques : ",
            color=discord.Color.red()
        )
        
        embed.add_field(name="Premier 🥇 :", value=f"{premier}", inline=False)
        embed.add_field(name="Deuxième 🥈 :", value=f"{deuxieme}", inline=False)
        embed.add_field(name="Troisème 🥉 :", value=f"{troisieme}", inline=False)
        
        embed.set_footer(text="Bot créé par F1F Team", icon_url="https://cdn.discordapp.com/attachments/1339299411360088226/1367477935392428083/Votre_texte_de_paragraphe_12.png?ex=6871ac52&is=68705ad2&hm=a63fd375a9f30130247df80b936c43e1d93b3a5b16c3415f7a63cac72614058e&")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1339299411360088226/1368544420504272987/Design_sans_titre_2.png?ex=68719910&is=68704790&hm=46bd1e4a625f33cc26d5e029888bef5c265732b842de241daa62662206f13885&")

        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        tab["Pseudo"] = interaction.user
        tab["Premier"] = premier
        tab["Deuxième"] = deuxieme
        tab["Troisième"] = troisieme
        
        data.append(tab)
        
        table = pd.DataFrame(data)
        table.iloc[0]
        file_path = "../data/Result_Qualif_Pronos_F1F_DEMO.xlsx"

        if os.path.exists(file_path):
            # Lire les anciennes données
            old_data = pd.read_excel(file_path)
            # Ajouter les nouvelles lignes
            combined_data = pd.concat([old_data, table], ignore_index=True)
        else:
            # Si fichier n'existe pas, créer juste avec les nouvelles données
            combined_data = table

        # Écrire dans le fichier Excel (remplace l'ancien)
        combined_data.to_excel(file_path, index=False)
        
        logger.info(f"{interaction.user.name} à fais ses pronos qualifs")
    else:
        embed = discord.Embed(
            title = f"Désolé {interaction.user} !",
            description="On dirait que tu as deja fait un pronostique si tu veux le modifier utilise la fonction /modify",
            color=discord.Color.red()
        )
        
        embed.set_footer(text="Bot créé par F1F Team", icon_url="https://cdn.discordapp.com/attachments/1339299411360088226/1367477935392428083/Votre_texte_de_paragraphe_12.png")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1339299411360088226/1368544420504272987/Design_sans_titre_2.png")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        logger.info(f"{interaction.user.name} à tenter de réutiliser la commandes pronos qualifs")
    
 #_______________________________________________________________________________________________________________________________
   
@tree.command(name="pronos_course", description="Pronostiques Course de Formule 1")
@app_commands.describe(premier = "Le premier", deuxieme = "Le deuxième", troisieme = "Le troisième", meilleur_tour = "Meilleur Tour")
async def pronos_course(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str, meilleur_tour: str):
    
    data = []
    tab = {}
    
    file_path = "../data/Result_Course_Pronos_F1F_DEMO.xlsx"
    
    colonnes = ["Pseudo", "Premier", "Deuxième", "Troisième", "MT"]
    
    if not os.path.exists(file_path):
        # Création d'un DataFrame vide avec les colonnes attendues
        df = pd.DataFrame(columns=colonnes)
        df.to_excel(file_path, index=False)
    else:
        df = pd.read_excel(file_path)
        
    df = pd.read_excel(file_path)
    
    # Le pseudo que tu veux chercher — ici je suppose que c'est le pseudo Discord
    pseudo_recherche = str(interaction.user)  # par exemple pour chercher avec le pseudo Discord exact
    
    # Filtrer la DataFrame pour la ligne où la colonne 'Pseudo' correspond au pseudo recherché
    resultat = df[df['Pseudo'] == pseudo_recherche]
    
    if resultat.empty:
        embed = discord.Embed(
            title = f"🐐 Merci pour vos pronos {interaction.user} !",
            description="Voici tes pronostiques : ",
            color=discord.Color.red()
        )
        
        embed.add_field(name="Premier 🥇 :", value=f"{premier}", inline=False)
        embed.add_field(name="Deuxième 🥈 :", value=f"{deuxieme}", inline=False)
        embed.add_field(name="Troisème 🥉 :", value=f"{troisieme}", inline=False)
        embed.add_field(name="Meilleur Tour ⏱️ :", value=f"{meilleur_tour}", inline=False) 
        
        embed.set_footer(text="Bot créé par F1F Team", icon_url="https://cdn.discordapp.com/attachments/1339299411360088226/1367477935392428083/Votre_texte_de_paragraphe_12.png?ex=6871ac52&is=68705ad2&hm=a63fd375a9f30130247df80b936c43e1d93b3a5b16c3415f7a63cac72614058e&")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1339299411360088226/1368544420504272987/Design_sans_titre_2.png?ex=68719910&is=68704790&hm=46bd1e4a625f33cc26d5e029888bef5c265732b842de241daa62662206f13885&")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        tab["Pseudo"] = interaction.user
        tab["Premier"] = premier
        tab["Deuxième"] = deuxieme
        tab["Troisième"] = troisieme
        tab["MT"] = meilleur_tour
        
        data.append(tab)
        
        table = pd.DataFrame(data)
        table.iloc[0]
        file_path = "../data/Result_Course_Pronos_F1F_DEMO.xlsx"

        if os.path.exists(file_path):
            # Lire les anciennes données
            old_data = pd.read_excel(file_path)
            # Ajouter les nouvelles lignes
            combined_data = pd.concat([old_data, table], ignore_index=True)
        else:
            # Si fichier n'existe pas, créer juste avec les nouvelles données
            combined_data = table

        # Écrire dans le fichier Excel (remplace l'ancien)
        combined_data.to_excel(file_path, index=False)
        
        logger.info(f"{interaction.user.name} à fais ses pronos courses")
        
    else:
        embed = discord.Embed(
            title = f"Désolé {interaction.user} !",
            description="On dirait que tu as deja fait un pronostique si tu veux le modifier utilise la fonction /modify",
            color=discord.Color.red()
        )
        
        embed.set_footer(text="Bot créé par F1F Team", icon_url="https://cdn.discordapp.com/attachments/1339299411360088226/1367477935392428083/Votre_texte_de_paragraphe_12.png")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1339299411360088226/1368544420504272987/Design_sans_titre_2.png")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        logger.info(f"{interaction.user.name} à tenter de réutiliser la commandes pronos course")
 
#_______________________________________________________________________________________________________________________________
   
@tree.command(name="visualisation_pronos_course", description="Voir mon pronostique de course")
async def visualisation_pronos_course(interaction: discord.Interaction):
    
    file_path = "../data/Result_Course_Pronos_F1F_DEMO.xlsx"
    df = pd.read_excel(file_path)
    
    # Le pseudo que tu veux chercher — ici je suppose que c'est le pseudo Discord
    pseudo_recherche = str(interaction.user)  # par exemple pour chercher avec le pseudo Discord exact
    
    # Filtrer la DataFrame pour la ligne où la colonne 'Pseudo' correspond au pseudo recherché
    resultat = df[df['Pseudo'] == pseudo_recherche]
    
    if not resultat.empty:
        ligne = resultat.iloc[0]  # OK, il y a au moins une ligne
        
        premier = ligne['Premier']
        deuxieme = ligne['Deuxième']
        troisieme = ligne['Troisième']
        meilleur_tour = ligne['MT']

        embed = discord.Embed(
            title = f"🐐 Merci pour vos pronos {interaction.user} !",
            description="Voici tes pronostiques : ",
            color=discord.Color.red()
        )
        
        embed.add_field(name="Ton Premier 🥇 :", value=f"{premier}", inline=False)
        embed.add_field(name="Ton Deuxième 🥈 :", value=f"{deuxieme}", inline=False)
        embed.add_field(name="Ton Troisième 🥉 :", value=f"{troisieme}", inline=False)
        embed.add_field(name="Ton Meilleur Tour ⏱️ :", value=f"{meilleur_tour}", inline=False) 
        
        embed.set_footer(text="Bot créé par F1F Team", icon_url="https://cdn.discordapp.com/attachments/1339299411360088226/1367477935392428083/Votre_texte_de_paragraphe_12.png")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1339299411360088226/1368544420504272987/Design_sans_titre_2.png")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)  
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
   
#_______________________________________________________________________________________________________________________________
     
@tree.command(name="visualisation_pronos_qualif", description="Voir mon pronostique de qualif")
async def visualisation_pronos_qualif(interaction: discord.Interaction):
    
    
    file_path = "../data/Result_Qualif_Pronos_F1F_DEMO.xlsx"
    df = pd.read_excel(file_path)
    
    # Le pseudo que tu veux chercher — ici je suppose que c'est le pseudo Discord
    pseudo_recherche = str(interaction.user)  # par exemple pour chercher avec le pseudo Discord exact
    
    # Filtrer la DataFrame pour la ligne où la colonne 'Pseudo' correspond au pseudo recherché
    resultat = df[df['Pseudo'] == pseudo_recherche]
    
    if not resultat.empty:
        ligne = resultat.iloc[0]  # OK, il y a au moins une ligne
        
        premier = ligne['Premier']
        deuxieme = ligne['Deuxième']
        troisieme = ligne['Troisième']
        
        embed = discord.Embed(
            title = f"🐐 Merci pour vos pronos {interaction.user} !",
            description="Voici tes pronostiques : ",
            color=discord.Color.red()
        )
        
        embed.add_field(name="Ton Premier 🥇 :", value=f"{premier}", inline=False)
        embed.add_field(name="Ton Deuxième 🥈 :", value=f"{deuxieme}", inline=False)
        embed.add_field(name="Ton Troisième 🥉 :", value=f"{troisieme}", inline=False)
        
        embed.set_footer(text="Bot créé par F1F Team", icon_url="https://cdn.discordapp.com/attachments/1339299411360088226/1367477935392428083/Votre_texte_de_paragraphe_12.png")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1339299411360088226/1368544420504272987/Design_sans_titre_2.png")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)  
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
        

#_______________________________________________________________________________________________________________________________

@tree.command(name="modify_course", description="Modifie ton pronostique pour la course")
@app_commands.describe(premier = "Le premier", deuxieme = "Le deuxième", troisieme = "Le troisième", meilleur_tour = "Meilleur Tour")
async def modify_course(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str, meilleur_tour: str):
    
    file_path = "../data/Result_Course_Pronos_F1F_DEMO.xlsx"
    df = pd.read_excel(file_path)
    
    # Le pseudo que tu veux chercher — ici je suppose que c'est le pseudo Discord
    pseudo_recherche = str(interaction.user)  # par exemple pour chercher avec le pseudo Discord exact
    
    # Filtrer la DataFrame pour la ligne où la colonne 'Pseudo' correspond au pseudo recherché
    resultat = df[df['Pseudo'] == pseudo_recherche].index
    
    if resultat.empty:
        embed = discord.Embed(
            title = f"Désolé {interaction.user} !",
            description="On dirait que tu n'as pas encore fait de pronostique",
            color=discord.Color.red()
        )
        
        embed.set_footer(text="Bot créé par F1F Team", icon_url="https://cdn.discordapp.com/attachments/1339299411360088226/1367477935392428083/Votre_texte_de_paragraphe_12.png")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1339299411360088226/1368544420504272987/Design_sans_titre_2.png")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            title = f"🐐 Merci pour vos pronos {interaction.user} !",
            description="Voici tes pronostiques : ",
            color=discord.Color.red()
        )
        
        embed.add_field(name="Premier 🥇 :", value=f"{premier}", inline=False)
        embed.add_field(name="Deuxième 🥈 :", value=f"{deuxieme}", inline=False)
        embed.add_field(name="Troisème 🥉 :", value=f"{troisieme}", inline=False)
        embed.add_field(name="Meilleur Tour ⏱️ :", value=f"{meilleur_tour}", inline=False) 
        
        embed.set_footer(text="Bot créé par F1F Team", icon_url="https://cdn.discordapp.com/attachments/1339299411360088226/1367477935392428083/Votre_texte_de_paragraphe_12.png?ex=6871ac52&is=68705ad2&hm=a63fd375a9f30130247df80b936c43e1d93b3a5b16c3415f7a63cac72614058e&")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1339299411360088226/1368544420504272987/Design_sans_titre_2.png?ex=68719910&is=68704790&hm=46bd1e4a625f33cc26d5e029888bef5c265732b842de241daa62662206f13885&")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        i = resultat[0]
        
        df.at[i, "Pseudo"] = interaction.user
        df.at[i, "Premier"] = premier
        df.at[i, "Deuxième"] = deuxieme
        df.at[i, "Troisième"] = troisieme
        df.at[i, "MT"] = meilleur_tour
        
        df.to_excel(file_path, index=False)

        

bot.run(TOKEN)

