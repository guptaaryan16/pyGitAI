# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../../"))


# -- Project information -----------------------------------------------------

project = "pyGitAI"
copyright = "2024, Aryan Gupta"
author = "Aryan Gupta"

# The full version, including alpha/beta/rc tags
release = "v0.1.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.githubpages",
    "sphinx.ext.autodoc",
    "sphinx_inline_tabs",
    "sphinx.ext.intersphinx",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_theme_options = {
    "light_logo": "pygitai-logo-light.png",
    "dark_logo": "pygitai-logo-dark.png",
    "announcement": """<em>Important</em> announcement!
    We are really excited to announce the alpha(pre-release) version of the CLI app. 
    """,
    "source_repository": "https://github.com/guptaaryan16/pygitai/",
    "source_branch": "main",
    "source_directory": "docs/",
}


extensions.append("sphinx.ext.todo")
extensions.append("sphinx.ext.autosummary")
extensions.append("sphinx.ext.intersphinx")
extensions.append("sphinx.ext.mathjax")
extensions.append("sphinx.ext.viewcode")
extensions.append("sphinx.ext.graphviz")


autosummary_generate = True


# -- Extension configuration -------------------------------------------------
