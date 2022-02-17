Installation
************

Installation using pip
======================
If you have a working python installation, you can install Subprojecttoctree
using ``pip``::

    python3 -m pip install --user --upgrade sphinx-subprojecttoctree

This command will download Subprojecttoctree from the 
`Python Package Index (PyPI) <https://pypi.org/project/sphinx-subprojecttoctree/>`_
and install it for the user executing the commands only.

Installation from source
========================
Download the source code by using::

    git clone git@github.com:DriesSchaumont/sphinx-subprojecttoctree.git
    cd sphinx-subprojecttoctree


Afterward, install Subprojecttoctree from the ``sphinx-subprojecttoctree``
directory (new directory after you clone this repository), by executing::

    cd sphinx-subprojecttoctree
    python3 -m pip install --user --upgrade .

If something goes wrong when using ``pip install``, update pip and try again::

    pip install -U pip
    python3 -m pip install --user --upgrade .
