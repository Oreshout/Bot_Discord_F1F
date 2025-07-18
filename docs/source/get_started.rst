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

   f1f_bot/
   ├── bot.py
   ├── cogs/
   │   ├── predictions.py
   │   └── ...
   ├── utils/
   │   ├── scraping.py
   │   └── ...
   ├── .env
   ├── .venv/
   ├── requirements.txt
   └── README.rst

Installation
------------

.. code-block:: bash

   git clone https://github.com/votre-utilisateur/f1f-bot.git
   cd f1f-bot
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

Python Libraries Used in F1F Bot
--------------------------------

.. list-table:: ________
   :widths: 20 30 40 20
   :header-rows: 1

   * - 📦 pip install
     - 💻 Python import
     - 🧠 Main Purpose
     - 🧩 Category
   * - `discord.py`
     - `import discord`  
       `from discord.ext import commands`
     - Manage the Discord interface (messages, events, commands)
     - 🟣 Discord Bot
   * - `pandas`
     - `import pandas as pd`
     - Data analysis and manipulation (tables, CSV, etc.)
     - 🔵 Data Processing
   * - `beautifulsoup4`
     - `from bs4 import BeautifulSoup`
     - HTML parsing to extract data
     - 🟠 Web Scraping
   * - `selenium`
     - `from selenium import webdriver`
     - Browser automation (advanced scraping)
     - 🟠 Web Scraping
   * - `requests`
     - `import requests`
     - HTTP requests to APIs or websites
     - 🟠 Web Scraping
   * - `lxml` *(or `html5lib`)*
     - *(used by BeautifulSoup)*
     - Fast and robust HTML/XML parser
     - ⚙️ Parsing Dependency
   * - `sphinx`
     - *(not required directly in code)*
     - Automatic documentation generation
     - 🟡 Documentation
   * - `jupyter` *(notebook)*
     - *(launched via interface, not imported)*
     - Interactive notebooks for testing and code demos
     - 🟡 Documentation / Demo
   * - `asyncio`
     - `import asyncio`
     - Asynchronous task management
     - 🔴 Async Programming
   * - `typing` *(builtin)*
     - `from typing import List, Optional, Dict`
     - Static typing and function annotations
     - ⚪ Utility
   * - `os` *(builtin)*
     - `import os`
     - Access to file system / environment variables
     - ⚪ Utility
   * - `dotenv` *(optional)*
     - `from dotenv import load_dotenv`
     - Load environment variables from a `.env` file
     - ⚪ Security / Config
   * - `gitpython` *(optional)*
     - `import git`
     - Git integration within the script
     - ⚫ DevOps / Git
   * - `aiohttp` *(optional)*
     - `import aiohttp`
     - Asynchronous HTTP requests (more efficient than `requests`)
     - 🔴 Async Programming
   * - `schedule` *(optional)*
     - `import schedule`
     - Scheduling tasks at regular intervals
     - 🔁 Scheduled Tasks

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
