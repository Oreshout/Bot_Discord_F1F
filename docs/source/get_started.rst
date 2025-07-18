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

.. list-table:: 📚 Used Python Libraries
   :widths: 20 30 40 20
   :header-rows: 1

   * - 📦 pip install
     - 💻 Python import
     - 🧠 Main Purpose
     - 🧩 Category
   * - `python-dotenv`
     - `from dotenv import load_dotenv`
     - Load environment variables from a `.env` file
     - ⚪ Security / Config
   * - `discord.py`
     - `import discord`  
       `from discord.ext import commands`
     - Manage Discord interactions: messages, events, commands
     - 🟣 Discord Bot
   * - `fastf1`
     - `import fastf1`
     - Access F1 telemetry and session data via API
     - 🔴 F1 Data API
   * - `pandas`
     - `import pandas as pd`
     - Data manipulation and analysis (tables, CSV, etc.)
     - 🔵 Data Processing
   * - `thefuzz`
     - `from thefuzz import fuzz`
     - Fuzzy string matching (text similarity)
     - 🟢 Text Matching
   * - `sphinx`
     - *(not used in Python code directly)*
     - Generate documentation automatically from source code
     - 🟡 Documentation
   * - `sphinx_rtd_theme`
     - *(configured in `conf.py`)*
     - Classic Sphinx theme styled like ReadTheDocs
     - 🎨 Documentation Theme
   * - `myst-parser`
     - *(enabled in `extensions` in `conf.py`)*
     - Add Markdown (.md) support to Sphinx
     - 📝 Markdown Support
   * - `furo`
     - *(configured in `conf.py`)*
     - Clean, modern, responsive Sphinx theme (light/dark mode)
     - 🎨 Documentation Theme

How to install all these librairies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

  pip install -r requirements.txt

Configuration
-------------

Make sure to create a `.env` file with the following structure:

.. code-block:: ini

   DISCORD_TOKEN_F1F = your_token_here

Development Notes
-----------------

To launch the bot locally:

.. code-block:: bash

   source .venv/bin/activate
   python app\_app.py


License
-------

MIT License.  
© Formula 1 France Development Team.
