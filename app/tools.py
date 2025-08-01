from config import logger, bot, EMBED_COLOR_RED, EMBED_THUMBNAIL, EMBED_FOOTER_TEXT, EMBED_IMAGE
import discord
import asyncio
from datetime import timedelta, datetime
from config import os
import yt_dlp
import json
from error_embed import info_embed


def ensure_file_exists(path):
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({}, f)
            
            
async def help_admin(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔐 Help Admin - Commandes réservées aux admins",
        description=f"Bonjour {interaction.user.mention}, voici les commandes **admin** disponibles :",
        color=discord.Color.red()
    )

    # Modération
    embed.add_field(name="/admin_clear", value="🧹 Supprime un nombre défini de messages", inline=False)
    embed.add_field(name="/admin_ban", value="🔨 Bannir un membre avec raison et article", inline=False)

    # Gestion des pronostics
    embed.add_field(name="/admin_open", value="🟢 Ouvre une session de pronos pour une durée donnée", inline=False)
    embed.add_field(name="/admin_close", value="🔴 Ferme la session de pronos en cours", inline=False)
    embed.add_field(name="/session", value="🗂️ Configure manuellement une session + update leaderboard", inline=False)
    embed.add_field(name="/admin_getresult", value="🔄 Force la mise à jour des résultats via l’API", inline=False)

    # Gestion du bot
    embed.add_field(name="/admin_status", value="📊 Affiche le mode actuel du bot : manuel ou auto", inline=False)
    embed.add_field(name="/admin_stop", value="⛔ Stoppe le mode automatique du bot", inline=False)
    embed.add_field(name="/admin_launch", value="🚀 Lance le mode automatique du bot", inline=False)

    # Économie (admin)
    embed.add_field(name="/admin_retrait", value="💼 Retire de l'argent d’un membre", inline=False)

    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
    embed.set_image(url=EMBED_IMAGE)

    await interaction.response.send_message(embed=embed, ephemeral=True)

    logger.info(f"{interaction.user.name} a demandé /help_admin dans {interaction.channel.name}")



async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📜 Help - Liste des commandes",
        description=f"Salut {interaction.user.mention} ! Voici les commandes disponibles :",
        color=EMBED_COLOR_RED
    )

    # Commandes générales
    embed.add_field(name="/help", value="📖 Affiche cette liste d’aide", inline=False)
    embed.add_field(name="/presentation", value="🤖 Laisse le bot se présenter et choisis-lui un nom", inline=False)
    embed.add_field(name="/rules", value="📏 Affiche le règlement d’utilisation du bot", inline=False)

    # F1 – Pronos
    embed.add_field(name="/pronos", value="🏁 Enregistre ou modifie tes pronostics", inline=False)
    embed.add_field(name="/visualisation", value="🔍 Affiche tes pronos actuels", inline=False)
    embed.add_field(name="/leaderboard", value="🏆 Affiche le classement général", inline=False)
    embed.add_field(name="/next_event", value="📅 Affiche le prochain événement F1", inline=False)

    # Musique
    embed.add_field(name="/play_song", value="🎶 Joue une chanson demandée", inline=False)

    # Économie virtuelle
    embed.add_field(name="/salaire", value="💸 Récupère ton salaire quotidien", inline=False)
    embed.add_field(name="/solde", value="💰 Affiche ton solde actuel", inline=False)
    embed.add_field(name="/virement", value="🏦 Transfère de l’argent à un autre membre", inline=False)
    embed.add_field(name="/top", value="📊 Classement des plus riches du serveur", inline=False)
    embed.add_field(name="/deposit", value="🔒 Dépose de l'argent sur ton compte protégé", inline=False)
    embed.add_field(name="/withdraw", value="🔓 Retire de l'argent de ton compte protégé", inline=False)
    embed.add_field(name="/solde_proteger", value="🧾 Affiche ton solde protégé", inline=False)
    embed.add_field(name="/boutique", value="🛍️ Ouvre la boutique", inline=False)

    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
    embed.set_image(url=EMBED_IMAGE)

    await interaction.response.send_message(embed=embed, ephemeral=True)

    logger.info(f"{interaction.user.name} a demandé /help dans {interaction.channel.name}")


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


async def presentation_bot(interaction: discord.Interaction):

    file_path = 'data/NameBot.json'

    embed = discord.Embed(
        title="Présentation du Bot + Concours de Nom 🏁",
        description=(
            "👋 **Bonjour à toi, fan de Formule 1 !**\n\n"
            "Je suis **le nouveau bot officiel** de la communauté **Formula 1 France**. Mon rôle ? "
            "T’accompagner pendant toute la saison avec des outils pratiques comme la récupération de tes pronostics et des infos à jour sur les Grands Prix ! 🇫🇷🏎️\n\n"

            "Sois indulgent avec moi, je viens tout juste d’être lancé : je suis encore en **BETA** 🥺\n\n"

            "📊 D’autres fonctions arrivent bientôt : infos circuits, classements en direct, statistiques pilotes, et même un jeu spécial F1F!\n\n"

            "🎉 __**Et maintenant, place au concours !**__\n\n"
            "🤔 Mes créateurs ne m’ont pas encore donné de nom... C’est là que **toi** tu entres en jeu !\n"
            "Propose-moi un nom original, fun ou en rapport avec la F1 et F1F, **et si ta proposition est retenue, elle deviendra mon nom officiel trop bien non ?!**\n\n"

            " 📬__Pour participer :__\n"
            "Répond simplement à **ce message privé** avec ton idée de nom pour le bot.\n"
            "**Une seule condition : que ce soit cool, en rapport avec la Formule 1 et F1F (le mot GOAT est fortement conseillé) !!**\n\n"

            "🏆 Le vainqueur sera annoncé sur le serveur et gagnera une **petite surprise** 👀\n\n"
            "À toi de jouer, et que le meilleur nom gagne ! 🏎️✨"
        ),
        color=discord.Color.red()
    )

    embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_image(url=EMBED_IMAGE)

    try:
        await interaction.user.send(embed=embed)

        msg = await bot.wait_for(
            "message",
            check=lambda m: m.author == interaction.user and isinstance(
                m.channel, discord.DMChannel)
        )

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                data = json.loads(content) if content else {}
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data[str(msg.author.name)] = msg.content

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=True)

        await interaction.user.send("Merci pour ta proposition !")

    except discord.Forbidden:
        await interaction.channel.send("Je n'ai pas pu envoyer le message")

    if interaction.guild is None:
        logger.info(f"Présentation par {interaction.user.name} en MP")
    else:
        logger.info(
            f"Présentation par {interaction.user.name} dans {interaction.channel.name} sur {interaction.guild.name}")


async def music_play(interaction: discord.Interaction, song_name: str):
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True

    if not interaction.guild.voice_client:
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            await channel.connect()
            await interaction.response.send_message("✅ Rejoint le salon vocal", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Tu dois être dans un salon vocal", ephemeral=True)
            return

    voice = interaction.guild.voice_client

    if not voice:
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            voice = await channel.connect()
        else:
            await interaction.response.send_message("❌ Tu dois être dans un salon vocal", ephemeral=True)
            return

    await interaction.response.send_message(f"🔍 Recherche : **{song_name}**", ephemeral=True)

    ydl_opts = {'format': 'bestaudio', 'noplaylist': 'True'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{song_name}", download=False)['entries'][0]
            stream_url = info['url']
            found_title = info.get('title', song_name)
        except Exception as e:
            await interaction.followup.send(f"❌ Impossible de lire la musique. Erreur : {e}")
            return

    # Définir la fonction avant de l'utiliser
    async def auto_leave_if_idle(voice_client, delay=300):
        await asyncio.sleep(delay)
        if not voice_client.is_playing() and not voice_client.is_paused():
            await voice_client.disconnect()
            logger.info("⏹️ Déconnexion automatique après 5 minutes d'inactivité.")
            await interaction.followup.send("⏹️ Déconnexion automatique après 5 minutes d'inactivité.**")
            # Ici, interaction n'est plus garanti safe. Tu peux notifier ailleurs si besoin.

    def after_playing(err):
        if err:
            print(f"Erreur de lecture : {err}")
        asyncio.create_task(auto_leave_if_idle(voice))

    audio_source = discord.FFmpegPCMAudio(stream_url)
    voice.play(audio_source, after=after_playing)

    await interaction.followup.send(f"🎶 Lecture : **{found_title}**")
