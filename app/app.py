from config import bot, tree, discord,  logger, TOKEN, EMBED_COLOR_RED, EMBED_THUMBNAIL, EMBED_FOOTER_TEXT
from discord import app_commands

from qualif import pronos_qualif_logic, visualisation_pronos_qualif_logic, modify_qualif_logic
from race import pronos_course_logic, visualisation_pronos_course_logic, modify_course
from tools import help, clear_slash



@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Connecté en tant que {bot.user} !")
    logger.info("BOT LANCER")
 
#_______________________________________________________________________________________________________________________________
   
@tree.command(name="ping", description="Répond avec Pong !")
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong !")
    
#_______________________________________________________________________________________________________________________________
   
@tree.command(name="say", description="Répète ton message")
@app_commands.describe(message="Le message à répéter")
async def say_slash(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"💬 {message}")
    
 #_______________________________________________________________________________________________________________________________
   
@tree.command(name="salut", description="Salue quelqu’un")
async def salut_slash(interaction: discord.Interaction):
    await interaction.response.send_message(f"👋 Salut {interaction.user.mention} !")

#_______________________________________________________________________________________________________________________________
  
@tree.command(name="clear", description="Supprime des messages (admin uniquement)")
@app_commands.describe(nombre="Nombre de messages à supprimer")
async def clearing_tool(interaction: discord.Interaction, nombre: int):
    await clear_slash(interaction, nombre)
#_______________________________________________________________________________________________________________________________
 
@tree.command(name="help", description="Gives you all the commands you can use with this bot")
async def helping_tools(interaction: discord.Interaction):
    await help(interaction)
    
#_______________________________________________________________________________________________________________________________
@tree.command(name="pronos_course", description="Pronostiques Course de Formule 1")
@app_commands.describe(premier = "Le premier", deuxieme = "Le deuxième", troisieme = "Le troisième", meilleur_tour = "Meilleur Tour")
async def prono_race(interaction: discord.Interaction,premier: str, deuxieme: str, troisieme: str, meilleur_tour: str):
    await pronos_course_logic(interaction, premier, deuxieme, troisieme, meilleur_tour)
 
#_______________________________________________________________________________________________________________________________
@tree.command(name="pronos_qualifs", description="Pronostiques Qualification de Formule 1")
@app_commands.describe(premier = "Le premier", deuxieme = "Le deuxième", troisieme = "Le troisième")
async def pronostique_qualification(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str):
    await pronos_qualif_logic(interaction, premier, deuxieme, troisieme)
#_______________________________________________________________________________________________________________________________
@tree.command(name="visualisation_pronos_course", description="Voir mon pronostique de course")
async def voir_pronos_course(interaction: discord.Interaction):
    await visualisation_pronos_course_logic(interaction) 
#_______________________________________________________________________________________________________________________________ 
@tree.command(name="visualisation_pronos_qualif", description="Voir mon pronostique de qualif")
async def voir_pronos_qualif(interaction: discord.Interaction):
    await visualisation_pronos_qualif_logic(interaction)

#_______________________________________________________________________________________________________________________________
@tree.command(name="modify_course", description="Modifie ton pronostique pour la course")
@app_commands.describe(premier = "Le premier", deuxieme = "Le deuxième", troisieme = "Le troisième", meilleur_tour = "Meilleur Tour")
async def modifier_pronos(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str, meilleur_tour: str):
    await modify_course(interaction, premier, deuxieme, troisieme, meilleur_tour)  # 👈 Appel ici

#_______________________________________________________________________________________________________________
@tree.command(name="modify_qualif", description="Modifie ton pronostique pour la qualification")
@app_commands.describe(premier = "Le premier", deuxieme = "Le deuxième", troisieme = "Le troisième")
async def modifier_qualif(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str):
    await modify_qualif_logic(interaction, premier, deuxieme, troisieme)

bot.run(TOKEN)

