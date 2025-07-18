from discord import app_commands

from config import bot, tree, logger, discord, TOKEN
from qualif import pronos_qualif_logic, visualisation_pronos_qualif_logic, modify_qualif_logic
from race import pronos_course_logic, visualisation_pronos_course_logic, modify_course
from scrapping_result import scrapping_result_course, scrapping_result_qualif
from tools import help, clear_slash
from error_embed import chat_you_dont_have_perm
from classement import embed_classement, calculer_classement
from read_docs import read_the_docs


@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Connecté en tant que {bot.user} !")
    logger.info("BOT LANCER")

# _______________________________________________________________________________________________________________________________


@tree.command(name="ping", description="Répond avec Pong !")
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong !")

# _______________________________________________________________________________________________________________________________


@tree.command(name="say", description="Répète ton message")
@app_commands.describe(message="Le message à répéter")
async def say_slash(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"💬 {message}")

# _______________________________________________________________________________________________________________________________


@tree.command(name="salut", description="Salue quelqu’un")
async def salut_slash(interaction: discord.Interaction):
    await interaction.response.send_message(f"👋 Salut {interaction.user.mention} !")

# _______________________________________________________________________________________________________________________________


@tree.command(name="clear", description="Supprime des messages (admin uniquement)")
@app_commands.describe(nombre="Nombre de messages à supprimer")
async def clearing_tool(interaction: discord.Interaction, nombre: int):
    await clear_slash(interaction, nombre)
# _______________________________________________________________________________________________________________________________


@tree.command(name="help", description="Gives you all the commands you can use with this bot")
async def helping_tools(interaction: discord.Interaction):
    await help(interaction)

# _______________________________________________________________________________________________________________________________


@tree.command(name="pronos_course", description="Pronostiques Course de Formule 1")
@app_commands.describe(premier="Le premier", deuxieme="Le deuxième", troisieme="Le troisième", meilleur_tour="Meilleur Tour")
async def prono_race(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str, meilleur_tour: str):
    await pronos_course_logic(interaction, premier, deuxieme, troisieme, meilleur_tour)

# _______________________________________________________________________________________________________________________________


@tree.command(name="pronos_qualifs", description="Pronostiques Qualification de Formule 1")
@app_commands.describe(premier="Le premier", deuxieme="Le deuxième", troisieme="Le troisième")
async def pronostique_qualification(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str):
    await pronos_qualif_logic(interaction, premier, deuxieme, troisieme)
# _______________________________________________________________________________________________________________________________


@tree.command(name="visualisation_pronos_course", description="Voir mon pronostique de course")
async def voir_pronos_course(interaction: discord.Interaction):
    await visualisation_pronos_course_logic(interaction)
# _______________________________________________________________________________________________________________________________


@tree.command(name="visualisation_pronos_qualif", description="Voir mon pronostique de qualif")
async def voir_pronos_qualif(interaction: discord.Interaction):
    await visualisation_pronos_qualif_logic(interaction)

# _______________________________________________________________________________________________________________________________


@tree.command(name="modify_course", description="Modifie ton pronostique pour la course")
@app_commands.describe(premier="Le premier", deuxieme="Le deuxième", troisieme="Le troisième", meilleur_tour="Meilleur Tour")
async def modifier_pronos(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str, meilleur_tour: str):
    # 👈 Appel ici
    await modify_course(interaction, premier, deuxieme, troisieme, meilleur_tour)

# _______________________________________________________________________________________________________________


@tree.command(name="modify_qualif", description="Modifie ton pronostique pour la qualification")
@app_commands.describe(premier="Le premier", deuxieme="Le deuxième", troisieme="Le troisième")
async def modifier_qualif(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str):
    await modify_qualif_logic(interaction, premier, deuxieme, troisieme)

# _______________________________________________________________________________________________________________


@tree.command(name="admin_result_reasearch_course", description="AC-001")
async def recup_valeur(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator:
        await interaction.response.defer(ephemeral=True)

        try:
            embed = await scrapping_result_course(interaction)
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Erreur pendant le scraping : {e}")
            await interaction.followup.send(
                content="❌ Une erreur est survenue lors de la récupération des résultats.",
                ephemeral=True
            )
    else:
        await chat_you_dont_have_perm(interaction)

# _______________________________________________________________________________________________________________


@tree.command(name="admin_result_reasearch_qualif", description="AC-002")
async def recup_valeur_qualif(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator:
        await interaction.response.defer(ephemeral=True)

        try:
            embed = await scrapping_result_qualif(interaction)
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Erreur pendant le scraping : {e}")
            await interaction.followup.send(
                content="❌ Une erreur est survenue lors de la récupération des résultats.",
                ephemeral=True
            )
    else:
        await chat_you_dont_have_perm(interaction)

# _______________________________________________________________________________________________________________________________


@tree.command(name="classement", description="Affiche le classement des pronostics")
async def classement(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    
    output_file_path = "../data/Classement_Qualif.xlsx"

    resultats = read_the_docs(interaction, "../data/resultats_qualif.json")
    pronostics = read_the_docs(
        interaction, "../data/Result_Qualif_Pronos_F1F_DEMO.xlsx")

    if resultats is None or pronostics is None:
        await interaction.followup.send("Erreur : Fichier(s) manquant(s)", ephemeral=True)
        return

    classement_df = calculer_classement(resultats, pronostics, output_file_path)
    classement = classement_df.values.tolist()  # convertit en liste de tuples
    embed = embed_classement(classement)

    await interaction.followup.send(embed=embed, ephemeral=True)


bot.run(TOKEN)
