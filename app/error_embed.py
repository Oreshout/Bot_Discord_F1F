from config import logger, EMBED_COLOR_RED, EMBED_IMAGE, EMBED_THUMBNAIL, EMBED_FOOTER_TEXT, PRONOS_ID
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
    role = interaction.guild.get_role(PRONOS_ID)
    embed = discord.Embed(
        title="Infos",
        description=message,
        color=EMBED_COLOR_RED
    )

    embed.set_footer(text=EMBED_FOOTER_TEXT)
    embed.set_image(url=EMBED_IMAGE)
    embed.set_thumbnail(url=EMBED_THUMBNAIL)
    await interaction.followup.send(
        content=f"||{role.mention}||",
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