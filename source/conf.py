import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path('..', 'src').resolve()))
sys.path.insert(0, os.path.abspath(os.path.join('..', 'app')))
sys.path.insert(0, os.path.abspath(os.path.join('..', 'prompt_optimizer_code')))
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'Bot_F1F'
copyright = '2025, Matt'
author = 'Matt, Victor'
release = '1.0.3'

# -- General configuration ---------------------------------------------------

html_baseurl = 'https://username.github.io/Bot_Discord_F1F/'

extensions = [
    "sphinx.ext.autodoc",    # doc automatique depuis docstrings
    "sphinx.ext.napoleon",   # support Google/Numpy style docstrings
    "sphinx.ext.viewcode",
    "myst_parser",
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
html_static_path = ['_static']

# Logo et favicon (vérifie que les fichiers existent dans _static)
html_logo = '../build/_static/F1F-logo.png'
html_favicon = '../build/_static/F1F-logo.ico'
html_css_files = [
    'custom.css',
]

locale_dirs = ['/locales']  # Où sont stockées les traductions
gettext_compact = False

language = 'fr'

# -- Options for HTML output -------------------------------------------------

html_theme = 'furo'
