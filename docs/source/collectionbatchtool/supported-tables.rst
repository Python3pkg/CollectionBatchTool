.. py:currentmodule:: collectionbatchtool

.. _supported-tables:

Supported Specify Tables
========================

This document lists the tables and 
:ref:`TableDataset subclasses<tabledataset-subclasses>` that are currently 
implemented. Only tables with a corresponding TableDataset subclass are 
available for batch operations (i.e. data import and export).


========================= ===============================
Specify Table             TableDataset subclass
========================= ===============================
agent                     AgentDataset
collectingevent           CollectingeventDataset
collectingeventattribute  CollectingeventattributeDataset
collection                ---
collectionobject          CollectionobjectDataset
collectionobjectattribute CollectionobjectattributeDataset
collector                 CollectorDataset
determination             DeterminationDataset
discipline                ---
division                  ---
geography                 GeographyDataset
geographytreedef          ---
geographytreedefitem      GeographytreedefitemDataset
locality                  LocalityDataset
preptype                  PreptypeDataset
preparation               PreparationDataset
specifyuser               ---
storage                   StorageDataset
storagetreedef            ---
storagetreedefitem        StoragetreedefitemDataset
taxon                     TaxonDataset
taxontreedef              ---
taxontreedefitem          TaxontreedefitemDataset
========================= ===============================

