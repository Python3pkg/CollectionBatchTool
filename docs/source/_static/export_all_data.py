#!/usr/bin/env python

"""export_all_data.py - script for exporting all available data"""

import os
import argparse

from collectionbatchtool import *


def export_all_data(config_file, output_dir=None, quiet=True):
    """
    Export table data to CSV files.

    Parameters
    ----------
    output_dir : str
        Path to the output directory.
    """
    apply_user_settings(config_file) 
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
    parser = argparse.ArgumentParser(
        description='A command-line script that exports Specify data.')
    parser.add_argument(
        'config_file', type=argparse.FileType('rU'),
        help='path to a config-file')
    parser.add_argument('output_dir', default='.', nargs='?',
        help='path to output directory')
    parser.add_argument(
        '-v', '--verbose', action='store_true')
    args = parser.parse_args()
 
    if not os.path.isdir(args.output_dir):
        msg = "%d is not valid directory" % args.output_dir
        raise argparse.ArgumentTypeError(msg)
    
    quiet=False if args.verbose else False
 
    export_all_data(
        args.config_file.name, output_dir=args.output_dir, quiet=False)
