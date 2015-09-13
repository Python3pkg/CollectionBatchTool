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

Currently only with support for Python 3.

Source repository: `<https://github.com/jmenglund/CollectionBatchTool>`_

Documentation at `<http://collectionbatchtool.readthedocs.org>`_

.. image:: https://badge.fury.io/py/CollectionBatchTool.svg
    :target: http://badge.fury.io/py/CollectionBatchTool

.. image:: https://api.travis-ci.org/jmenglund/CollectionBatchTool.svg?branch=master
  :target: https://travis-ci.org/jmenglund/CollectionBatchTool


Installation
------------

For most users, the easiest way is probably to install the latest version 
hosted on `PyPI <https://pypi.python.org/>`_:

.. code-block:: console

    $ pip install collectionbatchtool

The project is hosted at https://github.com/jmenglund/CollectionBatchTool and 
can also be installed using git:

.. code-block:: console

    $ git clone https://github.com/jmenglund/CollectionBatchTool.git
    $ cd CollectionBatchTool
    $ python setup.py install
