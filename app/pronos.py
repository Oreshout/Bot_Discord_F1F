# Gestion des pronostiques, Ã©criture et lecture
import json
import os


def pronos_qualif_logic(id, pseudo, premier: str, second: str, troisieme: str, bt: str):
    file_path = "data/Pronos.json"
    if not os.path.exists(file_path):
        pronos_database = {
            str(id): {
                "Pseudo": pseudo,
                "1": premier,
                "2": second,
                "3": troisieme,
                "Best Lap": bt,
            }
        }
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            pronos_database = json.load(f)
            if str(id) not in pronos_database:
                pronos_database[str(id)] = {
                    "Pseudo": pseudo,
                    "1": premier,
                    "2": second,
                    "3": troisieme,
                    "Best Lap": bt,
                }
            else:
                print("Modif")
                pronos_database[str(id)["Pseudo"]] = pseudo
                pronos_database[str(id)["1"]] = premier
                pronos_database[str(id)["2"]] = second
                pronos_database[str(id)["3"]] = troisieme
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(pronos_database, f, ensure_ascii=False, indent=4)


pronos_qualif_logic(19, "Victor", "Oscar", "Pierre", "Lando", "Lando")
