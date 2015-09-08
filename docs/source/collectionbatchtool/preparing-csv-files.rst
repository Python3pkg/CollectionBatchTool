.. py:currentmodule:: collectionbatchtool

.. _preparing-csv-files:

Preparing CSV files
===================

One of CollectionBatchTool's underlying principles is that there should be
one specified file format for each database table available for import (see
which tables are available for import in the document on 
:ref:`supported Specify tables <supported-tables>`). An import file
should be in the comma-separated values (CSV) file format, with the first line 
containing column names. The names of the columns should be the same as in the 
corresponding database table, except for names of key-columns (see below). 


SourceID-columns
----------------

The key-columns in import files are collectively referred to as 
*SourceID-columns*. These columns are functionally equivalent to the primary and 
foreign keys in database tables, but will not get imported directly into the 
database. Rather, they will be used for updating foreign key values before the 
data is uploaded. The names of the SourceID-columns resemble those of 
the database's key-fields. Here is what they look like for agent-table data:

.. csv-table::
   :header: "Database key-field", "SourceID-column"

   agentid, agent_sourceid
   createdbyagentid, createdbyagent_sourceid
   modifiedbyagentid, modifiedbyagent_sourceid
   parentorganizationid, parentorganization_sourceid


To see the names of the key-columns, just check the 
:attr:`~TableDataset.key_columns` attribute of your :class:`TableDataset` 
object:

.. code-block:: pycon

   >>> agt = AgentDataset()
   >>> agt.key_columns
   {'agentid': 'agent_sourceid',
    'createdbyagentid': 'createdbyagent_sourceid',
    'modifiedbyagentid': 'modifiedbyagent_sourceid',
    'parentorganizationid': 'parentorganization_sourceid'}

.. Note::
   Don't know how to set up your database connetion? Have a look at the 
   :ref:`quickstart guide <quickstart>`.


Which fields are available?
---------------------------

Which fields that are available for data import (or export) depends on the
version of CollectionBatchTool you are using. You can get a list of available 
column names for the import file by examining at the 
:attr:`~TableDataset.file_columns` attribute of your :class:`TableDataset` 
object. The example below shows the columns available for import to (or export
from) the agent-table. 

.. code-block:: pycon

   >>> agt = AgentDataset()
   >>> agt.file_columns
   ['agent_sourceid',
    'createdbyagent_sourceid',
    'modifiedbyagent_sourceid',
    'parentorganization_sourceid',
    'abbreviation',
    'agenttype',
    'dateofbirth',
    'dateofbirthprecision',
    'dateofdeath',
    'dateofdeathprecision',
    'datetype',
    'email',
    'firstname',
    'guid',
    'initials',
    'interests',
    'jobtitle',
    'lastname',
    'middleinitial',
    'remarks',
    'suffix',
    'timestampcreated',
    'timestampmodified',
    'title',
    'url',
    'version']

