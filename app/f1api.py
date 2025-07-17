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
    session = f1.get_session(data['Saison'], data["Location"], data["Session"])
    if not session.f1_api_support:
        # Rajouter  une erreur sur discord
        logger.info("L'api n'est pas disponible")
        return 2
    session.load()
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
    except ValueError:
        # Aussi rajouter une erreur sur discord
        logger.info("Value are not avalaible yet")
        return 1
    with open('data/Results.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
