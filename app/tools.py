from config import logger, bot, EMBED_COLOR_RED, EMBED_THUMBNAIL, EMBED_FOOTER_TEXT, EMBED_IMAGE
import discord
import asyncio
from datetime import timedelta,datetime
from config import os
import fastf1 as f1api
import classement as ldb
import json
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


async def presentation_bot(interaction: discord.Interaction):
    
    file_path = 'data/NameBot.json'
    
    embed = discord.Embed(
    title="📢 Présentation du Bot + Concours de Nom 🏁",
    description=(
        "👋 **Bonjour à toi, fan de Formule 1 !**\n\n"
        "Je suis **le nouveau bot officiel** de la communauté **Formula 1 France**. Mon rôle ? "
        "T’accompagner pendant toute la saison avec des outils pratiques, des pronostics et des infos à jour sur les Grands Prix ! 🇫🇷🏎️\n\n"

        "__**🔧 Commandes utiles :**__\n"
        "• `/pronos_course` → Donne ton podium de course\n"
        "• `/pronos_qualifs` → Donne ton top 3 en qualifications\n"
        "• `/visualisation_pronos_course` → Consulte ton pronostic\n"
        "• `/modify_course` → Modifie ton choix avant le départ\n\n"

        "📊 D’autres fonctions arrivent bientôt : infos circuits, classements en direct, statistiques pilotes...\n\n"
        
        "---\n\n"

        "🎉 **Et maintenant, place au concours !**\n\n"
        "🤔 Mon créateur ne m’a pas encore donné de nom... C’est là que **toi** tu entres en jeu !\n"
        "Propose-moi un nom original, fun ou en rapport avec la F1 – **et si ta proposition est retenue, elle deviendra mon nom officiel !**\n\n"

        "__📬 Pour participer :__\n"
        "Répond simplement à **ce message privé** avec ton idée de nom pour le bot.\n"
        "**Une seule condition : que ce soit cool et en rapport avec la Formule 1 !**\n\n"

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
            check=lambda m: m.author == interaction.user and isinstance(m.channel, discord.DMChannel)
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

    logger.info(f"{interaction.user.name} à demander une présentation dans le salon {interaction.channel.name}")




