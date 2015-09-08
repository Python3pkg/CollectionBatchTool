.. py:currentmodule:: collectionbatchtool

.. _quickstart:

Quickstart
==========

This guide gives you a brief introduction to CollectionBatchTool's
most basic features. The following will be covered:


* :ref:`before-you-begin`
* :ref:`connecting-to-database`
* :ref:`exporting-table-data`
* :ref:`importing-table-data`
* :ref:`updating-data`


.. _before-you-begin:

Before you begin
----------------

A few things need to be in place in order to be able to use 
CollectionBatchTool:

* You need root access to the Specify (MySQL) database you want to work with.
* Your collection must be present in the database. If the collection
  is missing, you have to create it by using *Specify Setup Wizard*. 
* Your Specify user must be available to the collection in question.

.. Warning::
    Using CollectionBatchTool is equivalent to writing SQL-statement against 
    the database as a root user. You are responsible for any changes made to
    the data. In order to avoid concurrency problems, make sure that no one
    else is accessing the database while you are using the tool.


.. _connecting-to-database:

Setting up the database connection
----------------------------------

CollectionBatchTool let you work with one Specify collection at a time.
Enter your personal settings in a configuration file similar to what is shown 
below. Then, save the file with a suitable name, for example 
:file:`settings.cfg`.

.. code-block:: cfg

    [MySQL]
    Database = my_database
    Host = localhost
    User = root
    Password = password

    [Specify]
    CollectionName = My collection
    User = user

To apply your settings, use the function :func:`apply_user_settings`
provided with the path to your configuration file:

.. code-block:: pycon

    >>> from collectionbatchtool import *
    >>> apply_user_settings('settings.cfg')

.. Note::
    It is good practice to always backup your data before you start working
    with a database.


.. _exporting-table-data:

Exporting data from a single table
----------------------------------

In this exercise we will export data from the agent-table in Specify to a 
comma-separated values (CSV) file. We assume that the database connection has 
been set up as described in the previous section. Now, let's begin by first 
creating an :class:`AgentDataset` object:

.. code-block:: pycon

    >>> agt = AgentDataset()

This newly created object will eventually hold all the data we want to export. 
For the moment, it basically contains an empty dataframe stored to the 
:attr:`~TableDataset.frame` attribute. You can verify that the dataframe 
is empty by examining the :class:`AgentDataset` object (see the last line of 
the output):

.. code-block:: pycon

    >>> agt
    <class 'collectionbatchtool.AgentDataset'>
    model: <class 'specifymodels.Agent'>
    key_columns: {
        'agentid': 'agent_sourceid'
        'createdbyagentid': 'createdbyagent_sourceid'
        'modifiedbyagentid': 'modifiedbyagent_sourceid'
        'parentorganizationid': 'parentorganization_sourceid'}
    static_content: {
        'divisionid': 2
        'specifyuserid': None}
    where_clause: <class 'peewee.Expression'>
    frame: <class 'pandas.core.frame.DataFrame'> [0 rows x 30 columns]

You can also look at the :attr:`~TableDataset.frame` attribute directly:

.. code-block:: pycon

    >>> agt.frame
    Empty DataFrame
    Columns: [
        agent_sourceid, createdbyagent_sourceid, modifiedbyagent_sourceid, 
        parentorganization_sourceid, abbreviation, agenttype, dateofbirth, 
        dateofbirthprecision, dateofdeath, dateofdeathprecision, datetype, email, 
        firstname, guid, initials, interests, jobtitle, lastname, middleinitial, 
        remarks, suffix, timestampcreated, timestampmodified, title, url, version, 
        agentid, createdbyagentid, modifiedbyagentid, parentorganizationid]
    Index: []

    [0 rows x 30 columns]

Next, we would like to load data from the agent table into our object's 
:attr:`~TableDataset.frame` attribute. We do so by using the
:meth:`~TableDataset.from_database` method. By setting ``quiet=False`` we will 
get some information on what's going on: 

.. code-block:: pycon

    >>> agt.from_database(quiet=False)
    [AgentDataset] reading database records: 1/1


If there are any agent-records associated with your collection, these should 
now be stored to your :class:`AgentDataset` object. A new collection within 
its own division in Specify contains just a single agent-record (as in our 
example).

Writing the data to a CSV file is just as easy as retrieving the data from the 
database. The method :meth:`~TableDataset.to_csv` and a file path is all 
that is needed:

.. code-block:: pycon

    >>> agt.to_csv('agent.csv', update_sourceid=True, quiet=False)
    [AgentDataset] updating SourceID-columns... 
        copying 'agentid' to 'agent_sourceid' [1 value]
        copying 'createdbyagentid' to 'createdbyagent_sourceid' [0 values]
        copying 'modifiedbyagentid' to 'modifiedbyagent_sourceid' [0 values]
        copying 'parentorganizationid' to 'parentorganization_sourceid' [0 values]
    [AgentDataset] writing to CSV file... 
        1 rows x 26 columns; agent.csv


In the example above, we use the ``update_sourceid`` parameter to ensure that 
every ID-column is copied to its corresponding SourceID-column before the data 
is written to the file.

.. Note::
   Want to export data from some other table? 
   Take a look at :ref:`supported Specify tables <supported-tables>` to see 
   which tables are currently available.


.. _importing-table-data:

Importing data to a single table
--------------------------------

Data import is not so different from data export. One important difference, 
though, is that you first need to prepare CSV files according to some 
specific rules. We don't go into the details here, but if you wish you can read 
about the format specifications in the document on
:ref:`how to prepare CSV files<preparing-csv-files>`.

In this excercise we will import data to the agent-table. Like in the export 
example above, we assume that the database connection has been set up properly. 
We will try to import a small sample dataset (three columns and ten rows) 
listing some of the
`Apostles of Linnaeus <https://en.wikipedia.org/wiki/Apostles_of_Linnaeus>`_.
The first column, *agent_sourceid*, is somewhat special and may be used to 
connect records outside of the Specify database. This column can also be used 
to trace imported data, as we will see towards the end of this exercise. 

.. _sample-data-apostles: 

The sample file :file:`apostles.csv` contains the following records:

.. csv-table::
   :file: ../_static/apostles.csv
   :header-rows: 1

:download:`apostles.csv <../_static/apostles.csv>`

Like with exports, we start out by creating an :class:`AgentDataset` object:

.. code-block:: pycon

    >>> agt = AgentDataset()

To read the data from the CSV file, we use the 
:meth:`~TableDataset.from_csv` method:

.. code-block:: pycon

    >>> agt.from_csv('apostles.csv', quiet=False)
    [AgentDataset] reading CSV file... 
        10 rows x 3 columns; apostles.csv

The :class:`AgentDataset` object should now hold the ten records. We continue 
with uploading the data to the agent-table. The method 
:meth:`~TableDataset.to_database` takes care of the upload for us. We use 
the method's ``defaults`` parameter to insert default values instead of 
``NULL``. This parameter accepts a python :class:`dict` with column names and 
values to insert:

.. code-block:: pycon

    >>> agt_defaults = {
    ...     'agenttype': 1,
    ...     'dateofbirthprecision': 1,
    ...     'dateofdeathprecision': 1,
    ...     'middleinitial': ''
    ... }
    >>> agt.to_database(defaults=agt_defaults, quiet=False)
    [AgentDataset] loading records to database: 10/10


After the import is completed, your :class:`AgentDataset` object will 
automatically get updated with the inserted records' primary key values. If you 
look at the :attr:`~TableDataset.frame` attribute of your :class:`AgentDataset` 
object, you should see a new value in the *agentid*-column for every record 
that was imported to the database.

Now, let's try to upload the dataset again. As you should notice, none of the 
records gets inserted into the database this time. The reason is the new 
values in the *agentid*-column. Only records where the primary key is missing 
will get uploaded to the database.

Finally, we can use the :meth:`~TableDataset.write_mapping_to_csv` method 
to export the mapping between *agent_sourceid* and *agentid*. This mapping 
allow us to trace the source of every imported record.

.. code-block:: pycon

    >>> agt.write_mapping_to_csv('agent-mapping.csv')

.. Important::
   There is no data validation carried out by CollectionBatchTool prior to 
   import. An incorrect datatype, or violation of a database contraint, will 
   result in an error and an exception being raised.

.. _updating-data:

Updating existing database records
----------------------------------

In the last exercise of the quickstart guide, we will try to update some of 
the records that we imported in the :ref:`previously <importing-table-data>`. 
Suppose that we want to update the agent-table with new birthyears for three of 
the apostles that were imported.

The new sample file :file:`apostles_birthyear.csv` contains the following 
information:

.. csv-table::
   :file: ../_static/apostles_birthyear.csv
   :header-rows: 1

:download:`apostles_birthyear.csv <../_static/apostles_birthyear.csv>`

We begin by creating a new :class:`AgentDataset` object and reading the new 
sample data into that object:

.. code-block:: pycon

    >>> agt = AgentDataset()
    >>> agt.from_csv('apostles_birthyear.csv', quiet=False)
    [AgentDataset] reading CSV file... 
        3 rows x 4 columns; apostles_birthyear.csv

Next, we get primary key values from the agent-table based on content in the 
columns *firstname* and *lastname* (we assume here that the combination of first
and last names will uniquely identify individual agent records). We use the 
:meth:`~TableDataset.match_database_records` method:

.. code-block:: pycon

    >>> agt.match_database_records(['firstname', 'lastname'], quiet=False)
    [AgentDataset] updating primary key from database... 
        target-column:   'agentid'
        match-column(s): ['firstname', 'lastname']
        matches:         3/3

You should now be able to see the updated values in the *agentid*-column 
if you check the :attr:`~TableDataset.frame` attribute of your
:class:`AgentDataset` object. 
Once the primary key values are in place, it's easy to update the database 
with information from the two new columns with the 
:meth:`~TableDataset.update_database_records` method:

.. code-block:: pycon

    >>> agt.update_database_records(['dateofbirth', 'dateofbirthprecision'], quiet=False)
    [AgentDataset] updating database records: 3/3


You have now reached the end of the quickstart guide. Wan't to know more? 
Continue to the guide on CollectionBatchTool's 
:ref:`advanced features <advanced-operations>` or read more about functions, 
classes and methods in the :ref:`API reference<api>`.
