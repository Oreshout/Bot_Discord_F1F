import fastf1 as f1
from datetime import datetime, timezone
import pandas as pd
import json
from config import logger
from pronos import country_fonction, get_session_name
import os

os.makedirs('cache_fastf1', exist_ok=True)
f1.Cache.enable_cache('cache_fastf1')

def getNextEvent():
    year = datetime.now(timezone.utc).year
    calendar = f1.get_event_schedule(year)
    now = datetime.now(timezone.utc)
    
    print("Colonnes du calendrier :", calendar.columns)  # print des colonnes pour vérifier

    for row in calendar.itertuples():
        round_number = row.Index
        country = row.Country
        location = row.Location

        # On parcourt toutes les sessions et on cherche leur nom pour savoir laquelle est le sprint, qualif, etc.
        sessions = []
        for i in range(1, 6):  # Session1 à Session5
            session_name = getattr(row, f'Session{i}', None)
            session_date = getattr(row, f'Session{i}DateUtc', None)

            if session_name is None or session_date is None:
                continue

            # On associe les codes aux noms des sessions
            code = None
            if "Race" in session_name:
                code = "R"
            elif "Sprint" in session_name:
                code = "S"
            elif "Qualifying" in session_name:
                code = "Q"
            elif "Practice" in session_name:
                code = "P"

            if code:
                sessions.append((code, session_date))

        for session_code, session_date in sessions:
            if pd.isna(session_date):
                logger.info(f"[{country}] Pas de date pour la session '{session_code}'")
                continue

            # ✅ Correction ici : forcer la timezone si manquante
            if session_date.tzinfo is None:
                session_date = session_date.replace(tzinfo=timezone.utc)

            if now > session_date:
                logger.info(f"[{country}] Session '{session_code}' déjà passée")
                continue

            session_data = {
                "Round": round_number,
                "Country": country,
                "Location": location,
                "Session": session_code,
                "Date": session_date.strftime("%d/%m/%Y,%H:%M:%S"),
                "Saison": year
            }

            os.makedirs('data', exist_ok=True)
            with open('data/Session.json', 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=4)

            logger.info(f"[{country}] Prochaine session trouvée : {session_code} à {location}")
            return

    logger.warning("Aucune session future trouvée dans le calendrier.")
    
def getResults():
    
    country = country_fonction()
    session_name = get_session_name()
    with open(f'data/Session_{country}_{session_name}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    country = data.get('Country', 'unknown').lower()
    session_type = data.get("Session", "")  # garder la casse

    try:
        session = f1.get_session(data['Saison'], data["Round"], session_type)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la session : {e}")
        return 5

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

    if len(session.results) < 3:
        logger.warning("Pas assez de résultats pour un top 3.")
        return 1

    try:
        number = session.laps.pick_fastest().DriverNumber
        row = session.results[session.results.DriverNumber == str(number)]
        driver = row.FullName.values[0] if not row.empty else "Inconnu"

        result = {
            "1": session.results.FullName.iloc[0],
            "2": session.results.FullName.iloc[1],
            "3": session.results.FullName.iloc[2],
            "Best Lap": driver,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.warning(f"Erreur dans le traitement des résultats : {e}")
        return 1

    if session_type == "Q":
        filename = f'data/Results_Qualif_{country}.json'
    elif session_type == "S":
        filename = f'data/Results_Sprint_{country}.json'
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
