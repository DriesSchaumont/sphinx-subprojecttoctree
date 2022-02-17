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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import os
from pkg_resources import get_distribution

# -- Project information -----------------------------------------------------

project = "Subprojecttoctree"
copyright = "2022, Dries Schaumont"
author = "Dries Schaumont"


# The full version, including alpha/beta/rc tags

release = get_distribution("sphinx-subprojecttoctree").version
if os.environ.get("READTHEDOCS") == "True":
    version = ".".join(release.split(".")[:2])
else:
    version = release

release = version
# -- General configuration ---------------------------------------------------

# The suffix of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx_issues"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


issues_uri = "https://github.com/DriesSchaumont/sphinx-subprojecttoctree/issues/{issue}"
issues_pr_uri = "https://github.com/DriesSchaumont/sphinx-subprojecttoctree/pull/{pr}"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []
