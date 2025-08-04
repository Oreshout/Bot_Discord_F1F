from discord import app_commands
import asyncio
from config import os, bot, tree, logger, discord, TOKEN, ROLE_ID_F1PADDOCKCLUB
import config as conf
import tools as tool
import error_embed as embed
import classement as ldb
from admin_command import ban
import pronos as pr
import json
import f1api
from datetime import timedelta
from typing import Literal
import economie as eco
import boutique as shop


@bot.event
async def on_ready():
    global command_enabled
    command_enabled = False
    global auto
    auto = False
    print(f"✅ Connecté en tant que {bot.user} !")
    logger.info("BOT LANCER")

# _______________________________________________________________________________________________________________________________


@tree.command(name="admin_clear", description="Supprime des messages (admin uniquement)")
@app_commands.describe(nombre="Nombre de messages à supprimer")
async def clearing_tool(interaction: discord.Interaction, nombre: int):
    await tool.clear_slash(interaction, nombre)
# _______________________________________________________________________________________________________________________________


@tree.command(name="help", description="Gives you all the commands you can use with this bot")
async def helping_tools(interaction: discord.Interaction):
    await tool.help(interaction)

# _______________________________________________________________________________________________________________________________


@tree.command(name="admin_help", description="Gives you all the commands you can use with this bot")
async def admin_helping_tools(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator:
        await tool.help_admin(interaction)
    else:
        await embed.chat_you_dont_have_perm(interaction)

# _______________________________________________________________________________________________________________________________


@tree.command(name="pronos", description="Enregistre tes pronos ou modifie les si tu l'as déjà fait")
@app_commands.describe(
    statue="Type de session (Qualif, Course, Sprint, Sprint_Qualif)",
    premier="Le premier",
    deuxieme="Le deuxième",
    troisieme="Le troisième",
    best_lap="Meilleur tour (uniquement pour Course et Sprint, optionnel pour Qualif)"
)
async def submit(interaction: discord.Interaction,
                 statue: Literal["Course", "Qualif", "Sprint", "Sprint_Qualif"],
                 premier: str,
                 deuxieme: str,
                 troisieme: str,
                 best_lap: str = None):
    await interaction.response.defer(ephemeral=True)
    STATUSES_VALIDES = ["qualif", "course", "sprint", "sprint_qualif"]
    statue_lower = statue.lower()

    if statue_lower not in STATUSES_VALIDES:
        readable = ", ".join([s.capitalize() for s in STATUSES_VALIDES])
        await embed.Error(interaction, f"❌ Statue invalide. Choisis parmi : {readable}.")
        return

    if statue_lower in ["Course", "Sprint"] and not best_lap:
        await embed.Error(interaction, "❌ Pour Course et Sprint, le Meilleur tour est obligatoire.")
        return

    # Pour Qualif, on ignore best_lap
    if statue_lower in ["Qualif", "Sprint_Qualif"]:
        best_lap = None

    if command_enabled:
        try:
            success = pr.pronos_generic(
                str(interaction.user),  # pseudo
                premier,
                deuxieme,
                troisieme,
                statue_lower,
                best_lap
            )
        except Exception as e:
            logger.exception("Erreur pendant l'enregistrement du prono")
            await embed.Error(interaction, f"❌ Erreur pendant l'enregistrement du prono : `{e}`")
            return

        if success:
            await interaction.followup.send("✅ Ton prono a bien été pris en compte !", ephemeral=True)
            logger.info(
                f'{interaction.user} a fait son pronostic {statue_lower}')
        else:
            await embed.Error(interaction, "❌ Tu ne peux modifier ton pronostic qu'une seule fois.")
    else:
        await embed.Error(interaction, "Il y a une heure pour tout faire, et celle-ci n'est pas pour les pronos. Par conséquent ton prono n'a pas pu être enregistré. Si tu veux être notifié des prochaines sessions, utilise /role")

# _______________________________________________________________________________________________________________________________


@tree.command(name="visualisation", description="Te montre tes pronos")
async def visu(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    await pr.visualisation(interaction)
# _______________________________________________________________________________________________________________________________


@tree.command(name="leaderboard", description="Affiche le clasement des membres")
async def leaderboard(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = ldb.Leaderboard()
    await interaction.followup.send(content=None, embed=embed)
    logger.info(f'{interaction.user} à regarder le leaderbord')

# _______________________________________________________________________________________________________________________________


@tree.command(name="admin_ban", description="AC-03")
@app_commands.describe(member="Membre à bannnir", reason="Raison du bannissement", article="Le ou les articles qu'il a enfreint")
async def bannissement(interaction: discord.Interaction, member: discord.Member, reason: str, article: str):
    if interaction.user.guild_permissions.ban_members:
        await interaction.response.defer(ephemeral=True)
        await ban(interaction, member, reason, article)
        logger.info(f"{interaction.user.name} à banni {member}")

    else:
        await embed.chat_you_dont_have_perm(interaction)

# _______________________________________________________________________________________________________________________________


@tree.command(name="admin_open", description="Ouvre une session de pronostics pour un temps donné")
@app_commands.describe(duration="temps en heures", statue="Choix de la session")
async def create(interaction: discord.Interaction, duration: float, statue: Literal["Course", "Qualif", "Sprint", "Sprint_Qualif"]):
    global current_session, command_enabled, auto, task

    if interaction.user.guild_permissions.administrator:
        if not auto:
            await interaction.response.defer()
            current_session = statue
            command_enabled = True
            task = asyncio.create_task(
                tool.start_Session(interaction, duration))
            await task
            command_enabled = False
            current_session = None  # reset à la fin de la session
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
            await interaction.followup.send(f" Erreur : {str(e)}")
            return
        ldb.save_results()
        await interaction.followup.send("Le Leaderboard est à jour")
    else:
        await interaction.followup.send(embed=await embed.permError(interaction))

# _______________________________________________________________________________________________________________________________


@tree.command(name="admin_getresult", description="Mettre à jour l'api")
async def maj_api(interaction: discord.Interaction):
    await interaction.response.defer()
    if interaction.user.guild_permissions.administrator:
        await interaction.followup.send("⏳ Mise à jour en cours...")

        try:
            result = f1api.getResults()

            if result == 0:
                await interaction.followup.send("✅ Résultats mis à jour avec succès.")
            elif result == 1:
                await interaction.followup.send("⚠️ Les résultats ne sont pas encore disponibles. Réessaie plus tard.")
            elif result == 2:
                await interaction.followup.send("❌ L'API FastF1 ne prend pas en charge cette session.")
            elif result == 3:
                await interaction.followup.send("❌ Erreur lors du chargement de la session FastF1.")
            else:
                await interaction.followup.send("❌ Une erreur inattendue est survenue.")

        except Exception as e:
            await interaction.followup.send(f"Erreur : {str(e)}")
    else:
        await interaction.followup.send(embeds=await embed.permError(interaction))

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


async def auto_mod(interaction: discord.Interaction):
    global command_enabled
    global auto
    auto = True
    while (True):
        f1api.getNextEvent()
        await interaction.followup.send("Le mode auto à bien été lancé", ephemeral=True)
        time = tool.Wait()
        logger.info(str(time))
        if (time > 0):
            await asyncio.sleep(time)
            logger.info("C'est l'heure")
            command_enabled = True
            await asyncio.sleep(timedelta(hours=5).total_seconds())
            logger.info("c'est fini")
            command_enabled = False
            f1api.getResults()
            ldb.saveResults()
            if (os.path.exists("data/Pronos.json")):
                os.remove("data/Pronos.json")
        elif (time <= -timedelta(hours=5).total_seconds()):
            break
        else:
            logger.info("C'est l'heure")
            command_enabled = True
            await asyncio.sleep(timedelta(hours=5).total_seconds()+time)
            logger.info("C'est fini")
            command_enabled = False
            f1api.getResults()
            ldb.saveResults()
            if (os.path.exists("data/Pronos.json")):
                os.remove("data/Pronos.json")


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

# _______________________________________________________________________________________________________________________________


@tree.command(name="presentation", description="Laisse moi me présenter et aide moi à trouver mon nom !")
async def presentation(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(f"{interaction.user.mention}, va voir tes MP !", ephemeral=False)
    await tool.presentation_bot(interaction)
    logger.info(f"{interaction.user} a demandé la présentation du BOT")


# _______________________________________________________________________________________________________________________________


@tree.command(name="avis", description="Laisse nous un avis sur le bot !")
async def review(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(f"{interaction.user.mention}, va voir tes MP !", ephemeral=False)
    await tool.avis(interaction)
    logger.info(f"{interaction.user} a donné son avis du BOT")

# _______________________________________________________________________________________________________________________________


@tree.command(name="rules", description="Affiche le règlement d'usage du BOT")
async def reglement(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    await embed.rules(interaction)
    logger.info(f"{interaction.user} a demandé les règles du BOT.")

# _______________________________________________________________________________________________________________________________


@tree.command(name="play_song", description="Joue une musique demander")
@app_commands.describe(title="Nom de la musique")
async def music(interaction: discord.Interaction, title: str):
    if any(role.id == ROLE_ID_F1PADDOCKCLUB for role in interaction.user.roles) or interaction.user.guild_permissions.administrator:
        await interaction.response.defer(ephemeral=True)
        await tool.music_play(interaction, title)
        logger.info(f"{interaction.user} a demandé de la musique au BOT.")

# _______________________________________________________________________________________________________________________________


@bot.tree.command(name="next_event", description="Affiche le prochain événement F1")
async def next_event(interaction: discord.Interaction):
    await interaction.response.defer()

    try:
        # Appelle ta fonction qui met à jour data/Session.json
        f1api.getNextEvent()

        # Lecture du fichier JSON avec les infos du prochain event
        with open('data/Session.json', 'r', encoding='utf-8') as f:
            session = json.load(f)

        embed = discord.Embed(title="🏁 Prochain Événement F1",
                              description=f"Session: {session.get('Session')}\n"
                              f"Round: {session.get('Round')}\n"
                              f"Pays: {session.get('Country')}\n"
                              f"Circuit: {session.get('Location')}\n"
                              f"Saison: {session.get('Saison')}",
                              color=0x0099ff)

        embed.add_field(name="Date / Heure (UTC)",
                        value=session.get('Date'), inline=False)
        embed.set_footer(text="Données via FastF1 API")

        await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send(f"❌ Une erreur est survenue : {e}")

# _______________________________________________________________________________________________________________________________


@tree.command(name="salaire", description="Te permet de récupérer ton salaire journalié")
async def paye(interaction: discord.Interaction):
    await interaction.response.defer()
    msg = eco.salaire(interaction)
    await interaction.followup.send(msg, ephemeral=True)
    logger.info(f"{interaction.user} a demandé son salaire journalié")

# _______________________________________________________________________________________________________________________________


@tree.command(name="solde", description="Te permet de voir ton solde actuelle")
async def solding(interaction: discord.Interaction):
    await interaction.response.defer()
    await eco.voir_solde(interaction)
    logger.info(f"{interaction.user} a regardé son solde")

# _______________________________________________________________________________________________________________________________


@tree.command(name="virement", description="Fais un virement de X argent sur le compte de la personnes que tu choisis.")
@app_commands.describe(somme_a_retirer="L'argent que tu veux envoyé à la personne", member="La personne que a qui tu veux envoyer de l'argent.")
async def vir(interaction: discord.Interaction, somme_a_retirer: int, member: discord.Member):
    await interaction.response.defer()
    await eco.virement(interaction, somme_a_retirer, member)
    logger.info(f"{interaction.user} a fais un virement à {member}")

# _______________________________________________________________________________________________________________________________


@tree.command(name="admin_retrait", description="Fais un retrait de X argent sur le compte de la personnes que tu choisis.")
@app_commands.describe(somme_a_retirer="L'argent que tu veux retirer à la personne", member="La personne que a qui tu veux retirer de l'argent.")
async def ret(interaction: discord.Interaction, somme_a_retirer: int, member: discord.Member):
    if interaction.user.guild_permissions.administrator:
        await interaction.response.defer()
        await eco.retrait(interaction, somme_a_retirer, member)
        logger.info(f"{interaction.user} a fais un retrait à {member}")
    else:
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(embed=await embed.permError(interaction), ephemeral=True)

# _______________________________________________________________________________________________________________________________


@tree.command(name="top", description="Montre les 10 plus grandes richesse du serveur")
async def toop(interaction: discord.Interaction):
    await interaction.response.defer()
    await eco.top(interaction)
    logger.info(f"{interaction.user} à visionné le top 10 du serv")

# _______________________________________________________________________________________________________________________________


@tree.command(name="deposit",  description="Déplace ton argent de ton compte courant au compte bancaire sécurisé")
@app_commands.describe(somme_a_verser="Argent que tu veux viré")
async def depo(interaction: discord.Interaction, somme_a_verser: int):
    await interaction.response.defer()
    await eco.virement_compte_courant_to_protect(interaction, somme_a_verser)
    logger.info(
        f"{interaction.user} a verser **{somme_a_verser}** sur son compte sécurisé.")

# _______________________________________________________________________________________________________________________________


@tree.command(name="solde_proteger", description="T'affiche ton solde sur ton compte protéger")
async def show(interaction: discord.Interaction):
    await interaction.response.defer()
    await eco.voir_solde_proteger(interaction)
    logger.info(f"{interaction.user} a regardé son solde protegé")

# _______________________________________________________________________________________________________________________________


@tree.command(name="withdraw",  description="Déplace ton argent de ton compte protegé au compte courant")
@app_commands.describe(somme_a_verser="Argent que tu veux viré")
async def dwith(interaction: discord.Interaction, somme_a_verser: int):
    await interaction.response.defer()
    await eco.virement_compte_protege_to_courant(interaction, somme_a_verser)
    logger.info(
        f"{interaction.user} a verser **{somme_a_verser}** sur son compte courant.")

# _______________________________________________________________________________________________________________________________


@tree.command(name="boutique", description="Ouvre la boutique")
async def boutic(interaction: discord.Interaction):
    await interaction.response.defer()
    await shop.boutique(interaction)
    logger.info(f"{interaction.user} a ouvert la boutique.")

# _______________________________________________________________________________________________________________________________

@tree.command(name="admin_send_mess", description="Le bot envoi le message de ton choix")
async def send_mess(interaction: discord.Interaction):
    await interaction.response.defer()
    await tool.envoie_de_message(interaction, conf.PRONOS)
    logger.info(f"{interaction.user} a envoyé un message via le bot.")



bot.run(TOKEN)
