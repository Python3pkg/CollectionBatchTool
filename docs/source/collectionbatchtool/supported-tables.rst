.. py:currentmodule:: collectionbatchtool

.. _supported-tables:

Supported Specify Tables
========================

This document lists the tables and 
:ref:`TableDataset subclasses<tabledataset-subclasses>` that are currently 
implemented. Only tables with a corresponding TableDataset subclass are 
available for batch operations (i.e. data import and export).


========================= ================================ ==============
Specify table             TableDataset subclass            Version added
========================= ================================ ==============
accession                 AccessionDataset                 0.1.4
addressofrecord           AddressofrecordDataset           0.1.4
agent                     AgentDataset
collectingevent           CollectingeventDataset
collectingeventattribute  CollectingeventattributeDataset  0.1.2
collection                ---
collectionobject          CollectionobjectDataset
collectionobjectattribute CollectionobjectattributeDataset 0.1.2
collector                 CollectorDataset
determination             DeterminationDataset
discipline                ---
division                  ---
geography                 GeographyDataset
geographytreedef          ---
geographytreedefitem      GeographytreedefitemDataset
locality                  LocalityDataset
picklist                  PicklistDataset                  0.1.6
picklistitem              PicklistitemDataset              0.1.6
preptype                  PreptypeDataset
preparation               PreparationDataset
repositoryagreement       RepositoryagreementDataset       0.1.4
specifyuser               ---
storage                   StorageDataset
storagetreedef            ---
storagetreedefitem        StoragetreedefitemDataset
taxon                     TaxonDataset
taxontreedef              ---
taxontreedefitem          TaxontreedefitemDataset
========================= ================================ ==============
