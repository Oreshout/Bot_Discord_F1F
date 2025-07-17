# Gestion des pronostiques, écriture et lecture
import json
import os
import discord


def pronos(id: int, pseudo: str, premier: str, second: str, troisieme: str, bt: str):
    file_path = '../data/Pronos.json'
    if not os.path.exists(file_path):
        pronos_database = {
            str(id): {
                "Pseudo": pseudo,
                "1": premier,
                "2": second,
                "3": troisieme,
                "Best Lap": bt,
                "Modif":False
            }
        }
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            pronos_database = json.load(f)
            if str(id) not in pronos_database:
                pronos_database[str(id)] = {
                    "Pseudo": pseudo,
                    "1": premier,
                    "2": second,
                    "3": troisieme,
                    "Best Lap": bt,
                    "Modif":False
                }
            else:
                if(pronos_database[str(id)]["Modif"] == True):
                    return False
                else:

                    pronos_database[str(id)]["Pseudo"] = pseudo
                    pronos_database[str(id)]["1"] = premier
                    pronos_database[str(id)]["2"] = second
                    pronos_database[str(id)]["3"] = troisieme
                    pronos_database[str(id)]["Best Lap"] = bt
                    pronos_database[str(id)]["Modif"] = True


    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(pronos_database, f, ensure_ascii=False, indent=4)
    return True

    

    
