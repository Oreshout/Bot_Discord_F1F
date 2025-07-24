import fastf1 as f1
from datetime import datetime, timezone
import pandas as pd
import json
from config import logger


def getNextEvent():
    year = datetime.now(timezone.utc).year
    calendar = f1.get_event_schedule(year)
    time = datetime.now(timezone.utc)
    for row in calendar.itertuples():
        if (pd.isna(row.Session4DateUtc)):
            logger.info("Pas de Date pour la qualif à "+row.Location)
        elif (time > row.Session4Date):
            logger.info(row.Location + " est passé (Qualif)")
        else:
            logger.info("Prochaine Session Qualif à "+row.Location)
            session = {
                "Round": str(row.Index),
                "Country": row.Country,
                "Location": row.Location,
                "Session": 'Q',
                "Date": row.Session4DateUtc.strftime("%d/%m/%Y,%H:%M:%S"),
                "Saison": datetime.now(timezone.utc).year
            }
            with open('data/Session.json', 'w', encoding='utf-8') as f:
                json.dump(session, f, ensure_ascii=False, indent=4)
            break
        if (pd.isna(row.Session5DateUtc)):
            logger.info("Pas de Date pour la course à "+row.Location)
        elif (time > row.Session5Date):
            logger.info(row.Location + " est passé (Course)")
        else:
            logger.info("Prochaine Course à "+row.Location)
            session = {
                "Round": row.Index,
                "Country": row.Country,
                "Location": row.Location,
                "Session": 'R',
                "Date": row.Session5DateUtc.strftime("%d/%m/%Y,%H:%M:%S"),
                "Saison": datetime.now(timezone.utc).year
            }
            with open('data/Session.json', 'w', encoding='utf-8') as f:
                json.dump(session, f, ensure_ascii=False, indent=4)
            break


def getResults():
    with open('data/Session.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    country = data.get('Country', 'unknown').lower()
    session_type = data.get("Session", "").lower()

    session = f1.get_session(data['Saison'], data["Location"], data["Session"])

    if not session.f1_api_support:
        logger.info("L'API FastF1 n'est pas disponible pour cette session.")
        return 2

    try:
        session.load()
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la session : {e}")
        return 3

    if session.results is None or session.results.empty:
        logger.warning("Les résultats ne sont pas encore disponibles.")
        return 1

    try:
        number = session.laps.pick_fastest().DriverNumber
        row = session.results.loc[session.results.DriverNumber == str(number)]
        driver = row.FullName.values[0]

        result = {
            "1": session.results.FullName.iloc[0],
            "2": session.results.FullName.iloc[1],
            "3": session.results.FullName.iloc[2],
            "Best Lap": driver
        }

    except (ValueError, IndexError) as e:
        logger.warning(f"Erreur dans le traitement des résultats : {e}")
        return 1

    if "qualif" in session_type:
        filename = f'data/Results_Qualif_{country}.json'
    else:
        filename = f'data/Results_Course_{country}.json'

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        logger.info(f"Résultats sauvegardés dans {filename}")
        return 0
    except Exception as e:
        logger.error(f"Erreur sauvegarde résultats : {e}")
        return 4
