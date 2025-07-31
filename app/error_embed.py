from config import logger, EMBED_COLOR_RED, EMBED_IMAGE, EMBED_THUMBNAIL, EMBED_FOOTER_TEXT
import discord


async def chat_you_dont_have_perm(interaction: discord.Interaction):
    embed = discord.Embed(
        title=f"Désolé {interaction.user} !",
        description="On dirait que tu n'as pas les permissions pour utilisé cette commande",
        color=EMBED_COLOR_RED
    )

    embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_image(url=EMBED_IMAGE)

    await interaction.response.send_message(embed=embed, ephemeral=True)


async def chat_Oops(interaction: discord.Interaction):
    embed = discord.Embed(
        title=f"Désolé {interaction.user} !",
        description="Oops ca ne fonctionne pas!",
        color=EMBED_COLOR_RED
    )

    embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_image(url=EMBED_IMAGE)

    await interaction.response.send_message(embed=embed, ephemeral=True)


async def info_embed(message: str, interaction: discord.Interaction):
    embed = discord.Embed(
        title="Infos",
        description=message,
        color=EMBED_COLOR_RED
    )

    embed.set_footer(text=EMBED_FOOTER_TEXT)
    embed.set_image(url=EMBED_IMAGE)
    embed.set_thumbnail(url=EMBED_THUMBNAIL)
    await interaction.followup.send(
        ephemeral=False,
        embed=embed
    )


async def permError(interaction: discord.Interaction):
    logger.warning(
        f"{str(interaction.user.id)} alias {interaction.user} a tenté de lancer une commande sans en avoir les droits")
    embed = discord.Embed(
        title="❌ Tu n'a pas les permissions pour cette commande",
        color=EMBED_COLOR_RED
    )
    embed.set_footer(text=EMBED_FOOTER_TEXT)
    embed.set_image(url=EMBED_IMAGE)
    embed.set_thumbnail(url=EMBED_THUMBNAIL)
    return embed


async def Error(interaction: discord.Interaction, erreur: str):
    embed = discord.Embed(
        title="❌ Oups, une erreur est survenue",
        description=erreur,
        color=EMBED_COLOR_RED,
    )
    embed.set_footer(text=EMBED_FOOTER_TEXT)
    embed.set_image(url=EMBED_IMAGE)
    embed.set_thumbnail(url=EMBED_THUMBNAIL)
    await interaction.followup.send(
        ephemeral=True,
        embed=embed
    )


async def no_prono(interaction: discord.Interaction):
    embed = discord.Embed(
        title="❌ Oups, on dirait que tu n'as pas fais de pronos",
        description=f"{interaction.user.name} utilise la fonction pronos !",
        color=EMBED_COLOR_RED,
    )
    embed.set_footer(text=EMBED_FOOTER_TEXT)
    embed.set_image(url=EMBED_IMAGE)
    embed.set_thumbnail(url=EMBED_THUMBNAIL)
    await interaction.followup.send(
        ephemeral=True,
        embed=embed
    )


async def rules(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📕 Règlement de Formula 1 France BOT",
        description=f"{interaction.user.name}, en utilisant ce bot vous acceptez automatiquement les règles ci-dessous.",
        color=EMBED_COLOR_RED,
    )

    embed.add_field(
        name="1️⃣ Respect des utilisateurs",
        value="Tout comportement irrespectueux, insultant ou toxique envers les autres utilisateurs est strictement interdit.",
        inline=False,
    )

    embed.add_field(
        name="2️⃣ Utilisation correcte des commandes",
        value="L'utilisation répétée ou abusive des commandes dans un court laps de temps peut entraîner une suspension temporaire de vos accès au bot.",
        inline=False,
    )

    embed.add_field(
        name="3️⃣ Sécurité & protection",
        value="N'essayez en aucun cas de modifier, injecter ou perturber le fonctionnement du bot. Toute tentative d'exploitation de faille sera signalée.",
        inline=False,
    )

    embed.add_field(
        name="4️⃣ Confidentialité des données",
        value="Aucune donnée sensible n’est collectée. Les pronostics et scores sont uniquement utilisés à des fins de classement et d’animation du serveur.",
        inline=False,
    )

    embed.add_field(
        name="5️⃣ Commandes réservées",
        value="Certaines commandes sont réservées aux administrateurs ou modérateurs. Toute tentative d’accès non autorisé sera sanctionnée.",
        inline=False,
    )

    embed.add_field(
        name="6️⃣ Signalement de bugs",
        value="Si vous remarquez un bug, merci de le signaler rapidement à l'équipe via le salon dédié. Ne tentez pas d'en profiter à votre avantage.",
        inline=False,
    )

    embed.add_field(
        name="7️⃣ Règlement évolutif",
        value="Ce règlement est susceptible d’évoluer. Vous serez informé de tout changement dans les annonces officielles du serveur.",
        inline=False,
    )

    embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_image(url=EMBED_IMAGE)

    await interaction.followup.send(embed=embed, ephemeral=True)
