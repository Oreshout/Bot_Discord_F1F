import discord
from config import EMBED_COLOR_RED, EMBED_THUMBNAIL, EMBED_FOOTER_TEXT, EMBED_IMAGE


def calculer_classement(resultats, pronostics_df):
    classement = []

    # Convertir JSON en liste de noms dans l'ordre
    resultats_dict = {int(pos): nom for pos, nom in resultats}

    for _, row in pronostics_df.iterrows():
        pseudo = row["Pseudo"]
        score = 0

        for i in range(1, len(resultats_dict) + 1):
            prediction = row.get(f"P{i}")
            vrai_nom = resultats_dict.get(i)

            if prediction and vrai_nom:
                if prediction.strip().lower() == vrai_nom.strip().lower():
                    score += 1  # +1 point pour chaque bonne position

        classement.append((pseudo, score))

    # Trier par score décroissant
    classement.sort(key=lambda x: x[1], reverse=True)

    return classement

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
