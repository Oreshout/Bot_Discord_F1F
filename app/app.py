import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

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
    print(f"Connecté en tant que {bot.user} ! Slash commands prêtes.")
    
@tree.command(name="ping", description="Répond avec Pong !")
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong !")
    
    
@tree.command(name="say", description="Répète ton message")
@app_commands.describe(message="Le message à répéter")
async def say_slash(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"💬 {message}")
    
    
@tree.command(name="salut", description="Salue quelqu’un")
@app_commands.describe(user_name="Le nom à saluer (facultatif)")
async def salut_slash(interaction: discord.Interaction, user_name: str = None):
    if user_name is None:
        user_name = interaction.user.mention
    await interaction.response.send_message(f"👋 Salut {user_name} !")

    
@tree.command(name="clear", description="Supprime des messages (admin uniquement)")
@app_commands.describe(nombre="Nombre de messages à supprimer")
async def clear_slash(interaction: discord.Interaction, nombre: int):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("🚫 Tu n’as pas la permission.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)  # On indique qu'on va répondre plus tard

    deleted = await interaction.channel.purge(limit=nombre + 1)
    
    await interaction.followup.send(f"🧹 {len(deleted)} messages supprimés !", ephemeral=True)
    
@tree.command(name="help", description="Gives you all the commands you can use with this bot")
#@app_commands.describe(nombre="Commande Help de Base")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📜 Aide - Liste des commandes",
        description=f"Salut {interaction.user.mention} ! Voici les commandes que tu peux utiliser :",
        color=discord.Color.red()
    )
    
    embed.add_field(name="/ping", value="Répond avec Pong ! 🏓", inline=False)
    embed.add_field(name="/say <message>", value="Répète ton message 💬", inline=False)
    embed.add_field(name="/salut [nom]", value="Salue quelqu’un 👋", inline=False)
    embed.add_field(name="/clear <nombre>", value="Supprime des messages (admin uniquement) 🧹", inline=False)
    
    embed.set_footer(text="Bot créé par Matt")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

    
bot.run(TOKEN)

