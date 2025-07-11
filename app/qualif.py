from config import logger, EMBED_COLOR_RED, EMBED_THUMBNAIL, EMBED_FOOTER_TEXT, EMBED_IMAGE
import os
import discord
import pandas as pd


async def pronos_qualif_logic(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str):

    data = []
    tab = {}

    file_path = "../data/Result_Course_Pronos_F1F_DEMO.xlsx"
    df = pd.read_excel(file_path)

    # Le pseudo que tu veux chercher — ici je suppose que c'est le pseudo Discord
    # par exemple pour chercher avec le pseudo Discord exact
    pseudo_recherche = str(interaction.user)

    # Filtrer la DataFrame pour la ligne où la colonne 'Pseudo' correspond au pseudo recherché
    resultat = df[df['Pseudo'] == pseudo_recherche]

    if resultat.empty:
        embed = discord.Embed(
            title=f"🐐 Merci pour vos pronos {interaction.user} !",
            description="Voici tes pronostiques : ",
            color=EMBED_COLOR_RED
        )

        embed.add_field(name="Premier 🥇 :", value=f"{premier}", inline=False)
        embed.add_field(name="Deuxième 🥈 :", value=f"{deuxieme}", inline=False)
        embed.add_field(name="Troisème 🥉 :",
                        value=f"{troisieme}", inline=False)

        embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url=EMBED_IMAGE)

        await interaction.response.send_message(embed=embed, ephemeral=True)

        tab["Pseudo"] = interaction.user
        tab["Premier"] = premier
        tab["Deuxième"] = deuxieme
        tab["Troisième"] = troisieme

        data.append(tab)

        table = pd.DataFrame(data)
        table.iloc[0]
        file_path = "../data/Result_Qualif_Pronos_F1F_DEMO.xlsx"

        if os.path.exists(file_path):
            # Lire les anciennes données
            old_data = pd.read_excel(file_path)
            # Ajouter les nouvelles lignes
            combined_data = pd.concat([old_data, table], ignore_index=True)
        else:
            # Si fichier n'existe pas, créer juste avec les nouvelles données
            combined_data = table

        # Écrire dans le fichier Excel (remplace l'ancien)
        combined_data.to_excel(file_path, index=False)

        logger.info(f"{interaction.user.name} à fais ses pronos qualifs")
    else:
        embed = discord.Embed(
            title=f"Désolé {interaction.user} !",
            description="On dirait que tu as deja fait un pronostique si tu veux le modifier utilise la fonction /modify",
            color=EMBED_COLOR_RED
        )

        embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url=EMBED_IMAGE)

        await interaction.response.send_message(embed=embed, ephemeral=True)

        logger.info(
            f"{interaction.user.name} à tenter de réutiliser la commandes pronos qualifs")


async def visualisation_pronos_qualif_logic(interaction: discord.Interaction):

    file_path = "../data/Result_Qualif_Pronos_F1F_DEMO.xlsx"
    df = pd.read_excel(file_path)

    # Le pseudo que tu veux chercher — ici je suppose que c'est le pseudo Discord
    # par exemple pour chercher avec le pseudo Discord exact
    pseudo_recherche = str(interaction.user)

    # Filtrer la DataFrame pour la ligne où la colonne 'Pseudo' correspond au pseudo recherché
    resultat = df[df['Pseudo'] == pseudo_recherche]

    if not resultat.empty:
        ligne = resultat.iloc[0]  # OK, il y a au moins une ligne

        premier = ligne['Premier']
        deuxieme = ligne['Deuxième']
        troisieme = ligne['Troisième']

        embed = discord.Embed(
            title=f"🐐 Merci pour vos pronos {interaction.user} !",
            description="Voici tes pronostiques : ",
            color=EMBED_COLOR_RED
        )

        embed.add_field(name="Ton Premier 🥇 :",
                        value=f"{premier}", inline=False)
        embed.add_field(name="Ton Deuxième 🥈 :",
                        value=f"{deuxieme}", inline=False)
        embed.add_field(name="Ton Troisième 🥉 :",
                        value=f"{troisieme}", inline=False)

        embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url=EMBED_IMAGE)

        await interaction.response.send_message(embed=embed, ephemeral=True)

        logger.info(f"{interaction.user.name} a regarder ses pronos qualif")

    else:
        embed = discord.Embed(
            title=f"Désolé {interaction.user} !",
            description="On dirait que tu n'as pas encore fait de pronostique",
            color=EMBED_COLOR_RED
        )

        embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url=EMBED_IMAGE)

        await interaction.response.send_message(embed=embed, ephemeral=True)

        logger.info(
            f"{interaction.user.name} a tenter de regarder ses pronos qualif alors qu'il n'en avais pas fais")


async def modify_qualif_logic(interaction: discord.Interaction, premier: str, deuxieme: str, troisieme: str):

    file_path = "../data/Result_Qualif_Pronos_F1F_DEMO.xlsx"
    df = pd.read_excel(file_path)

    # Le pseudo que tu veux chercher — ici je suppose que c'est le pseudo Discord
    # par exemple pour chercher avec le pseudo Discord exact
    pseudo_recherche = str(interaction.user)

    # Filtrer la DataFrame pour la ligne où la colonne 'Pseudo' correspond au pseudo recherché
    resultat = df[df['Pseudo'] == pseudo_recherche].index

    if resultat.empty:
        embed = discord.Embed(
            title=f"Désolé {interaction.user} !",
            description="On dirait que tu n'as pas encore fait de pronostique",
            color=EMBED_COLOR_RED
        )

        embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url=EMBED_IMAGE)

        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            title=f"🐐 Merci pour vos pronos {interaction.user} !",
            description="Voici tes pronostiques : ",
            color=EMBED_COLOR_RED
        )

        embed.add_field(name="Premier 🥇 :", value=f"{premier}", inline=False)
        embed.add_field(name="Deuxième 🥈 :", value=f"{deuxieme}", inline=False)
        embed.add_field(name="Troisème 🥉 :",
                        value=f"{troisieme}", inline=False)

        embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_image(url=EMBED_IMAGE)

        await interaction.response.send_message(embed=embed, ephemeral=True)

        i = resultat[0]

        df.at[i, "Pseudo"] = interaction.user
        df.at[i, "Premier"] = premier
        df.at[i, "Deuxième"] = deuxieme
        df.at[i, "Troisième"] = troisieme

        df.to_excel(file_path, index=False)
