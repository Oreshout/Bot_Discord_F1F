import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path('..', 'src').resolve()))
sys.path.insert(0, os.path.abspath(os.path.join('..', 'app')))
sys.path.insert(0, os.path.abspath(os.path.join('..', 'prompt_optimizer_code')))
sys.path.insert(0, os.path.abspath('..'))
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Bot_F1F'
copyright = '2025, Matt'
author = 'Matt'
release = '1.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",        # Pour la doc automatique depuis les docstrings
    "sphinx.ext.napoleon",       # Pour les docstrings Google/Numpy style
    "sphinx.ext.viewcode",
    "myst_parser",
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = []

language = 'French'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']