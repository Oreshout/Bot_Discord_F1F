from discord import app_commands
import asyncio
from config import os, bot, tree, logger,discord, TOKEN
from tools import help, clear_slash,start_Session,Wait,presentation_bot
import error_embed as embed
import classement as ldb
from admin_command import ban
import pronos as pr
import json
import f1api
from datetime import timedelta,datetime


@bot.event
async def on_ready():
    global command_enabled
    command_enabled = False
    global auto
    auto = False
    print(f"✅ Connecté en tant que {bot.user} !")
    logger.info("BOT LANCER")


@bot.event
async def on_message(message: discord.Message):
    # Nos ID pour pouvoir etre les seuls à pouvoir lancer la commande
    owners_id = [1256311918319112294, 1200489866165747722,]
    if (not message.author.bot):
        if message.content == "!sync":
            if message.author.id not in owners_id:
                logger.warning(
                    f"{str(message.author.id)} alias {message.author.display_name} a tenté de sync le bot")
                await message.delete()
            else:
                synced = await tree.sync()
                try:
                    await message.author.send(f"🔄 {len(synced)} commandes slash synchronisées.")
                except discord.Forbidden:
                    message.channel.send("Je n'ai pas pu t'envoyer de dm mais "+len(
                        synced)+" commandes ont été correctement synchronisées")
                    asyncio.sleep(5)
                    pass
                await message.delete()
                
# _______________________________________________________________________________________________________________________________

@tree.command(name="presentation", description="Laisse moi me présenter et aide moi à trouver mon nom !")
async def presentation(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(f"{interaction.user.mention}, va voir tes MP !", ephemeral=False)
    await presentation_bot(interaction)

bot.run(TOKEN)
