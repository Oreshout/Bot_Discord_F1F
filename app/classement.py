import json
import os
from thefuzz import fuzz
import discord
from config import logger, EMBED_COLOR_RED, EMBED_THUMBNAIL, EMBED_FOOTER_TEXT, EMBED_IMAGE


def saveResults():
    
    try:
        with open('../data/Results.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
        with open('../data/Pronos.json', 'r', encoding='utf-8') as f:
            pronos = json.load(f)

    except ValueError:
        logger.info("Files cannot be accessed, are you sure pronostics exist ?")
        return
    
    try:
        with open('data/Barem.json', 'r', encoding='utf-8') as f:
            barem = json.load(f)
    except ValueError:
        logger.info("Problem with Barem")
        return
    
    Premier = results['1']
    Second = results['2']
    Troisième = results['3']
    
    for key in pronos.keys():
        points = 0
        complex = False
        logger.info(key)
        Premier_Pronos = False
        Second_Pronos = False
        Troisième_Pronos = False

        def match_Position(entry: str, target: str, threshold: int) -> bool:
            parts = entry.strip().split(' ', 1)
            
            if (len(parts) == 2):
                prenom, nom = parts
            else:
                prenom = nom = parts[0]
                
            target_prenom, target_nom = target.strip().split(' ', 1)
            return fuzz.ratio(target_prenom.lower(), prenom.lower()) >= 90 or fuzz.ratio(target_nom.lower(), nom.lower()) >= threshold
        
        Premier_Pronos = match_Position(pronos[key]['1'], Premier, 90)
        Second_Pronos = match_Position(pronos[key]['2'], Second, 90)
        Troisième_Pronos = match_Position(pronos[key]['3'], Troisième, 90)

        try:
            if Premier_Pronos and Second_Pronos and Troisième_Pronos:
                logger.info("Tout juste pour "+pronos[key]["Pseudo"])
                points += barem["allCorrect"]
                complex = True
                
            elif Premier_Pronos and Second_Pronos:
                logger.info("Le premier et le deuxième sont bon pour " +
                            pronos[key]['Pseudo']+" + "+str(barem["first2Correct"])+" Points")
                points += barem["first2Correct"]
                complex = True
                
            elif Second_Pronos and Troisième_Pronos:
                
                logger.info(
                    "Le premier est bon"+pronos[key]['Pseudo']+" + "+str(barem["last2Correct"])+" Points")
                points += barem["last2Correct"]
                complex = True
                
            elif (Troisième_Pronos and Premier_Pronos):
                
                logger.info("Le premier et le dernier sont bons pour " +
                            pronos[key]['Pseudo']+" + "+str(barem["1and3Correct"])+" Points")
                points += barem["1and3Correct"]
                complex = True
                
        except KeyError as e:
            logger.info(str(e) + "is missing")
            pass
        except TypeError as e:
            logger.info(e)
            pass

        try:
            if (Premier_Pronos and not complex):
                logger.info("Le premier est bon pour " +
                            pronos[key]['Pseudo']+" + "+str(barem["firstCorrect"])+" Points")
                points += barem["firstCorrect"]
                
            if (Second_Pronos and not complex):
                logger.info("Le deuxième est bon pour " +
                            pronos[key]['Pseudo']+" + "+str(barem["secondCorrect"])+" Points")
                points += barem["secondCorrect"]
                
            if (Troisième_Pronos and not complex):
                logger.info("Le troisième est bon pour " +
                            pronos[key]['Pseudo']+" + "+str(barem["thirdCorrect"])+" Points")
                points += barem["thirdCorrect"]
                
        except KeyError as e:
            logger.info(str(e) + "is missing")
            return
        
        except TypeError as e:
            logger.info(e)
            return
        
        file_path = 'data/Leaderbord.json'
        
        if not os.path.exists(file_path):
            pointsPronos = {
                key: {
                    "Pseudo": pronos[key]["Pseudo"],
                    "Points": points
                }
            }
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                pointsPronos = json.load(f)
                if key not in pointsPronos:
                    pointsPronos[key] = {
                        "Pseudo": pronos[key]["Pseudo"],
                        "Points": points
                    }
                else:
                    pointsPronos[key]["Pseudo"] = pronos[key]["Pseudo"]
                    pointsPronos[key]["Points"] += points

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(pointsPronos, f, ensure_ascii=False, indent=4)


def Leaderboard():
    
    try:
        with open("data/Leaderbord.json", 'r', encoding='utf-8') as f:
            pointsPronos = json.load(f)
            pronosLeaderboard = dict(
                sorted(pointsPronos.items(), key=lambda item: item[1]['Points'], reverse=True))
            
    except FileNotFoundError:
        logger.info("The file doesn't exist")
        return
    
    except KeyError:
        logger.info("Erreur dans la lecture des points")
        return
    
    embed = discord.Embed(
        title="🏆 Classement des Pronostics",
        color=EMBED_COLOR_RED
    )
    pseudos, points = zip(*[(val['Pseudo'], val['Points'])
                          for val in pronosLeaderboard.values()])
    pseudos = list(pseudos)
    points = list(points)
    position = 1
    for i in range(len(pseudos)):
        embed.add_field(name=f"{position}ᵉ - {pseudos[i]}",
                        value=f"Score : **{points[i]}**", inline=False)
        if (i+1 < len(pseudos) and points[i] != points[i+1]):
            position += 1
    embed.set_footer(text=EMBED_FOOTER_TEXT)
    embed.set_image(url=EMBED_IMAGE)
    embed.set_thumbnail(url=EMBED_THUMBNAIL)
    return embed
