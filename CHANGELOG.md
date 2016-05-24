# Changelog #

Tracking changes in CollectionBatchTool between versions. 
See also https://github.com/jmenglund/CollectionBatchTool/releases.

## 0.1.6 ##

* Fixes data type issue in the method `update_database_records`.
* Added support for uploading pick lists (tables picklist and picklistitem)

[View commits](https://github.com/jmenglund/CollectionBatchTool/compare/v0.1.5...v0.1.6)

Released 2016-05-24


## 0.1.5 ##

This release fixes one bug in the method `match_database_records`. Matching duplicate values against values in a database table will no longer result in an error being raised. A warning will be issued instead.

[View commits](https://github.com/jmenglund/CollectionBatchTool/compare/v0.1.4...v0.1.5)


## 0.1.4 ##

This release contains a number of small fixes and enhancements.


### New features ###

* Added support for the following tables: accession, addressofrecord and repositoryagreement
* Added separate function for initiating the database (the configuration file is no longer required)
* Added separate function for applying the Specify context (collection and user)
* Adapted script "export_all_data.py" in docs for calls from the command line

Released 2016-03-14

[View commits](https://github.com/jmenglund/CollectionBatchTool/compare/v0.1.3...v0.1.4)



## 0.1.3 ##

This release was created only to get things working correctly on PyPI.
There should be no substantial changes from the previous release.

[View commits](https://github.com/jmenglund/CollectionBatchTool/compare/v0.1.2...v0.1.3)



## 0.1.2 ##

This release contains a number of small fixes and enhancements.


### New features ###

* Added support for the tables collectingeventattribute and collectionobjectattribute
* Fixed issue with the table collector
* Small documentation updates in a few places

Released 2016-01-04

[View commits](https://github.com/jmenglund/CollectionBatchTool/compare/v0.1.1...v0.1.2)



## 0.1.1 ##

This release contains a number of small fixes and enhancements.


### New features ###

* Added PyPI integration via Travis CI
* Added badges for Tavis CI and PyPI to README.rst
* Small documentation updates in varous places
* Improved organization of the collectionbatchtool module

Released 2015-09-13

[View commits](https://github.com/jmenglund/CollectionBatchTool/compare/v0.1.0...v0.1.1)



## 0.1.0 ##

Initial release

Released 2015-09-09
