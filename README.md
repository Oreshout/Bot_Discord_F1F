<h1 align="center">

![Image](/sprites/banniere_F1F.png)

<h4 align="center">Moderation, Pronostics.</h4>

<p align="center">
  <a href="https://discord.gg/89ENkYSCWE">
    <img src="/sprites/discord-logo.png" alt="Discord Server" width="70" height="45">
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

| 📦 `pip install`         | 💻 Python `import`                                     | 🧠 Main Purpose                                             | 🧩 Category             |
| ------------------------ | ------------------------------------------------------ | ----------------------------------------------------------- | ----------------------- |
| `discord.py`             | `import discord`<br>`from discord.ext import commands` | Manage the Discord interface (messages, events, commands)   | 🟣 Discord Bot          |
| `pandas`                 | `import pandas as pd`                                  | Data analysis and manipulation (tables, CSV, etc.)          | 🔵 Data Processing      |
| `beautifulsoup4`         | `from bs4 import BeautifulSoup`                        | HTML parsing to extract data                                | 🟠 Web Scraping         |
| `selenium`               | `from selenium import webdriver`                       | Browser automation (advanced scraping)                      | 🟠 Web Scraping         |
| `requests`               | `import requests`                                      | HTTP requests to APIs or websites                           | 🟠 Web Scraping         |
| `lxml` *(or `html5lib`)* | *(used by BeautifulSoup)*                              | Fast and robust HTML/XML parser                             | ⚙️ Parsing Dependency   |
| `sphinx`                 | *(not required directly in code)*                      | Automatic documentation generation                          | 🟡 Documentation        |
| `jupyter` *(notebook)*   | *(launched via interface, not imported)*               | Interactive notebooks for testing and code demos            | 🟡 Documentation / Demo |
| `asyncio`                | `import asyncio`                                       | Asynchronous task management                                | 🔴 Async Programming    |
| `typing` *(builtin)*     | `from typing import List, Optional, Dict`              | Static typing and function annotations                      | ⚪ Utility               |
| `os` *(builtin)*         | `import os`                                            | Access to file system / environment variables               | ⚪ Utility               |
| `dotenv` *(optional)*    | `from dotenv import load_dotenv`                       | Load environment variables from a `.env` file               | ⚪ Security / Config     |
| `gitpython` *(optional)* | `import git`                                           | Git integration within the script                           | ⚫ DevOps / Git          |
| `aiohttp` *(optional)*   | `import aiohttp`                                       | Asynchronous HTTP requests (more efficient than `requests`) | 🔴 Async Programming    |
| `schedule` *(optional)*  | `import schedule`                                      | Scheduling tasks at regular intervals                       | 🔁 Scheduled Tasks      |

### How to install all these librairies

```console
pip install -U discord.py pandas beautifulsoup4 selenium requests sphinx notebook python-dotenv
```