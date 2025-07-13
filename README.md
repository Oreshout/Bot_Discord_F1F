<h1 align="center">

![Image](/sprites/banniere_F1F.png)

<h4 align="center">Moderation, Pronostics.</h4>

<p align="center">
  <a href="https://discord.gg/89ENkYSCWE">
    <img src="/sprites/Discord-logo.png" alt="Discord Server" width="70" height="45">
  </a>
 
 <p align="center">
  <a href="#overview">Overview</a>
  •
  <a href="#installation">Installation</a>
  •
  <a href="http://docs.discord.red/en/stable/index.html">Documentation</a>
  •
  <a href="#plugins">Plugins</a>
  •
  <a href="#join-the-community">Community</a>
  •
  <a href="#license">License</a>
</p>


# Overview

The F1F Discord Bot is a collaborative project designed to enhance Formula 1 communities on Discord by offering an interactive and intelligent prediction system. Developed in Python 3.13.5, the bot allows users to submit race predictions, track their performance, and engage with real-time F1 data in a fun and competitive way.

The core of the bot is built using the `discord.py` library, with `pandas` handling data analysis and user statistics. For gathering up-to-date information from F1 websites, the project makes use of web scraping tools such as `BeautifulSoup`, `Selenium`, and `requests`. The documentation and testing process is supported by tools like Sphinx and Jupyter, while Git and GitHub ensure a clean and collaborative development workflow.

This project is particularly suited for beginner developers or anyone interested in learning how Discord bots work—from backend logic to data scraping and community engagement. That said, experienced contributors are also very welcome to help expand the project’s scope. Whether you’re passionate about coding, motorsport, or both, the F1F Bot is an exciting opportunity to grow your skills in a real-world project while having fun with a dynamic team.


# Installation 

| 📦 `pip install`          | 💻 `import` Python                                     | 🧠 Rôle principal                                           | 🧩 Catégorie                |
| ------------------------- | ------------------------------------------------------ | ----------------------------------------------------------- | --------------------------- |
| `discord.py`              | `import discord`<br>`from discord.ext import commands` | Gérer l’interface Discord (messages, événements, commandes) | 🟣 Bot Discord              |
| `pandas`                  | `import pandas as pd`                                  | Analyse et manipulation de données (tableaux, CSV, etc.)    | 🔵 Traitement de données    |
| `beautifulsoup4`          | `from bs4 import BeautifulSoup`                        | Parsing HTML pour extraire des données                      | 🟠 Web scraping             |
| `selenium`                | `from selenium import webdriver`                       | Automatisation de navigateur (scraping avancé)              | 🟠 Web scraping             |
| `requests`                | `import requests`                                      | Requêtes HTTP vers des API ou des sites web                 | 🟠 Web scraping             |
| `lxml` *(ou `html5lib`)*  | *(utilisé par BeautifulSoup)*                          | Parser HTML/XML rapide et robuste                           | ⚙️ Dépendance parsing       |
| `sphinx`                  | *(pas nécessaire dans le code directement)*            | Génération automatique de documentation                     | 🟡 Documentation            |
| `jupyter` *(notebook)*    | *(lancé via interface, pas importé)*                   | Notebooks interactifs pour tester/analyser du code          | 🟡 Documentation / Démo     |
| `asyncio`                 | `import asyncio`                                       | Gestion des tâches asynchrones                              | 🔴 Programmation asynchrone |
| `typing` *(builtin)*      | `from typing import List, Optional, Dict`              | Typage statique et annotations de fonctions                 | ⚪ Utilitaire                |
| `os` *(builtin)*          | `import os`                                            | Accès au système de fichiers / variables d’environnement    | ⚪ Utilitaire                |
| `dotenv` *(optionnel)*    | `from dotenv import load_dotenv`                       | Charger des variables d’environnement (.env)                | ⚪ Sécurité / Config         |
| `gitpython` *(optionnel)* | `import git`                                           | Intégration Git dans le script                              | ⚫ DevOps / Git              |
| `aiohttp` *(optionnel)*   | `import aiohttp`                                       | Requêtes HTTP asynchrones (plus efficace que requests)      | 🔴 Asynchrone               |
| `schedule` *(optionnel)*  | `import schedule`                                      | Planification de tâches à intervalles réguliers             | 🔁 Tâches programmées       |

```console
pip install -U discord.py pandas beautifulsoup4 selenium requests sphinx notebook python-dotenv
```