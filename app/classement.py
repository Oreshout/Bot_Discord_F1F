import json
import os
from thefuzz import fuzz
import discord
from config import logger, EMBED_COLOR_RED, EMBED_THUMBNAIL, EMBED_FOOTER_TEXT, EMBED_IMAGE
import pronos as pr

def load_json_file(path):
    """Charge un fichier JSON, retourne un dict vide si fichier absent ou invalide."""
    if not os.path.exists(path):
        logger.warning(f"Fichier {path} non trouvé, création d'un dict vide.")
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (ValueError, json.JSONDecodeError) as e:
        logger.error(f"Erreur lors du chargement du fichier {path}: {e}")
        return {}

def match_position(entry: str, target: str, threshold: int) -> bool:
    """Compare les noms avec tolérance, utilise fuzzy matching sur prénom ou nom."""
    parts = entry.strip().split(' ', 1)
    if len(parts) == 2:
        prenom, nom = parts
    else:
        prenom = nom = parts[0]

    target_parts = target.strip().split(' ', 1)
    if len(target_parts) != 2:
        logger.warning(f"Format inattendu pour target '{target}'")
        return False
    target_prenom, target_nom = target_parts

    return (fuzz.ratio(target_prenom.lower(), prenom.lower()) >= 90 or
            fuzz.ratio(target_nom.lower(), nom.lower()) >= threshold)

def save_results(race_type):
    """
    race_type doit être une des chaînes : 'Qualif', 'CourseSprint', 'Course'
    """

    logger.info(f"save_results appelée avec race_type = {race_type}")

    country = pr.country_fonction()

    results = load_json_file('data/Results.json')
    pronos = load_json_file(f'data/pronos_{country}.json')
    barem = load_json_file('data/Barem.json')

    if not results or not pronos or not barem:
        logger.info("Fichiers nécessaires absents ou invalides, arrêt de la fonction.")
        return

    if race_type not in barem:
        logger.error(f"Type de course '{race_type}' non supporté dans le barème.")
        return

    bar = barem[race_type]
    premier = results.get('1', '')
    second = results.get('2', '')
    troisieme = results.get('3', '')

    leaderboard_path = 'data/Leaderbord.json'
    leaderboard = load_json_file(leaderboard_path)

    for key, user_pronos in pronos.items():
        points = 0
        pseudo = user_pronos.get('Pseudo', 'Inconnu')

        logger.info(f"Calcul des points pour l'utilisateur {key} ({pseudo})")

        premier_in_top3 = premier in [user_pronos.get('1', ''), user_pronos.get('2', ''), user_pronos.get('3', '')]
        second_in_top3 = second in [user_pronos.get('1', ''), user_pronos.get('2', ''), user_pronos.get('3', '')]
        troisieme_in_top3 = troisieme in [user_pronos.get('1', ''), user_pronos.get('2', ''), user_pronos.get('3', '')]

        premier_correct = match_position(user_pronos.get('1', ''), premier, 90)
        second_correct = match_position(user_pronos.get('2', ''), second, 90)
        troisieme_correct = match_position(user_pronos.get('3', ''), troisieme, 90)

        all_correct = premier_correct and second_correct and troisieme_correct

        if all_correct:
            points += bar.get('allCorrect', 0)
            logger.info(f"Tout juste pour {pseudo}, +{bar.get('allCorrect', 0)} pts")
        else:
            if premier_correct:
                points += bar.get('correctPosition', 0)
                logger.info(f"Premier à la bonne place pour {pseudo}, +{bar.get('correctPosition', 0)} pts")
            elif premier_in_top3:
                points += bar.get('inTop3', 0)
                logger.info(f"Premier dans le top 3 pour {pseudo}, +{bar.get('inTop3', 0)} pts")

            if second_correct:
                points += bar.get('correctPosition', 0)
                logger.info(f"Deuxième à la bonne place pour {pseudo}, +{bar.get('correctPosition', 0)} pts")
            elif second_in_top3:
                points += bar.get('inTop3', 0)
                logger.info(f"Deuxième dans le top 3 pour {pseudo}, +{bar.get('inTop3', 0)} pts")

            if troisieme_correct:
                points += bar.get('correctPosition', 0)
                logger.info(f"Troisième à la bonne place pour {pseudo}, +{bar.get('correctPosition', 0)} pts")
            elif troisieme_in_top3:
                points += bar.get('inTop3', 0)
                logger.info(f"Troisième dans le top 3 pour {pseudo}, +{bar.get('inTop3', 0)} pts")

    if key not in leaderboard:
        leaderboard[key] = {"Pseudo": pseudo, "Points": points}
    else:
        leaderboard[key]["Points"] += points


    try:
        with open(leaderboard_path, 'w', encoding='utf-8') as f:
            json.dump(leaderboard, f, ensure_ascii=False, indent=4)
        logger.info(f"Leaderboard mis à jour avec {len(leaderboard)} utilisateurs.")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde du leaderboard: {e}")
        
        
def Leaderboard():
    try:
        with open("data/Leaderbord.json", 'r', encoding='utf-8') as f:
            pointsPronos = json.load(f)
            pronosLeaderboard = dict(
                sorted(pointsPronos.items(), key=lambda item: item[1]['Points'], reverse=True)
            )
    except FileNotFoundError:
        logger.info("The file doesn't exist")
        return None
    except json.JSONDecodeError:
        logger.info("Le fichier Leaderbord.json est vide ou mal formé")
        return None
    except KeyError:
        logger.info("Erreur dans la lecture des points")
        return None

    if not pronosLeaderboard:
        embed = discord.Embed(
            title="🏆 Classement des Pronostics",
            description="Aucun résultat à afficher pour le moment.",
            color=EMBED_COLOR_RED
        )
        embed.set_footer(text=EMBED_FOOTER_TEXT)
        embed.set_image(url=EMBED_IMAGE)
        embed.set_thumbnail(url=EMBED_THUMBNAIL)
        return embed

    # Extraction sécurisée des pseudos et points
    try:
        pseudos, points = zip(*[(val['Pseudo'], val['Points']) for val in pronosLeaderboard.values()])
    except ValueError:
        logger.info("Erreur lors de l'extraction des pseudos et points.")
        return None

    embed = discord.Embed(
        title="🏆 Classement des Pronostics",
        color=EMBED_COLOR_RED
    )
    position = 1
    for i in range(len(pseudos)):
        embed.add_field(name=f"{position}ᵉ - {pseudos[i]}",
                        value=f"Score : **{points[i]}**", inline=False)
        # Incrément de la position seulement si le prochain score est différent
        if (i + 1 < len(pseudos)) and (points[i] != points[i + 1]):
            position += 1

    embed.set_footer(text=EMBED_FOOTER_TEXT)
    embed.set_image(url=EMBED_IMAGE)
    embed.set_thumbnail(url=EMBED_THUMBNAIL)
    return embed
