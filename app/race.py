
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
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
bot = commands.Bot(command_prefix="/", intents=intents)

tree = bot.tree 


async def pronos_course_logic(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str, meilleur_tour: str):
    
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




async def visualisation_pronos_course_logic(interaction: discord.Interaction):
    
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
