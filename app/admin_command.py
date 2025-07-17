from config import EMBED_COLOR_RED, EMBED_THUMBNAIL, EMBED_FOOTER_TEXT, EMBED_IMAGE
from error_embed import chat_Oops
import discord

async def ban(interaction: discord.Interaction, member: discord.Member, reason:str, article: str):
    try:
        await discord.Member.ban(reason=reason, article=article)
        
        embed = discord.Embed(
        title=f"Le membre {member} à été banni!",
        description="Zoup dehors",
        color=EMBED_COLOR_RED
    )

        embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url=EMBED_IMAGE)

        await interaction.response.send_message(embed=embed, ephemeral=False)
        
    except ValueError:
        chat_Oops(interaction)
    
    