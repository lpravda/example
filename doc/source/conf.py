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
from recommonmark.transform import AutoStructify

# -- Project information -----------------------------------------------------

project = "superposer"
copyright = "2021, Lukas Pravda"
author = "Lukas Pravda"

# The full version, including alpha/beta/rc tags
release = "0.1"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinxcontrib.napoleon",
    "sphinx.ext.todo",
    "sphinx_markdown_tables",
    "sphinx.ext.coverage",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "recommonmark",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "gemmi": ("https://project-gemmi.github.io/python-api/", None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]
pygments_style = "sphinx"
github_doc_root = "https://github.com/rtfd/recommonmark/tree/master/doc/"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_logo = "_static/logo.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]




def setup(app):
    app.add_config_value(
        "recommonmark_config",
        {
            "url_resolver": lambda url: github_doc_root + url,
            "auto_toc_tree_section": "Contents",
        },
        True,
    )
    app.add_transform(AutoStructify)
    app.connect(
        "autodoc-process-docstring",
        no_namedtuple_attrib_docstring,
    )


def no_namedtuple_attrib_docstring(app, what, name, obj, options, lines):
    is_namedtuple_docstring = len(lines) == 1 and lines[0].startswith(
        "Alias for field number"
    )
    if is_namedtuple_docstring:
        # We don't return, so we need to purge in-place
        del lines[:]