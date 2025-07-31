import fastf1 as f1
from datetime import datetime, timezone

year = datetime.now(timezone.utc).year
calendar = f1.get_event_schedule(year)

# Affiche toutes les courses et sessions (dates)
for row in calendar.itertuples():
    print(f"{row.Index} - {row.Location} ({row.Country})")
    print(f"Qualif : {getattr(row, 'Session4DateUtc', 'N/A')}")
    print(f"Course : {getattr(row, 'Session5DateUtc', 'N/A')}")
    print(f"Sprint : {getattr(row, 'Session6DateUtc', 'N/A')}")
    print('-------------------------')