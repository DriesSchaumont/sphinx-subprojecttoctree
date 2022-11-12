
Changelog
*********

0.5.3 (in development)
----------------------

0.5.2 (12/11/2022)
------------------
* Next and previous link now work when the sphinx readthedocs extension (readthedocs-sphinx-ext) is installed (which is the case with online builds) (:issue:`57`)

0.5.1 (11/11/2022)
------------------
* Fixed an issue where the HTML builder was not compatible with the builder from readthedocs-sphinx-ext, causing `AttributeError` when building subprojects on readthedocs (:issue:`55`)

0.5.0 (9/11/2022)
-----------------
* Support Sphinx 5.2 and 5.3 (:pr:`43` and :pr:`44`)
* Support sphinx-rtd-theme 1.1.* (:pr:`51`)
* Fix an issue 'next' and 'previous' buttons were not being generated when they link to a subproject or master project (:issue:`45`)

0.4.0 (30/08/2022)
------------------
* Support Sphinx 4.5, 5.0 and 5.1 (:issue:`35`).
* Loosen requests dependency to major verion (:issue:`35`).

0.3.1 (5/05/2022)
-----------------
* When generating a subproject toc, correct links to other subprojects are now generated (:issue:`33`).

0.3.0 (5/05/2022)
-----------------
* Fix the index file of a subproject not being updated when the master projecrt index is changed (:issue:`30`).
* Fix an issue where entries in the master project index are not included when they are listed after a subproject (:issue:`28`).
* Add missing request dependency (:issue:`25`).

0.2.0 (17/02/2022)
------------------
* Fixed an issue where the master toctree entries would be added to all subproject root toctrees (:issue:`12`).
* Do not raise when using a non-html builder (:issue:`14`).
* Subprojecttoctree now raises an error when trying to create nested subprojects (:issue:`18`).

0.1.4 (11/02/2022)
------------------
* Fixed an issue where using explicit toctree entries caused 'toctree contains reference to nonexisting document' (:issue:`10`).

0.1.3 (11/02/2022)
------------------
* Fixed an issue where the master file was being read when building main project (:issue:`7`).

0.1.2 (11/02/2022)
------------------
* Fix FileNotFoundError caused by not removing master document from source file list (:issue:`4`).

0.1.1 (10/02/2022)
------------------
* Fixed an issue where subprojecttoctree tries to delete a non-existent master index file (:issue:`2`).

0.1.0 (10/02/2022)
------------------
* Initial commit
