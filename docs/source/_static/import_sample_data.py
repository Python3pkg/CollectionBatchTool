#!/usr/bin/env python

"""import_sample_data.py - script for importing sample data"""

from collectionbatchtool import *

apply_user_settings('settings.cfg')  # change to your own config-file!

agt = AgentDataset()
agt.from_csv('agent_sample.csv', quiet=False)
agt.to_database(defaults={'agenttype': 1}, quiet=False)

loc = LocalityDataset()
loc.from_csv('locality_sample.csv', quiet=False)
loc.to_database(defaults={'srclatlongunit': 3}, quiet=False)

cev = CollectingeventDataset()
cev.from_csv('collectingevent_sample.csv', quiet=False)
cev.update_foreign_keys([agt, loc], quiet=False)
cev.to_database(quiet=False)

col = CollectorDataset()
col.from_csv('collector_sample.csv', quiet=False)
col.update_foreign_keys([agt, cev], quiet=False)
col.to_database(defaults={'isprimary': 1}, quiet=False)

cob = CollectionobjectDataset()
cob.from_csv('collectionobject_sample.csv', quiet=False)
cob.update_foreign_keys(cev, quiet=False)
cob.to_database(quiet=False)

pty = PreptypeDataset()
pty.from_csv('preptype_sample.csv', quiet=False)
pty.match_database_records('name')  # match existing preptypes by "name"
pty.to_database(defaults={'isloanable': 1}, quiet=False)

pre = PreparationDataset()
pre.from_csv('preparation_sample.csv', quiet=False)
pre.update_foreign_keys([pty, cob], quiet=False)
pre.to_database(quiet=False)
