#!/usr/bin/env python

"""export_all_data.py - script for exporting all available data"""

import os
from collectionbatchtool import *


def export_all_data(output_dir=None, quiet=True):
    """
    Export table data to CSV files.

    Parameters
    ----------
    output_dir : str
        Path to the output directory.
    """
    output_dir = output_dir if output_dir else ''
    for tabledataset_subclass in TableDataset.__subclasses__():
        instance = tabledataset_subclass()
        if instance.database_query.count() > 0:  # no files without data
            instance.from_database(quiet=quiet)
            filename = instance.model.__name__.lower() + '.csv'
            filepath = os.path.join(output_dir, filename)
            instance.to_csv(
                filepath, update_sourceid=True, quiet=quiet)


if __name__ == '__main__':
    apply_user_settings('settings.cfg')  # change to your own config-file!
    export_all_data(quiet=False)  # call the export function
