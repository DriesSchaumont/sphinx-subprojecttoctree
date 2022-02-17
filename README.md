# Subprojecttoctree
Subprojecttoctrees is a [Sphinx](https://www.sphinx-doc.org) extension that aims
to facilitate the integration of several documentation sources into a single 
[Read the Docs](https://docs.readthedocs.io) webpage. This project extends the 
[Read the Docs subproject](https://docs.readthedocs.io/en/stable/subprojects.html) 
concept, which allows projects to be configured as a subproject of another project, 
by creating a unified sidebar of URLs between these projects. A single 'master' index
is specified in the 'main' project, eliminating the need to update all subprojects 
to change the index and allowing for version-specific sidebar links.

## Documentation
The documentation can be found [here](https://sphinx-subprojecttoctree.readthedocs.io/).

## How to install
Before installing, it is recommended to create a virtual environment first.
Learn more about virtual environments [here](https://docs.python.org/3/tutorial/venv.html).

You can install binairy packages from the 
[Python Package Index (PyPI)](https://pypi.org/project/sphinx-subprojecttoctree/)

```
pip install sphinx-subprojecttoctree
```

More information can be found in the 
[documentation](https://sphinx-subprojecttoctree.readthedocs.io/en/latest/installation.html)

## Dependencies
This project is a plugin for [Sphinx](https://www.sphinx-doc.org).  

## Python version support
Python 3.8, 3.9 and 3.10 are officially supported.

## Running the tests
To run the tests, execute ``tox``.

## License
[MIT](https://github.com/DriesSchaumont/sphinx-subprojecttoctree/blob/main/LICENSE)