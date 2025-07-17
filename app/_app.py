from discord import app_commands
import asyncio

from config import os, bot, tree, logger,discord, TOKEN
from qualif import pronos_qualif_logic, visualisation_pronos_qualif_logic, modify_qualif_logic
from race import  visualisation_pronos_course_logic, modify_course
from scrapping_result import scrapping_result_course, scrapping_result_qualif
from tools import help, clear_slash, auto_mod
import error_embed as embed
import classement as ldb
from admin_command import ban
import pronos as pr
import json
import fastf1 as f1api


@bot.event
async def on_ready():
    global command_enabled
    command_enabled = False
    global auto
    auto = False
    print(f"✅ Connecté en tant que {bot.user} !")
    logger.info("BOT LANCER")

# _______________________________________________________________________________________________________________________________


@tree.command(name="ping", description="Répond avec Pong !")
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong !")

# _______________________________________________________________________________________________________________________________


@tree.command(name="say", description="Répète ton message")
@app_commands.describe(message="Le message à répéter")
async def say_slash(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"💬 {message}")

# _______________________________________________________________________________________________________________________________


@tree.command(name="salut", description="Salue quelqu’un")
async def salut_slash(interaction: discord.Interaction):
    await interaction.response.send_message(f"👋 Salut {interaction.user.mention} !")

# _______________________________________________________________________________________________________________________________


@tree.command(name="clear", description="Supprime des messages (admin uniquement)")
@app_commands.describe(nombre="Nombre de messages à supprimer")
async def clearing_tool(interaction: discord.Interaction, nombre: int):
    await clear_slash(interaction, nombre)
# _______________________________________________________________________________________________________________________________


@tree.command(name="help", description="Gives you all the commands you can use with this bot")
async def helping_tools(interaction: discord.Interaction):
    await help(interaction)

# _______________________________________________________________________________________________________________________________


@tree.command(name="pronos_course", description="Enregistre tes pronos dans la base de données")
@app_commands.describe(premier="Le premier", deuxieme="Le deuxième", troisieme="Le troisième", best_lap="Meilleur Tour")
async def submit(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str, best_lap: str):
    await interaction.response.defer(ephemeral=True)
    if (command_enabled):

        pr.pronos(interaction.user.id, str(interaction.user),
                  premier, deuxieme, troisieme, best_lap)
        await interaction.followup.send("Ton prono a bien été pris en compte", ephemeral=True)

    else:
        await embed.Error(interaction, "Il y a une heure pour tout faire, et celle ci n'est pas pour les pronos. Par conséquent ton prono n'a pas pu être enregistré. Si tu veux être notifié des prochaines sessions, utilise /role")

# _______________________________________________________________________________________________________________________________


@tree.command(name="pronos_qualifs", description="Pronostiques Qualification de Formule 1")
@app_commands.describe(premier="Le premier", deuxieme="Le deuxième", troisieme="Le troisième")
async def pronostique_qualification(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str):
    await pronos_qualif_logic(interaction, premier, deuxieme, troisieme)
# _______________________________________________________________________________________________________________________________


@tree.command(name="visualisation_pronos_course", description="Voir mon pronostique de course")
async def voir_pronos_course(interaction: discord.Interaction):
    await visualisation_pronos_course_logic(interaction)
# _______________________________________________________________________________________________________________________________


@tree.command(name="visualisation_pronos_qualif", description="Voir mon pronostique de qualif")
async def voir_pronos_qualif(interaction: discord.Interaction):
    await visualisation_pronos_qualif_logic(interaction)

# _______________________________________________________________________________________________________________________________


@tree.command(name="modify_course", description="Modifie ton pronostique pour la course")
@app_commands.describe(premier="Le premier", deuxieme="Le deuxième", troisieme="Le troisième", meilleur_tour="Meilleur Tour")
async def modifier_pronos(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str, meilleur_tour: str):
    # 👈 Appel ici
    await modify_course(interaction, premier, deuxieme, troisieme, meilleur_tour)

# _______________________________________________________________________________________________________________


@tree.command(name="modify_qualif", description="Modifie ton pronostique pour la qualification")
@app_commands.describe(premier="Le premier", deuxieme="Le deuxième", troisieme="Le troisième")
async def modifier_qualif(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str):
    await modify_qualif_logic(interaction, premier, deuxieme, troisieme)

# _______________________________________________________________________________________________________________


@tree.command(name="admin_result_reasearch_course", description="AC-001")
async def recup_valeur(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator:
        await interaction.response.defer(ephemeral=True)

        try:
            embed = await scrapping_result_course(interaction)
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Erreur pendant le scraping : {e}")
            await interaction.followup.send(
                content="❌ Une erreur est survenue lors de la récupération des résultats.",
                ephemeral=True
            )
    else:
        await embed.chat_you_dont_have_perm(interaction)

# _______________________________________________________________________________________________________________


@tree.command(name="admin_result_reasearch_qualif", description="AC-002")
async def recup_valeur_qualif(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator:
        await interaction.response.defer(ephemeral=True)

        try:
            embed = await scrapping_result_qualif(interaction)
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Erreur pendant le scraping : {e}")
            await interaction.followup.send(
                content="❌ Une erreur est survenue lors de la récupération des résultats.",
                ephemeral=True
            )
    else:
        await embed.chat_you_dont_have_perm(interaction)

# _______________________________________________________________________________________________________________________________

@tree.command(name="leaderboard", description="Affiche le clasement des membres")
async def leaderboard(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = ldb.Leaderboard()
    await interaction.followup.send(embed=embed)
    
# _______________________________________________________________________________________________________________________________
    
@tree.command(name="admin_ban", description="AC-03")
@app_commands.describe(member= "Membre à bannnir", reason = "Raison du bannissement" , article = "Le ou les articles qu'il a enfreint")
async def bannissement(interaction: discord.Interaction, member: discord.Member, reason: str, article: str):
    if interaction.user.guild_permissions.ban_members:
        await interaction.response.defer(ephemeral=True)

        try:
            await ban(interaction, member, reason, article)
            logger.info(f"{interaction.user.name} à banni {member}")
            
        except Exception as e:
            
            logger.error(f"Erreur pendant le ban : {e}")
            await interaction.followup.send(
                content="❌ Une erreur est survenue lors de la récupération des résultats.",
                ephemeral=True
            )
    else:
        await embed.chat_you_dont_have_perm(interaction)
        
# _______________________________________________________________________________________________________________________________
        
@tree.command(name="admin_open", description="Ouvre une session de pronostics pour un temp donné")
@app_commands.describe(duration="temps en heures")
async def create(interaction: discord.Interaction, duration: float):
    if interaction.user.guild_permissions.administrator:
        global auto
        if (not auto):
            await interaction.response.defer()
            global task
            global command_enabled
            command_enabled = True
            task = asyncio.create_task(
                embed.start_Session(interaction, duration))
            await task
            command_enabled = False
        else:
            await interaction.response.defer(ephemeral=True)
            await embed.Error(interaction, "Cette commande n'est pas disponible en mode auto")
    else:
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(embed=await embed.permError(interaction))
        
# _______________________________________________________________________________________________________________________________

@tree.command(name="admin_close", description="Ferme la session de pronos")
async def close(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    if interaction.user.guild_permissions.administrator:
        global auto
        if (not auto):
            global command_enabled
            if (command_enabled):
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
                command_enabled = False
                await interaction.followup.send("Les pronos ont bien été fermés")
            else:
                await embed.Error(interaction, "Il semble qu'aucune session pronos est actuellement ouverte")
        else:
            await embed.Error(interaction, "Cette commande n'est pas disponible en mode manuel")
    else:
        await interaction.followup.send(embed=await embed.permError(interaction))

# _______________________________________________________________________________________________________________________________

@tree.command(name="session", description="Configure manuellement la session des pronos récupère ses résultats, et update le leaderboard")
@app_commands.describe(saison="Année de la saison", location="Nom du Circuit", type="Type de l'événement(Q pour qualif, ou R pour course)")
async def session(interaction: discord.Interaction, saison: int, location: str, type: str):
    interaction.response.defer()
    if interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("⏳ Configuration en cours...", ephemeral=True)
        session = {
            "Saison": saison,
            "Location": location,
            "Session": type.upper()
        }
        os.makedirs('data', exist_ok=True)
        with open('data/Session.json', 'w', encoding='utf-8') as f:
            json.dump(session, f, ensure_ascii=False, indent=4)
        try:
            f1api.getResults()
        except Exception as e:
            interaction.followup.send(f" Erreur : {str(e)}")
        ldb.saveResults()
        os.remove('data/Pronos.json')
        await interaction.followup.send("Le Leaderboard est à jour")
    else:
        await interaction.followup.send(embed=await embed.permError(interaction))
        
# _______________________________________________________________________________________________________________________________

@tree.command(name="admin_status", description="Retourne le status du bot")
async def status(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    if interaction.user.guild_permissions.administrator:
        global auto
        if (auto):
            await interaction.followup.send("Le bot est en mode auto", ephemeral=True)
        else:
            await interaction.followup.send("Le bot est en mode manuel", ephemeral=True)
    else:
        await interaction.followup.send(embed=await embed.permError(interaction))

# _______________________________________________________________________________________________________________________________

@tree.command(name="admin_stop", description="Stop le fonctionnement auto du bot")
async def stop(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    if interaction.user.guild_permissions.administrator:
        global auto
        global task
        if (auto):
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            auto = False
            await interaction.followup.send("Le bot est repassé en mode manuel")
        else:
            await embed.Error(interaction, "Cette commande n'est pas disponible en mode manuel")
    else:
        await interaction.followup.send(embed=await embed.permError(interaction), ephemeral=True)

# _______________________________________________________________________________________________________________________________

@tree.command(name="admin_launch", description="Lance le fonctionnement auto du bot")
async def launch(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator:
        await interaction.response.defer(ephemeral=True)
        global task
        task = asyncio.create_task(auto_mod(interaction))
        await task
    else:
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(embed=await embed.permError(interaction), ephemeral=True)
        
# _______________________________________________________________________________________________________________________________

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

bot.run(TOKEN)
