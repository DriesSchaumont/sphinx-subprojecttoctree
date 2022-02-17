
Changelog
*********

0.2.1 (in development)
----------------------

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
