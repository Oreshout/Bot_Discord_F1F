import os
import logging
import discord
from dotenv import load_dotenv
from discord.ext import commands

# === 🔐 Chargement des variables d'environnement (.env) ===
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN_F1F")

# === 🧠 Intents Discord (pour messages, membres, etc.) ===
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # facultatif si tu gères les membres

# === 🤖 Bot et Tree pour les commandes slash ===
bot = commands.Bot(command_prefix="/", intents=intents)
tree = bot.tree

# === 📊 (Optionnel) Chargement global des fichiers Excel ===
# Exemple d'utilisation :
# df = pd.read_excel("../data/Result_Course_Pronos_F1F_DEMO.xlsx")

# === 🧾 Logger (fichier journal de logs) ===
LOG_LEVEL = logging.INFO
logger = logging.getLogger("F1F_Bot")
logger.setLevel(LOG_LEVEL)

log_path = "log/app.log"
# Crée le dossier si nécessaire
os.makedirs(os.path.dirname(log_path), exist_ok=True)

file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
file_handler.setLevel(LOG_LEVEL)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# === 🎨 Couleurs & Style pour les embeds ===
EMBED_COLOR_RED = discord.Color.red()
EMBED_COLOR_GREEN = discord.Color.green()
EMBED_COLOR_GOLD = discord.Color.gold()

EMBED_THUMBNAIL = "https://cdn.discordapp.com/attachments/1339299411360088226/1367477935392428083/Votre_texte_de_paragraphe_12.png?ex=6871ac52&is=68705ad2&hm=a63fd375a9f30130247df80b936c43e1d93b3a5b16c3415f7a63cac72614058e&"
EMBED_IMAGE = "https://cdn.discordapp.com/attachments/1339299411360088226/1368544420504272987/Design_sans_titre_2.png?ex=68719910&is=68704790&hm=46bd1e4a625f33cc26d5e029888bef5c265732b842de241daa62662206f13885&"
EMBED_BOUTIQUE_OFFICEL = "https://cdn.discordapp.com/attachments/1212852209491116113/1400458515289739434/Boutique_Officielle_-_2_-_Modifie.png?ex=688cb621&is=688b64a1&hm=76ad76a3246b3f9b3b613f112667873316d601e13c9b5d388effeea8957839cb&"

EMBED_FOOTER_TEXT = "Bot créé par F1F Team (BETA)"
EMBED_FOOTER_ICON = EMBED_THUMBNAIL


# === Scrapping devices ===

CLASS_NAME = 'a'

URL_BASE = "https://fr.motorsport.com/"
URL_RESULT_COURSE = "https://fr.motorsport.com/f1/results/2025"
URL_RESULT_QUALIF = "https://fr.motorsport.com/f1/results/2025/gp-de-grande-bretagne-653245/?st=Q3"

# === Environment variable ===

PRONOS_ID = 1398238150215860345
GUILD_ID = 1394054995523010761
ROLE_ID_F1PADDOCKCLUB = 992784555150946446

# === 🪙 Bot et Tree pour les commandes slash ===
SALAIRE_JOURNALIER = 100

# === Timer ===

JOUR = 86400

# === 🟨 ROLE ===

GOAT_DES_GOATS = 1339978184594034802
SUPREME_PARLE_TROP = 1339978383244656753
MYTHE_DU_SPORT_AUTO = 1339978320745594961
MYTHE_DE_LA_F1 = 1339978247433224303
BOOST_JOUR = 1400473431782330528

# === 🟩 Salon ===

COMMANDE_BOTS = 928612687263444992

