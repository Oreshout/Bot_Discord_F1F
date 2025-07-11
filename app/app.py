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
async def on_ready_slash():
    await tree.sync()
    print(f"Connecté en tant que {bot.user} ! Slash commands prêtes.")

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user} !")

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong !")
    
@tree.command(name="ping", description="Répond avec Pong !")
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong !")
    
@bot.command()
async def say(ctx, *, message):
    await ctx.send(f"💬 {message}")
    
@tree.command(name="say", description="Répète ton message")
@app_commands.describe(message="Le message à répéter")
async def say_slash(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"💬 {message}")
    
@bot.command()
async def salut(ctx):
    user_name = ctx.author.name
    await ctx.send(f"👋 Salut {user_name} !")
    
@tree.command(name="salut", description="Salue quelqu’un")
@app_commands.describe(nom="Le nom à saluer (facultatif)")
async def salut_slash(interaction: discord.Interaction, nom: str = "inconnu"):
    await interaction.response.send_message(f"👋 Salut {nom} !")

    
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, nombre: int = 5):
    await ctx.channel.purge(limit=nombre + 1)
    await ctx.send(f"🧹 {nombre} messages supprimés", delete_after=3)
    
@tree.command(name="clear", description="Supprime des messages (admin uniquement)")
@app_commands.describe(nombre="Nombre de messages à supprimer")
async def clear_slash(interaction: discord.Interaction, nombre: int):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("🚫 Tu n’as pas la permission.", ephemeral=True)
        return

    deleted = await interaction.channel.purge(limit=nombre + 1)
    await interaction.response.send_message(f"🧹 {len(deleted)-1} messages supprimés !", ephemeral=True)

    
bot.run(TOKEN)

