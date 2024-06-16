import os, sys

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Service for analyzing patent activity of Moscow companies'
copyright = '2024, Alexandr Fedorov, Alexandr Vagulich, Alexandr Arefiev, Konstantin Savchenko, Dmitriy Alekseev'
author = 'Alexandr Fedorov, Alexandr Vagulich, Alexandr Arefiev, Konstantin Savchenko, Dmitriy Alekseev'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['autoapi.extension']

autoapi_dirs = ['../../CompanyCategory', '../../PatentLoader', '../../web/src']

templates_path = ['_templates']
exclude_patterns = []

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

sys.path.append(os.path.abspath('../../'))

html_theme = 'alabaster'
html_static_path = ['_static']
