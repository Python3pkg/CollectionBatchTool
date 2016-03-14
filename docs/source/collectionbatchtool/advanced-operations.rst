.. py:currentmodule:: collectionbatchtool

.. _advanced-operations:

Advanced Operations
===================

This document demonstrates some of SpecifyBatchTool's more advanced features. 
The following sections are included:

* :ref:`exporting-from-multiple-tables`
* :ref:`importing-to-multiple-tables`
* :ref:`counting-database-records`

It is assumed here that you are familiar with the basic operations described
in the :ref:`quickstart guide <quickstart>`. Before you run any of the code
in this document, you should initiate your database as described in the section
:ref:`Setting up the database connection <connecting-to-database>` in the 
quickstart guide.


.. _exporting-from-multiple-tables:

Exporting data from multiple tables
-----------------------------------

Exporting data from multiple tables is easy as exporting data from a single 
table. Just use the :meth:`~TableDataset.from_database` and 
:meth:`~TableDataset.to_csv` methods. Remember to always set 
``update_sourceid=True`` in the :meth:`~TableDataset.to_csv` method to ensure 
that individual records can be connected also after they have been exported. 
Here is an example of how you export data from the locality- and 
geography-tables.

.. code-block:: pycon

    >>> loc = LocalitytDataset()
    >>> loc.from_database()
    >>> loc.to_csv(update_sourceid=True)
    >>> geo = GeographyDataset()
    >>> geo.from_database()
    >>> geo.to_csv(update_sourceid=True)


To export all the data available to CollectionBatchTool, we can write a 
simple script:


.. literalinclude:: ../_static/export_all_data.py
    :language: python

:download:`export_all_data.py <../_static/export_all_data.py>`


.. _importing-to-multiple-tables:

Importing data to multiple tables
---------------------------------

Importing data to multiple tables in Specify is a lot more complicated than 
doing single table imports. The major reason is that foreign keys need to be 
updated before the batches of data can be loaded to the database. Another 
reason is that presence of self-relations in some tables (e.g. agent and taxon) 
may require extra updates to the database after the records have been 
uploaded.

Loading batches of data is faster than updating existing database records. 
Therefore, you can speed up imports by minimizing the number of records being 
updated. This can be done by importing data to tables in a preferable order. 
For example, it is usually good to start with the agent-table, since many 
other tables refer to that.

Due to contraints in the database, you are sometimes also required to create 
records in a certain order. For example, every record uploaded to the 
preparation-table must refer to an existing record in the 
collectionobject-table.

.. Tip::
   When building import scripts it is often a good idea to start with a single 
   table, and then add other tables one at a time after doing some testing. 
   You can save a dump of your database before you begin, and then have that 
   dump restored prior to every new import trial.

For demonstration purpose, data will be uploaded to the following tables:

* agent
* locality
* collectingevent
* collector
* collectionobject
* preparationtype
* preparation

We will use some fabricated data, that in short look like this (you may 
recognize the agent names from the 
:ref:`import exercise <importing-table-data>` in the quickstart guide):

.. csv-table::
   :file: ../_static/sample_data_summary.csv
   :header-rows: 1

Download a zipped archive with the data: :download:`sample_data.zip <../_static/sample_data.zip>`

The following files are included in the archive:

.. csv-table::
   :header: "Filename", "Specify table", "# rows", "# columns"

   agent_sample.csv, agent, 5, 3
   locality_sample.csv, locality, 5, 2
   collectingevent_sample.csv, collectingevent, 5, 2
   collector_sample.csv, collector, 5, 4
   collectionobject_sample.csv, collectionobject, 10, 3
   preptype_sample.csv, preptype, 1, 2
   preparation_sample.csv, preparation, 10, 3


The script for importing the sample data is shown below. Note that we add 
default values to fields that cannot be set to ``NULL``.

.. literalinclude:: ../_static/import_sample_data.py
    :language: python

:download:`import_sample_data.py <../_static/import_sample_data.py>`
    

.. _counting-database-records:

Counting database records
-------------------------

You can easily count how many records there are in the database that 
belong to your collection. The code below counts the records in the 
agent-table, without the need of downloading them:

.. code-block:: pycon

    >>> agt = AgentDataset()
    >>> agt.database_query.count()
    1

To display the number of records for each available table, you can do 
something like this:

.. code-block:: pycon

    >>> for tabledataset_subclass in TableDataset.__subclasses__():
    ...     instance = tabledataset_subclass() 
    ...     print('{0}: {1}'.format(
    ...          instance.model.__name__, instance.database_query.count()))


.. _record-metadata:


