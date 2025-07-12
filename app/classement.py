import discord
import os
from config import logger, EMBED_COLOR_RED, EMBED_THUMBNAIL, EMBED_FOOTER_TEXT, EMBED_IMAGE
import pandas as pd

def calculer_classement(resultats, pronostics_df, output_file_path):
    classement = []

    # Convertir JSON en dict position -> nom
    resultats_dict = {int(pos): nom for pos, nom in resultats}

    for _, row in pronostics_df.iterrows():
        pseudo = row["Pseudo"]
        score = 0

        # Si tout est bon → +5 points
        if (
            row.get("Premier", "").strip().lower() == resultats_dict.get(1, "").strip().lower() and
            row.get("Deuxième", "").strip().lower() == resultats_dict.get(2, "").strip().lower() and
            row.get("Troisième", "").strip().lower() == resultats_dict.get(3, "").strip().lower()
        ):
            score += 5
        else:
            # Comparaison Premier
            if "Premier" in row and 1 in resultats_dict:
                if row["Premier"].strip().lower() == resultats_dict[1].strip().lower():
                    score += 1
                elif row["Premier"].strip().lower() in [
                    resultats_dict[2].strip().lower(), resultats_dict[3].strip().lower()
                ]:
                    score += 0.5

            # Comparaison Deuxième
            if "Deuxième" in row and 2 in resultats_dict:
                if row["Deuxième"].strip().lower() == resultats_dict[2].strip().lower():
                    score += 1
                elif row["Deuxième"].strip().lower() in [
                    resultats_dict[1].strip().lower(), resultats_dict[3].strip().lower()
                ]:
                    score += 0.5

            # Comparaison Troisième
            if "Troisième" in row and 3 in resultats_dict:
                if row["Troisième"].strip().lower() == resultats_dict[3].strip().lower():
                    score += 1
                elif row["Troisième"].strip().lower() in [
                    resultats_dict[1].strip().lower(), resultats_dict[2].strip().lower()
                ]:
                    score += 0.5

        # Ajouter au classement
        classement.append((pseudo, score))

    # Trier par score décroissant
    classement.sort(key=lambda x: x[1], reverse=True)

    # Création du DataFrame à partir du classement calculé
    colonnes = ["Pseudo", "Score"]
    df_classement = pd.DataFrame(classement, columns=colonnes)

    # Sauvegarde dans le fichier Excel
    df_classement.to_excel(output_file_path, index=False)

    logger.info(f"✅ Classement sauvegardé dans : {output_file_path}")

    return df_classement

# _______________________________________________________________________________________________________________________________


def embed_classement(classement):
    embed = discord.Embed(
        title="🏆 Classement des Pronostics",
        color=EMBED_COLOR_RED
    )
    for i, (pseudo, score) in enumerate(classement, start=1):
        embed.add_field(name=f"{i}ᵉ - {pseudo}",
                        value=f"Score : **{score}**", inline=False)

    embed.set_footer(text=EMBED_FOOTER_TEXT)
    embed.set_image(url=EMBED_IMAGE)
    embed.set_thumbnail(url=EMBED_THUMBNAIL)
    return embed
