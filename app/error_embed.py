from config import EMBED_COLOR_RED, EMBED_IMAGE, EMBED_THUMBNAIL, EMBED_FOOTER_TEXT
import discord


async def chat_you_dont_have_perm(interaction: discord.Interaction):
    embed = discord.Embed(
        title=f"Désolé {interaction.user} !",
        description="On dirait que tu n'as pas les permissions pour utilisé cette commande",
        color=EMBED_COLOR_RED,
    )

    embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_image(url=EMBED_IMAGE)

    await interaction.response.send_message(embed=embed, ephemeral=True)
