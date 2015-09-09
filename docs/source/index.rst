.. CollectionBatchTool documentation master file, created by
   sphinx-quickstart on Thu Aug 20 13:19:41 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. py:currentmodule:: collectionbatchtool

CollectionBatchTool
===================

CollectionBatchTool is a Python library for importing, exporting, and updating 
batches of collection data in `Specify <http://specifyx.specifysoftware.org>`_. 
The intended audience is advanced users such as data managers, migration 
specialists, and system administrators.

* Built on top of the packages
  `peewee <https://peewee.readthedocs.org>`_ and 
  `pandas <http://pandas.pydata.org>`_
* Fast uploading of large datasets
* Requires no prior knowledge in SQL and little knowledge in Python

.. image:: _static/specify_project_logo.png
   :target: http://specifyx.specifysoftware.org
   :width: 150px
   :alt: Specify


Source repository: `<https://github.com/jmenglund/CollectionBatchTool>`_

**New to CollectionBatchTool?** Here are a few documents to help you get 
started:

* :ref:`Quickstart guide <quickstart>`
  -- covers the most basic stuff and will take you about 10 minutes to 
  go through.
* :ref:`Preparing CSV files <preparing-csv-files>` – explains how to prepare 
  files for data import.
* :ref:`Supported Specify Tables <supported-tables>` – lists the database 
  tables currently supported.

.. important::
   The current version of CollectionBatchTool (|version|) only supports 
   Python 3.

.. toctree::
   :caption: Contents
   :name: mastertoc
   :maxdepth: 2
   :glob:
   
   collectionbatchtool/installation
   collectionbatchtool/quickstart
   collectionbatchtool/advanced-operations
   collectionbatchtool/preparing-csv-files
   collectionbatchtool/supported-tables
   collectionbatchtool/api


Project background
------------------

.. image:: _static/dina-logo-horizontal.png
   :target: http://dina-project.net
   :width: 180px
   :align: right
   :alt: DINA-project

CollectionBatchTool has been developed within the 
`DINA-project <http://dina-project.net>`_ in order to support migration of
large datasets (100,000+ records) to Specify. The tool was first released 
in September 2015.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

