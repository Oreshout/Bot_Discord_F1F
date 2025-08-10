import discord
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

intents = discord.Intents.default()
intents.members = True

def generate_welcome_image(member: discord.Member) -> str:
    """
    Génère une image de bienvenue à partir du template et de l'avatar du membre.
    Retourne le chemin du fichier final.
    """

    # Charger l'image template
    template = Image.open("sprites/welcome.png").convert("RGBA")

    # Récupérer l'avatar du membre (correctement avec display_avatar)
    avatar_url = member.display_avatar.url
    response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(response.content)).convert("RGBA")

    # Redimensionner l'avatar pour qu'il rentre dans le cercle prévu
    avatar_size = (350, 350)  # Ajuster selon ton image
    avatar = avatar.resize(avatar_size)

    # Créer un masque circulaire
    mask = Image.new("L", avatar.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, avatar.size[0], avatar.size[1]), fill=255)
    avatar.putalpha(mask)

    # Coller l'avatar sur le template (coordonnées à ajuster)
    template.paste(avatar, (650, 275), avatar)

    # Ajouter le texte avec le pseudo
    draw = ImageDraw.Draw(template)
    font = ImageFont.truetype("sprites/Font/Formula1-Black.ttf", 70)  # Tu peux mettre une autre police
    draw.text((500, 700), f"Bienvenue \n {member.display_name} !", font=font, fill=(255, 215, 0))  # Jaune or

    # Sauvegarder l'image finale
    output_path = f"sprites/bvn_craft/welcome_{member}.png"
    template.save(output_path)

    return output_path
