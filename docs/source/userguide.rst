User Guide
**********

Quickstart
==========
After installing Subprojecttoctree, the next step is to identify the project you wish 
to be the 'main' project, and one or more 'subprojects'. Then, follow the steps below
to configure your documentation builds

#. Enable the extension for all projects by adding subprojecttoctree 
   to the ``extension`` parameter in the Sphinx configuration (conf.py).
#. Set the ``is_subproject`` and ``readthedocs_url`` values, also in conf.py.
#. Use the ``subprojecttoctree`` directive to replace the regular ``toctree``
   directive in the root document of the main project (index.rst by default).
#. Use the ``subproject:`` tag in the main project to create a link to the subproject.
   The entry format should be formatted like ``title <subproject: subproject-name>``.
#. (for local builds) Set the ``READTHEDOCS_PROJECT`` environment variable,
   and optionally ``READTHEDOCS_LANGUAGE`` or ``READTHEDOCS_VERSION``.
#. (when building online) `Setup <https://docs.readthedocs.io/en/stable/subprojects.html>`_ 
   the main project and subprojects in Read the Docs.

Example
=======
Main project
------------

Main project directory contents::

  docs/
  ├─ build/
  ├─ source/
  │  ├─ index.rst
  │  ├─ foo.rst
  │  ├─ bar.rst
  │  ├─ conf.py

``index.rst``::

  Welcome to the Documentation!

  Contents:

  .. subprojecttoctree::
      foo
      bar
      SubprojectTitle <subproject: lorem>

``conf.py``::

  extensions = ["subprojecttoctree"]
  is_subproject=False
  readthedocs_url="http://example/.org"


Subproject
----------

Lorem subproject directory contents::

  docs/
  ├─ build/
  ├─ source/
  │  ├─ ipsum.rst
  │  ├─ dolor.rst
  │  ├─ index.rst
  │  ├─ conf.py

``index.rst``::

  Welcome to Lorem's Documentation!

  Contents:

  .. toctree::
      ipsum
      dolor


``conf.py``::

  extensions = ["subprojecttoctree"]
  is_subproject=True
  readthedocs_url="http://example/.org"

Sphinx configuration
====================
This Sphinx extension requires you to adjust or set three configuration values, 
which need to be set in the ``conf.py`` file located in the source directory 
of your Sphinx project.

* ``extensions`` (list): This is a Sphinx config value that lists the enabled 
  Sphinx extensions. 
* ``is_subproject`` (bool): A config value specific for this extension to
  indicate if this project is the main project or a subproject.
* ``readthedocs_url`` (str): A Subprojecttoctree config value to 
  specify the url of the **main** project.

Enabling the extension
----------------------
To enable Subprojecttoctree for your documentation builds, the 
`extensions <https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-extensions>`_ 
config value in ``conf.py`` needs to include ``"subprojecttoctree"``.
If you fail to this correctly, you will most likely encounter an error like 
``Unknown directive type "subprojecttoctree"``.

Defining subprojects
--------------------
The ``is_subproject`` configuration value needs to be set to either ``False`` or ``True``.
If ``True``, subprojecttoctree will asume that you are parsing a subproject. In this case,
the index from the main project will be downloaded, and its entries will be added to the toctree
from the index of the subproject as links. If ``False``, entries in the index toctree containing
the tag ``subproject:`` will be replaced by a URL pointing to the subproject 
(see :ref:`subprojecttoctree directive`). 

Specifying the URL of the main project
--------------------------------------
Subprojecttoctree requires ``readthedocs_url`` to be set. It should contain the url of
the main project build. It usually looks something like: ``http://project_name.readthedocs.io``, 
unless you use a customized URL. This URL will be used as a base for building the URLs in the
sidebar.

.. _subprojecttoctree directive:

The subprojecttoctree directive
===============================

Subprojecttoctree add a new directive, called ``subprojecttoctree``. This directive
needs to be used in the *main* project to replace the build-in ``toctree`` directive.
It can be used at other places at well, but there it should behave just like a
regular ``toctree``. When the ``subprojecttoctree`` directive is used in combination 
with the ``subproject`` tag in an explicit toctree entry, the entry will be replaced
with an URL linking to the subproject root index. The link is formatted like 
``{readthedocs_url}/projects/{subproject-name}/{language}/{version}/index.html``.
The ``readthedocs_url`` is read from the configuration, while ``subproject-name``
is the parsed from the toctree entry (part after the ``subproject:`` tag). Finally, the
``language`` and ``version`` parts originate from the ``READTHEDOCS_LANGUAGE`` and 
``READTHEDOCS_VERSION`` environment variables respectively.

.. note::
  Creating nested subprojects is not supported and will cause a documentation build to
  fail. Do not use the ``subproject:`` tag when building a subproject
  (``is_subproject=True``).

Only explicit entries in the ``suprojecttoctree`` directive will be checked
to contain the `subproject:` tag. Explicit entries have a title, and use the
format ``title <target>``. To mark a target to be a subproject, add the 
``subproject:`` tag before the target: ``title <subproject: target>``.
In order for the links created by subprojecttoctree to resolve correctly,
the target should be the ``alias`` that was set when adding as a subproject
in the Read the Docs admin panel (see :ref:`readthedocs online setup`).
Note that the title for the entry will also be used in to set the link
titles in the sidebar of the subprojects.


.. _readthedocs online setup:

Read the Docs Setup (Online builds)
===================================
Each suproject and the main project will need to be 
`imported <https://docs.readthedocs.io/en/stable/intro/import-guide.html>`_ into
Read the Docs. Once you have imported the documentation, navigate to the ``admin``
settings of the project you wish to be the main project, by clicking on the project
name and choosing ``Admin``. Next, navigate to the ``Subprojects`` subsection.
For each subproject, click ``Add subproject`` and add each individual subproject.
Please note that adding subprojects is a Read the Docs feature, and that issues
regarding this feature should be addressed to the team that develops Read the Docs.
More information on how to setup Read the Docs subprojects can be found
`here <https://docs.readthedocs.io/en/stable/subprojects.html>`_.

Local builds
============
When executing online builds on Read the Docs, its sets three environment variables
for you that subprojecttoctree needs.
* ``READTHEDOCS_PROJECT``
* ``READTHEDOCS_LANGUAGE``
* ``READTHEDOCS_VERSION``

Subprojecttoctree uses these variables to format the URLs that link together the different
projects. On local builds however, you need to set at least the ``READTHEDOCS_PROJECT`` variable
yourself before building the documentation. The ``READTHEDOCS_LANGUAGE`` and ``READTHEDOCS_VERSION``
will default to ``en`` and ``latest``. To prevent you from doing this manually, you can add
them to the Make files that are automatically created by ``sphinx-quickstart``.


Creating links between the projects
===================================
To create links between the projects, you can use the 
`Intersphinx <https://docs.readthedocs.io/en/stable/guides/intersphinx.html>`_ extension,
which has native Sphinx support.