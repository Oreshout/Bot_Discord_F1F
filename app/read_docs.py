import pandas as pd
import json
from config import logger, discord


def read_the_docs(interaction: discord.Interaction, file_path: str):

    try:
        if file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
            logger.info(
                f"[{interaction.user}] Lecture du fichier Excel réussie : {file_path}")
            return df

        elif file_path.endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info(
                f"[{interaction.user}] Lecture du fichier JSON réussie : {file_path}")
            return data

        else:
            logger.warning(
                f"[{interaction.user}] Format de fichier non pris en charge : {file_path}")
            return None

    except Exception as e:
        logger.error(
            f"[{interaction.user}] Erreur lors de la lecture du fichier {file_path} : {e}")
        return None
