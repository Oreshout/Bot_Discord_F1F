import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from config import discord, EMBED_COLOR_RED, EMBED_IMAGE, EMBED_THUMBNAIL, EMBED_FOOTER_TEXT, URL_RESULT_COURSE, URL_RESULT_QUALIF, logger

async def scrapping_result_course(interaction: discord.Interaction):
    
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = uc.Chrome(options=options, use_subprocess=True)
    logger.info("Driver has been initialized.")

    driver.get(URL_RESULT_COURSE)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ms-table_row"))
        )
    except TimeoutError:
        logger.info("Aucune ligne de tableau trouvée.")
        driver.quit()
        exit()

    # Parser la page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table_rows = soup.find_all("tr", class_="ms-table_row")

    # Récupérer uniquement les positions et noms
    positions_noms = []

    for row in table_rows[:-3]:
        columns = row.find_all("td")
        if len(columns) >= 2:  # on vérifie qu’il y a bien au moins position + nom
            pos = columns[0].get_text(strip=True)
            raw_name = columns[1].get_text(strip=True)
            for team in ["McLaren", "Stake Sauber", "Ferrari", "Red Bull", "Alpine", "Aston Martin", "Mercedes", "Haas", "Williams", "Racing Bulls"]:
                raw_name = raw_name.replace(team, "")
            name = raw_name.strip()

            positions_noms.append((pos, name))


    driver.quit()

    # Conversion en JSON bien formaté
    json_data = json.dumps(positions_noms, ensure_ascii=False, indent=4)

    # Optionnel : sauvegarder dans un fichier
    with open("../data/resultats_course.json", "w", encoding="utf-8") as f:
        f.write(json_data)
    
    logger.info("Récupération des résultats courses.")
    
    if not positions_noms:
        description = (
            "On dirait que tu as déjà fait un pronostique. "
            "Si tu veux le modifier, utilise la commande `/modify`."
        )
        title = f"Désolé {interaction.user} !"
    else:
        description = "La mise à jour du fichier `.json` est faite."
        title = f"Merci {interaction.user} !"

    embed = discord.Embed(
        title=title,
        description=description,
        color=EMBED_COLOR_RED
    )
    embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_image(url=EMBED_IMAGE)

    return embed  # ✅ On retourne l'embed sans l'envoyer

#_______________________________________________________________________________________________________________

async def scrapping_result_qualif(interaction: discord.Interaction):
    
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = uc.Chrome(options=options, use_subprocess=True)
    logger.info("Driver has been initialized.")

    driver.get(URL_RESULT_QUALIF)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ms-table_row"))
        )
    except TimeoutError:
        logger.info("Aucune ligne de tableau trouvée.")
        driver.quit()
        exit()

    # Parser la page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table_rows = soup.find_all("tr", class_="ms-table_row")

    # Récupérer uniquement les positions et noms
    positions_noms = []

    for row in table_rows[:-3]:
        columns = row.find_all("td")
        if len(columns) >= 2:  # on vérifie qu’il y a bien au moins position + nom
            pos = columns[0].get_text(strip=True)
            raw_name = columns[1].get_text(strip=True)
            for team in ["McLaren", "Stake Sauber", "Ferrari", "Red Bull", "Alpine", "Aston Martin", "Mercedes", "Haas", "Williams", "Racing Bulls"]:
                raw_name = raw_name.replace(team, "")
            name = raw_name.strip()

            positions_noms.append((pos, name))


    driver.quit()

    # Conversion en JSON bien formaté
    json_data = json.dumps(positions_noms, ensure_ascii=False, indent=4)

    # Optionnel : sauvegarder dans un fichier
    with open("../data/resultats_qualif.json", "w", encoding="utf-8") as f:
        f.write(json_data)
    
    logger.info("Récupération des résultats qualif.")
    
    if not positions_noms:
        description = (
            "On dirait que tu as déjà fait un pronostique. "
            "Si tu veux le modifier, utilise la commande `/modify`."
        )
        title = f"Désolé {interaction.user} !"
    else:
        description = "La mise à jour du fichier `.json` est faite."
        title = f"Merci {interaction.user} !"

    embed = discord.Embed(
        title=title,
        description=description,
        color=EMBED_COLOR_RED
    )
    embed.set_footer(text=EMBED_FOOTER_TEXT, icon_url=EMBED_THUMBNAIL)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_image(url=EMBED_IMAGE)

    return embed  # ✅ On retourne l'embed sans l'envoyer
