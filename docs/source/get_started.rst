Get Started
===========

.. image:: docs/_static/banniere_F1F.png
   :alt: F1F Bot Logo
   :align: center
   :width: 500px

Overview
--------

The F1F Bot is built in Python and interacts with the Discord API using `discord.py`.  
It automates tasks such as:

- User predictions (for Formula 1 races)
- Data scraping from race result websites
- Scheduled updates
- Database management
- Interactive commands on Discord

Project Structure
-----------------

.. code-block:: none

  Bot_Discord_F1F/
  ├── .github/
  │   └── workflows/
  │       └── static.yml   
  |
  ├── app/
  |   ├── __pycache__
  |   ├── _app.py
  |   ├── .env
  |   ├── admin_command.py
  |   ├── classement.py
  |   ├── config.py
  |   ├── error_embed.py
  |   ├── f1api.py
  |   ├── pronos.py
  |   ├── tools.py
  |  
  ├── data/
  |   ├── Barem.json
  |   ├── Leaderbord.json
  |   ├── NameBot.json
  |   ├── Pronos.json
  |   ├── Result.json
  |   ├── Session.json
  |
  ├── docs/
  |   ├── _images/
  |   |     └── F1F-logo.png
  |   ├── _sources/
  |   |     └── commands.rst.txt
  |   |     └── get_started.rst.txt
  |   |     └── index.rst.txt
  |   |     └── privacy_policy.rst.txt
  |   |     └── terms_of_service.rst.txt
  |   ├── _statics/
  |   |    └── ...
  |   ├── .doctrees/
  |   |    └── commands.doctree
  |   |    └── environment.pickle
  |   |    └── ... 
  |   ├── html/
  |   |    └── ...
  |   ├── source/
  |   |    └── commands.rst
  |   |    └── conf.py
  |   |    └── get_started.rst
  |   |    └── index.rst
  |   |    └── privacy_policy.rst
  |   |    └── terms_of_service.rst
  |   ├── .buildinfo
  |   ├── .buildinfo.bak
  |   ├── ...
  └── README.md  

Installation
------------

.. code-block:: bash

   git clone https://github.com/Oreshout/Bot_Discord_F1F.git
   cd Bot_Discord_F1F
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

Python Libraries Used in F1F Bot
--------------------------------

.. list-table:: 📚 Librairies utilisées
   :widths: 20 30 40 20
   :header-rows: 1

   * - 📦 pip install
     - 💻 Python import
     - 🧠 Main Purpose
     - 🧩 Category
   * - `python-dotenv`
     - `from dotenv import load_dotenv`
     - Charger des variables d’environnement depuis un fichier `.env`
     - ⚪ Security / Config
   * - `discord.py`
     - `import discord`  
       `from discord.ext import commands`
     - Gérer les messages, événements et commandes Discord
     - 🟣 Discord Bot
   * - `fastf1`
     - `import fastf1`
     - Accès aux données de Formule 1 via API (lap times, telemetry, etc.)
     - 🔴 F1 Data API
   * - `pandas`
     - `import pandas as pd`
     - Manipulation et analyse de données tabulaires (CSV, séries, etc.)
     - 🔵 Data Processing
   * - `thefuzz`
     - `from thefuzz import fuzz`
     - Fuzzy matching (comparaison de similarité textuelle)
     - 🟢 Text Similarity
   * - `sphinx`
     - *(non utilisé dans le code Python)*
     - Génération automatique de documentation
     - 🟡 Documentation
   * - `sphinx_rtd_theme`
     - *(configuré dans `conf.py`)*
     - Thème graphique style *ReadTheDocs* pour Sphinx
     - 🎨 Documentation Theme
   * - `myst-parser`
     - *(activé via `extensions` dans `conf.py`)*
     - Permet d’écrire la documentation Sphinx en Markdown (.md)
     - 📝 Markdown Support
   * - `furo`
     - *(configuré dans `conf.py`)*
     - Thème moderne, sombre/clair responsive pour Sphinx
     - 🎨 Documentation Theme

How to install all these librairies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   pip install -U discord.py pandas beautifulsoup4 selenium requests sphinx notebook python-dotenv

Configuration
-------------

Make sure to create a `.env` file with the following structure:

.. code-block:: ini

   DISCORD_TOKEN=your_token_here
   GUILD_ID=your_discord_guild_id

Modules and Libraries
---------------------

The bot uses the following libraries:

- **discord.py** – for interacting with the Discord API
- **pandas** – for managing tabular data
- **BeautifulSoup / Selenium** – for scraping external websites
- **schedule** – for timed task execution
- **dotenv** – for configuration via environment variables

Development Notes
-----------------

To launch the bot locally:

.. code-block:: bash

   source .venv/bin/activate
   python bot.py

You can add new commands using `discord.ext.commands.Cog`.

License
-------

MIT License.  
© Formula 1 France Development Team.
