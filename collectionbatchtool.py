#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""collectionbatchtool module"""

from __future__ import print_function
from __future__ import unicode_literals
import datetime
import os
import sys
from configparser import SafeConfigParser
import warnings
import pandas
import specifymodels
from numpy import nan


__authors__ = "Markus Englund"
__license__ = "MIT"
__version__ = '0.1.5'


# For Python 2 and 3 compatibility
try:
    basestring
except NameError:
    basestring = str

warnings.simplefilter('always', UserWarning)


def _bold(msg):
    """Make text bold."""
    return (u'\033[1m{0}\033[0m'.format(msg))


def _chunker(seq, chunksize):
    """Iterate over chunks of a sequence object."""
    return (seq[pos:pos + chunksize] for pos in range(0, len(seq), chunksize))


def _get_collection_context(database, collection_name):
    """
    Return a dict with Specify IDs associated
    with a specific collection.

    Parameters
    ----------
    database : :class:`peewee.MySQLDatabase`
    collection_name : str
    quiet : bool, default True
        If True, no output will be written to standard output.

    Returns
    -------
    dict
        institutionid, divisionid, disciplineid, collectionid,
        geographytreedefid, storagetreedefid, taxontreedefid.
    """
    try:
        database.connect()
    except:
        print('The database was not properly initialized.')
        raise
    try:
        collection = specifymodels.Collection.get(
            specifymodels.Collection.collectionname == collection_name)
        discipline = collection.disciplineid
        division = discipline.divisionid
        institution = division.institutionid
        collection_context = {
            'institutionid': institution.institutionid,
            'divisionid': division.divisionid,
            'disciplineid': discipline.disciplineid,
            'collectionid': collection.collectionid,
            'storagetreedefid': institution.storagetreedefid.storagetreedefid,
            'geographytreedefid':
                discipline.geographytreedefid.geographytreedefid,
            'taxontreedefid': discipline.taxontreedefid.taxontreedefid}
        return collection_context
    except specifymodels.Collection.DoesNotExist:
        print(
            'Could not find collection "{0}" in database.'
            .format(collection_name))
        raise
    finally:
        database.close()


def _get_invalid_items(items, valid_items, ignore_case=True):
    """
    Compare list of items against list of valid items.

    Parameters
    ----------
    items : List[str]
        List of items to compare agains `valid_items`.
    valid_items : List[str]
        List of valid items.
    ignore_case : bool, default True
        If True, matching will be case-insensitive.

    Returns
    -------
    List[str] or None
        Subset of `items` not in `valid_items` or None if all items
        are valid.
    """
    if ignore_case:
        items = list(map(str.lower, items))
        valid_items = list(map(str.lower, valid_items))
    if set(items).issubset(set(valid_items)):
        invalid_items = None
    else:
        invalid_items = list(set(items).difference(set(valid_items)))
    return invalid_items


def _get_noun_form(singular, plural, cnt):
    """Return the correct noun-form (plural or singular)."""
    return singular if cnt == 1 else plural


def _get_records(frame, timestamp_fields=None, static_content=None):
    """
    Yield the rows in a :class:`<pandas.DataFrame>`_ as a dict and
    optionally add timestamps and static content.

    Parameters
    ----------
    frame : :class:`pandas.DataFrame`
    timestamp_fields : list, default None
        Names of timestamp-fields to be populated.
    static_content : dict, default None
        Static data to add to the records.

    Yields
    ------
    dict
    """
    timestamp_fields = timestamp_fields if timestamp_fields else []
    static_content = static_content if static_content else {}
    for record in frame.to_dict('records'):
        if timestamp_fields:
            now_timestamp = datetime.datetime.now()  # same timestamp for
            for field in timestamp_fields:           # all timestamp-fields
                record[field] = now_timestamp        # within a record
        record.update(static_content)
        yield record


def _get_user_agentid(database, divisionid, specify_username):
    """
    Get the AgentID within a division for a Specify user.

    Parameters
    ----------
    database : :class:`peewee.MySQLDatabase`
    divisionid : int
    specify_username : str

    Returns
    -------
    int
        AgentID for the Specify user.
    """
    try:
        database.connect()
    except:
        print('The database was not properly initialized.')
        raise
    try:
        user_agent = (
            specifymodels.Agent.select(specifymodels.Agent)
            .join(specifymodels.Specifyuser)
            .where(
                (specifymodels.Specifyuser.name == specify_username) &
                (specifymodels.Agent.divisionid == divisionid)).get())
        return user_agent.agentid
    except specifymodels.Specifyuser.DoesNotExist:
        print(
            'Could not find Specify user "{0}" in database'
            .format(specify_username))
        raise
    finally:
        database.close()


def _insert_defaults(frame, defaults):
    """
    Return a :class:`pandas.DataFrame` with NaN-values replaced with
    defaults.

    Parameters
    ----------
    frame : :class:`pandas.DataFrame`
        Contains the data to be changed.
    defaults : dict
        Column name and value to insert.
    """
    for column in defaults:
        frame[column] = (frame[column].where(
            frame[column].notnull(), other=defaults[column]))
    return frame


def _pretty_dict(d, sort=True):
    """Pretty-formatting for a one-level :class:`<dict>`."""
    dict_string = '{\n'
    for (key, value) in (sorted(d.items()) if sort else d.iteritems()):
        dict_string += '    ' + repr(key) + ': ' + repr(value) + '\n'
    dict_string = dict_string.rstrip('\n') + '}'
    return dict_string


def _print_process_status(msg, current_record, total_records):
    """Print information about the record being processed."""
    current_record_string = (
        '{0}/{1}\r'
        .format(current_record, total_records)
        .rjust(2*len(str(total_records))+2, ' '))
    print(msg, current_record_string, end='')
    sys.stdout.flush()


def _validate_column_names(columns, valid_columns):
    """
    Validate list of column names.

    columns : List[str]
        List of columns to compare agains `valid_columns`.
    valid_columns : List[str]
        List of valid columns.

    Raises
    ------
    KeyError
        If any name in `columns` is not in `valid_columns`.
    """
    invalid_columns = _get_invalid_items(
        items=columns, valid_items=valid_columns, ignore_case=True)
    if invalid_columns:
        print('Invalid columns:')
        print(invalid_columns)
        raise KeyError(
            'Could not set "frame" due to invalid column name(s).')

def apply_specify_context(collection_name, specify_user, quiet=True):
    """
    Set up the Specify context.
    
    Parameters
    ----------
    collection_name : str
        Name of an existing Specify collection.
    specify_user : str
        Username for an existing Specify user.
    quiet : bool, default True
        If True, no output will be written to standard output.

    """
    if not quiet:
        print(_bold('applying Specify context: '))
    database = specifymodels.database
    collection_context = _get_collection_context(
        database=database, collection_name=collection_name)
    user_agentid = _get_user_agentid(
        database=database, divisionid=collection_context['divisionid'],
        specify_username=specify_user)
    specify_context = {'database': database, 'user_agentid': user_agentid}
    specify_context.update(collection_context)
    TableDataset.specify_context = specify_context
    if not quiet:
        print(
            '    collection:    {0}\n'
            '    Specify user:  {1}'
            .format(repr(collection_name), repr(specify_user)))


def apply_user_settings(filepath, quiet=True):
    """
    Read and apply user settings in a configuration file.

    Parameters
    ----------
    filepath : str
        Path to the configuration file.
    quiet : bool, default True
        If True, no output will be written to standard output.
    """
    # database = specifymodels.database
    if not quiet:
        print(_bold('reading config-file: '), end='')
    if not os.path.isfile(filepath):
        raise OSError('Invalid configuration file... ' + filepath)
    else:
        # Read config file
        config_parser = SafeConfigParser()
        config_parser.read(filepath)
        db_name = config_parser.get('MySQL', 'Database')
        db_host = config_parser.get('MySQL', 'Host')
        db_user = config_parser.get('MySQL', 'User')
        db_password = config_parser.get('MySQL', 'Password')
        collection = config_parser.get('Specify', 'CollectionName')
        specify_username = config_parser.get('Specify', 'User')  
        if not quiet:
            print(os.path.abspath(filepath))
        initiate_database(db_name, db_host, db_user, db_password, quiet=quiet)
        database = specifymodels.database
        apply_specify_context(collection, specify_username, quiet=quiet)


def initiate_database(database, host, user, passwd, quiet=True):
    """
    Initiate the database.
    
    Parameters
    ----------
    database : str
        Name of a MySQL database.
    host : str
        Database host.
    user : str
        MySQL user name.
    passwd : str
        MySQL password.
    quiet : bool, default True
        If True, no output will be written to standard output.
    """
    if not quiet:
        print(_bold('initiates database: '))
    specifymodels.database.init(
        database=database, host=host, user=user, passwd=passwd)
    if not quiet:
        print(
            '    database name: {0}\n'
            '    database host: {1}'
            .format(repr(database), repr(host)))


def query_to_dataframe(database, query):
    """
    Return result from a peewee :class:`SelectQuery` as a
    :class:`pandas.DataFrame`."""
    database.connect()
    db_frame = pandas.DataFrame(query.dicts().iterator())
    database.close()
    return db_frame.fillna(value=nan)


class TableDataset(object):
    """
    Store a dataset corresponding to a database table.

    Attributes
    ----------
    model : :class:`peewee.BaseModel`
        A Specify data model corresponding to a table.
    key_columns : dict
        Key-fields and SourceID-columns for the `model`.
    static_content : dict
        Data to automatically inserted for the `model`.
    where_clause : :class:`peewee.Expression`
        Condition for getting relevant data from the database.
    """

    def __init__(
            self, model, key_columns, static_content, where_clause, frame):
        self.model = model
        self.key_columns = key_columns
        self.static_content = static_content
        self.where_clause = where_clause
        self.frame = frame

    @property
    def database_columns(self):
        """List with available database columns."""
        return list(self.model._meta.fields.keys())

    @property
    def all_columns(self):
        """List containing all columns in the dataset."""
        all_columns = (
            sorted(self.key_columns.values()) +
            sorted(self.database_columns))
        return all_columns

    @property
    def file_columns(self):
        """List containing only the columns that can be
        written to or read from a file."""
        to_exclude = (
            list(self.key_columns.keys()) +
            list(self.static_content.keys()))
        file_columns = [
            column for column in self.all_columns
            if column not in to_exclude]
        return file_columns

    @property
    def primary_key_column(self):
        """Name of the primary key column."""
        return self.model._meta.primary_key.name

    @property
    def frame(self):
        """A :class:`pandas.DataFrame` to hold the data."""
        return self.__frame

    @property
    def foreign_key_columns(self):
        foreign_key_columns = {}
        for key_column in self.key_columns.keys():
            if not getattr(self.model, key_column).primary_key:
                rel_model = getattr(self.model, key_column).rel_model
                foreign_key_columns[rel_model] = (
                    foreign_key_columns.get(rel_model, []))
                foreign_key_columns[rel_model].append(key_column)
        return foreign_key_columns

    @property
    def database_query(self):
        """Database query for reading the data from the database."""
        if isinstance(self, CollectorDataset):
            q = (
                self.model.select()
                .join(specifymodels.Collectingevent)
                .where(self.where_clause))
        else:
            q = self.model.select().where(self.where_clause)
        return q

    @frame.setter
    def frame(self, frame):
        expected_columns = (
            self.file_columns + sorted(self.key_columns.keys()))
        if not isinstance(frame, pandas.DataFrame):
            raise TypeError('"frame" must be a :class:`pandas.DataFrame`')
        _validate_column_names(frame.columns, expected_columns)
        self.__frame = pandas.DataFrame(
            frame, columns=expected_columns)

    def __repr__(self):
        key_columns_repr = _pretty_dict(self.key_columns)
        static_content_repr = _pretty_dict(self.static_content)
        description = (
             '{0}\n'
             'model: {1}\n'
             'key_columns: {2}\n'
             'static_content: {3}\n'
             'where_clause: {4}\n'
             'frame: {5} [{6} rows x {7} columns]'
             .format(
                 self.__class__, self.model, key_columns_repr,
                 static_content_repr, type(self.where_clause),
                 type(self.frame), self.frame.shape[0],
                 self.frame.shape[1]))
        return description

    def _get_next_insert_id(self):
        """Get next autoincrement value."""
        database = self.specify_context['database']
        table_name = self.model._meta.name
        database.connect()
        sql_query = (
            "SELECT auto_increment FROM information_schema.tables "
            "WHERE table_name = '{0}' AND table_schema = '{1}';"
            .format(table_name, database.database))
        return database.execute_sql(sql_query).fetchone()[0]
        database.close()

    def _get_update_query(self, record):
        """Return a peewee :class:`SelectQuery` for updating a record."""
        primary_key_field = getattr(self.model, self.primary_key_column)
        primary_key_value = record[self.primary_key_column]
        del record[self.primary_key_column]
        update_query = (
            self.model.update(**record)
            .where(primary_key_field == primary_key_value))
        return update_query

    def describe_columns(self):
        """
        Return a :class:`pandas.DataFrame` describing the columns
        in the current model.
        """
        database = self.specify_context['database']
        frame = pandas.DataFrame(
            database.get_columns(self.model._meta.name),
            columns=[
                'column_name', 'data_type', 'null', 'primary_key', 'table'])
        frame['database_column'] = (
            frame.column_name.str.lower().isin(self.database_columns))
        frame['file_column'] = (
            frame.column_name.str.lower().isin(self.file_columns))
        foreign_key_frame = pandas.DataFrame(
            database.get_foreign_keys(self.model._meta.name),
            columns=[
                'column_name', 'fk_dest_table', 'fk_dest_column', 'table'])
        foreign_key_frame['foreign_key'] = True
        frame = frame.merge(
            foreign_key_frame, how='left', on=['table', 'column_name'])
        frame['foreign_key'].fillna(False, inplace=True)
        sourceid_frame = pandas.DataFrame(
            pandas.Series(self.key_columns), columns=['sourceid_column'])
        frame['column_name_lower'] = frame['column_name'].str.lower()
        frame = frame.merge(
            sourceid_frame, how='left', left_on='column_name_lower',
            right_index=True)
        static_content_frame = pandas.DataFrame(
            pandas.Series(self.static_content), columns=['static_content'])
        frame = frame.merge(
            static_content_frame, how='left', left_on='column_name_lower',
            right_index=True)
        columns = [
            'table', 'column_name', 'data_type', 'null', 'primary_key',
            'foreign_key', 'fk_dest_table', 'fk_dest_column',
            'database_column', 'file_column', 'sourceid_column',
            'static_content']
        return frame[columns]

    def from_csv(self, filepath, quiet=True, **kwargs):
        """Read dataset from a CSV file.

        Parameters
        ----------
        filepath : str
            File path or object.
        quiet : bool, default True
            If True, no output will be written to standard output.
        \**kwargs
            Arbitrary keyword arguments available in
            :func:`pandas.read_csv`.
        """
        if not quiet:
            print(
                _bold('[{0}] reading CSV file: ')
                .format(self.__class__.__name__), end='')
            print(os.path.abspath(filepath))
            sys.stdout.flush()
        frame = pandas.read_csv(filepath, **kwargs)
        _validate_column_names(frame.columns, self.file_columns)
        self.frame = frame
        if not quiet:
            print(
                '    {0} rows x {1} columns'.format(
                    frame.shape[0], frame.shape[1]))

    def from_database(self, quiet=True):
        """
        Read table data from the database.

        Parameters
        ----------
        quiet : bool, default True
            If True, no output will be written to standard output.
        """
        if not quiet:
            print(
                _bold('[{0}] reading database records: ')
                .format(self.__class__.__name__), end='')
            sys.stdout.flush()
        database = self.specify_context['database']
        to_exclude = (
            list(self.key_columns.values()) + list(self.static_content.keys()))
        frame_columns = [
            column for column in self.all_columns if column not in to_exclude]
        frame = query_to_dataframe(database, self.database_query)
        self.frame = pandas.DataFrame(frame, columns=frame_columns)
        if not quiet:
            print('{0}/{0}'.format(frame.shape[0]))

    def get_match_count(self, target_column, match_columns):
        """
        Return counts for matches and possible matches.

        Parameters
        ----------
        target_column : str
            Column that should have a value if any value in
            `match_columns` is not null.
        match_columns : str or List[str]
            Column or columns used for updating values in
            `target_column`.

        Returns
        -------
        tuple
            matches, possible matches
        """
        if isinstance(match_columns, basestring):
            match_columns = [match_columns]
        possible_matches = len(self.frame.dropna(
            how='all', subset=match_columns))
        matches = len(self.frame.dropna(subset=[target_column]))
        return (matches, possible_matches)

    def get_mismatches(self, target_column, match_columns):
        """
        Return a :class:`pandas.Series` or a :class:`pandas.DataFrame`
        with non-matching values.

        Parameters
        ----------
        target_column : str
            Column that should have a value if any value in
            `match_columns` is not null.
        match_columns : str or List[str]
            Column or columns used for updating values
            in `target_column`.
        """
        match_columns_notnull = pandas.DataFrame(
            self.frame[match_columns]).notnull().any(axis=1)
        target_column_isnull = self.frame[target_column].isnull()
        mismatches = self.frame[
            target_column_isnull & match_columns_notnull][match_columns]
        return mismatches

    def match_database_records(self, match_columns, quiet=True):
        """
        Update primary key values for records that match database.

        Parameters
        ----------
        match_columns : str or List[str]
            Columns to be matched against the database.
        quiet : bool, default False
            If True, no output will be written to standard output.
        """
        if not quiet:
            print(
                _bold('[{0}] updating primary key from database... ')
                .format(self.__class__.__name__))
            sys.stdout.flush()
        database = self.specify_context['database']
        if isinstance(match_columns, basestring):
            match_columns = [match_columns]
        db_frame = pandas.DataFrame(
            query_to_dataframe(database, self.database_query),
            columns=match_columns + [self.primary_key_column])
        db_frame.dropna(how='all', subset=match_columns, inplace=True)
        if (
            self.frame.dropna(subset=match_columns)
            .duplicated(subset=match_columns).any()
        ):
            warnings.warn(
                'Match-column(s) in frame contains non-unique values.')
        if db_frame.duplicated(subset=match_columns).any():
            warnings.warn(
                'Match-column(s) in database contains non-unique values.')
        self.frame = (
            self.frame.drop(labels=self.primary_key_column, axis=1)
            .merge(db_frame, how='left', on=match_columns))
        if not quiet:
            (matches, possible_matches) = self.get_match_count(
                self.primary_key_column, match_columns)
            print(
                '    target-column:   {0}\n'
                '    match-column(s): {1}\n'
                '    matches:         {2}/{3}'
                .format(
                    repr(self.primary_key_column),
                    match_columns, matches, possible_matches))

    def to_csv(
            self, filepath, update_sourceid=False, drop_empty_columns=False,
            quiet=True, encoding='utf-8', float_format='%g', index=False,
            **kwargs):
        """
        Write dataset a comma-separated values (CSV) file.

        Parameters
        ----------
        filepath : str
            File path or object.
        update_sourceid : bool, default False
            If True, copying ID-columns to SourceID-columns
            before writing to the CSV file.
        drop_empty_columns : bool, default False
            Drop columns that does not contain any data.
        quiet : bool, default True
            If True, no output will be written to standard output.
        encoding : str, default 'utf-8'
            A string representing the encoding to use in the output file.
        float_format : str or None, default '%g'
            Format string for floating point numbers.
        index : bool, default False
            Write row names (index).
        \**kwargs
            Arbitrary keyword arguments available in
            :meth:`pandas.DataFrame.to_csv`.
        """
        if update_sourceid:
            self.update_sourceid(quiet=quiet)
        if not quiet:
            print(
                _bold('[{0}] writing to CSV file: ')
                .format(self.__class__.__name__), end='')
            print(os.path.abspath(filepath))
            sys.stdout.flush()
        frame = pandas.DataFrame(self.frame[self.file_columns])
        if drop_empty_columns:
            frame = frame.dropna(axis=1, how='all')
        frame.to_csv(
            filepath, index=index,
            float_format=float_format, encoding=encoding, **kwargs)
        if not quiet:
            print(
                '    {0} rows x {1} columns'.format(
                    frame.shape[0], frame.shape[1]))

    def to_database(
            self, defaults=None, update_record_metadata=True,
            chunksize=10000, quiet=True):
        """
        Load a dataset into the corresponding table and update
        the dataset's primary key column from the database.

        Parameters
        ----------
        defaults : dict
            Column name and value to insert instead of nulls.
        update_record_metadata : bool, default True
            If True, record metadata will be generated during
            import, otherwise the metadata will be loaded from the dataset.
        chunksize : int
            Size of chunks being uploaded.
        quiet : bool, default True
            If True, no output will be written to standard output.
        """
        database = self.specify_context['database']
        print_msg = (
            _bold('[{}] loading records to database:')
            .format(self.__class__.__name__))
        mask = self.frame[self.primary_key_column].isnull()
        frame_to_upload = self.frame[mask]
        frame_uploaded = self.frame[~mask]
        timestamp_columns = []
        drop_columns = []  # columns to exclude before upload begins
        drop_columns.extend(
            [self.primary_key_column] + list(self.key_columns.values()))
        frame = frame_to_upload.copy()
        if defaults:
            frame = _insert_defaults(frame, defaults)
        if update_record_metadata:
            timestamp_columns = ['timestampcreated', 'timestampmodified']
            frame.createdbyagentid = self.specify_context['user_agentid']
            frame.modifiedbyagentid = self.specify_context['user_agentid']
            frame.version = 1
            drop_columns.extend(timestamp_columns)
        frame = frame.drop(labels=drop_columns, axis=1)
        frame = frame.dropna(axis=1, how='all')  # drop empty columns
        frame = frame.where(frame.notnull(), other=None)  # NaN --> None
        first_id = self._get_next_insert_id()
        total_records = len(frame)
        database.connect()
        with database.atomic():
            current_record = 0
            if not quiet:
                _print_process_status(print_msg, current_record, total_records)
            for chunk in _chunker(frame, chunksize):
                insert_query = self.model.insert_many(
                    _get_records(
                        chunk, timestamp_columns, self.static_content))
                insert_query.execute()
                current_record = current_record + len(chunk)
                if not quiet:
                    _print_process_status(
                        print_msg, current_record, total_records)
        database.close()
        next_id = self._get_next_insert_id()
        if not next_id == first_id:
            frame_to_upload = frame_to_upload.drop(
                labels=[self.primary_key_column], axis=1)
            frame_to_upload[self.primary_key_column] = pandas.Series(
                range(first_id, first_id + len(frame_to_upload)),
                index=frame_to_upload.index)
            self.frame = frame_uploaded.append(
                frame_to_upload, ignore_index=True)
        if not quiet:
            print()

    def update_database_records(
            self, columns, update_record_metadata=True, chunksize=10000,
            quiet=True):
        """
        Update records in database with matching primary key values.

        Parameters
        ----------
        columns : str or List[str]
            Column or columns with new values.
        update_record_metadata : bool, default True
            If True, record metadata will be generated during
            import, otherwise the metadata will be updated from the dataset.
        chunksize : int
            Size of chunks being updated; default 1000.
        quiet : bool, default True
            If True, no output will be written to standard output.
        """
        print_msg = (
            _bold('[{}] updating database records:')
            .format(self.__class__.__name__))
        if isinstance(columns, basestring):
            columns = [columns]
        database = self.specify_context['database']
        timestamp_columns = []
        drop_columns = []  # columns to exclude before update begins
        sys.stdout.flush()
        valid_columns = [
            column for column in self.database_columns
            if column != self.primary_key_column]
        _validate_column_names(columns, valid_columns)
        if self.frame[self.primary_key_column].duplicated().any():
            raise ValueError('Duplicated primary key values.')
        frame = self.frame.copy()
        if update_record_metadata:
            timestamp_columns = ['timestampmodified']
            static_content = {
                'modifiedbyagentid': self.specify_context['user_agentid']}
            if 'version' not in columns:
                columns.append('version')
            drop_columns.extend(timestamp_columns)
            frame.version = frame.version.fillna(0) + 1
        frame = (
            frame[[self.primary_key_column] + columns]
            .dropna(subset=[self.primary_key_column]))
        frame = frame.where(frame.notnull(), other=None)  # NaN --> None
        database.connect()
        with database.atomic():
            current_record = 0
            total_records = len(frame)
            if not quiet:
                _print_process_status(print_msg, current_record, total_records)
            for chunk in _chunker(frame, chunksize):
                records = _get_records(
                    chunk, timestamp_columns, static_content)
                for record in records:
                    update_query = self._get_update_query(record)
                    update_query.execute()
                current_record = current_record + len(chunk)
                if not quiet:
                    _print_process_status(
                        print_msg, current_record, total_records)
        database.close()
        if not quiet:
            print()

    def update_foreign_keys(self, from_datasets, quiet=False):
        """
        Update foreign key values from a related dataset based
        on sourceid values.

        Parameters
        ----------
        from_datasets : :class:`TableDataset` or List[:class:`TableDataset`]
            Dataset(s) from which foreign key values will be updated.
        quiet : bool, default False
            If True, no output will be written to standard output.
        """
        if not quiet:
            print(
                _bold('[{0}] updating foreign keys... ')
                .format(self.__class__.__name__))
            sys.stdout.flush()
        if isinstance(from_datasets, TableDataset):
            from_datasets = [from_datasets]
        for dataset in from_datasets:
            try:
                columns_to_update = self.foreign_key_columns[dataset.model]
            except KeyError:
                print(
                    'No columns related to dataset of class {0}.'
                    .format(dataset.__class__))
                raise
            for column_to_update in columns_to_update:
                update_from_column = getattr(
                    self.model, column_to_update).to_field.name
                left_on = self.key_columns[column_to_update]
                right_on = dataset.key_columns[update_from_column]
                if (
                    self.frame[left_on].notnull().any() and
                    dataset.frame[right_on].notnull().any()
                ):
                    right_frame = dataset.frame[[right_on, update_from_column]]
                    # Rename columns in the right frame
                    right_frame.columns = [left_on, column_to_update]
                    left_frame = self.frame.drop(
                        labels=[column_to_update], axis=1)
                    # Left join frames
                    left_frame = left_frame.merge(
                        right_frame, how='left', on=left_on)
                    self.frame = left_frame
                else:
                    self.frame[column_to_update] = nan
                if not quiet:
                    (matches, possible_matches) = self.get_match_count(
                        column_to_update, left_on)
                    print(
                        '    {0}: {1}/{2}'
                        .format(
                            repr(column_to_update), matches, possible_matches))

    def update_sourceid(self, quiet=True):
        """
        Copy values from ID-columns to SourceID-columns.

        Parameters
        ----------
        quiet : bool, default True
            If True, no output will be written to standard output.
        """
        if not quiet:
            print(
                _bold('[{0}] updating SourceID-columns... ')
                .format(self.__class__.__name__))
            sys.stdout.flush()
        for key_column in sorted(self.key_columns):
            if not quiet:
                not_null = self.frame[key_column].count()
                # value_string = 'value' if not_null == 1 else 'values'
                print(
                    '    copying {0} to {1} [{2} {3}]'
                    .format(
                        repr(key_column),
                        repr(self.key_columns[key_column]),
                        not_null,
                        _get_noun_form('value', 'values', not_null)))
                sys.stdout.flush()
                self.frame[
                    self.key_columns[key_column]
                ] = self.frame[key_column]

    def write_mapping_to_csv(
            self, filepath, quiet=True, float_format='%g',
            index=False, **kwargs):
        """
        Write ID-column mapping a comma-separated values (CSV) file.

        Parameters
        ----------
        filepath : str
            File path or object.
        quiet : bool, default True
            If True, no output will be written to standard output.
        float_format : str or None, default '%g'
            Format string for floating point numbers.
        index : bool, default False
            Write row names (index).
        \**kwargs
            Arbitrary keyword arguments available in
            :meth:`pandas.DataFrame.to_csv`.
        """
        if not quiet:
            print(
                _bold('[{0}] writing mapping to CSV file: ')
                .format(self.__class__.__name__), end='')
            print(os.path.abspath(filepath))
            sys.stdout.flush()
        columns = [
            self.primary_key_column, self.key_columns[self.primary_key_column]]
        frame = pandas.DataFrame(self.frame[columns])
        frame.to_csv(
            filepath, index=index, float_format=float_format, **kwargs)
        if not quiet:
            print(
                '    {0} rows x {1} columns'
                .format(
                    frame.shape[0], frame.shape[1]))
        if self.frame[columns].isnull().any().any():
            warnings.warn('Mapping is incomplete.')


class TreeDataset(object):
    """A dataset corresponding to a tree table in Specify."""

    def update_rankid_column(self, dataset, quiet=True):
        """
        Update RankID based on SourceID-column.

        Parameters
        ----------
        dataset : :class:`TableDataset`
            A treedefitem-dataset from which RankID should be updated.
        quiet : bool, default True
            If True, no output will be written to standard output.

        Notes
        -----
        This method exists in order to update the redundant RankID-columns
        in :class:`TreeDataset` dataframes.
        """
        if not quiet:
            print(
                _bold('[{0}] updating RankID... ')
                .format(self.__class__.__name__))
            sys.stdout.flush()
        expected_model_name = self.model.__name__ + 'treedefitem'
        if not dataset.model.__name__ == expected_model_name:
            raise TypeError(
                'RankID can only be updated from a dataset of '
                'type <{0}Dataset>'.format(expected_model_name))
        else:
            sourceid_name = dataset.key_columns[dataset.primary_key_column]
            right_frame = dataset.frame[[
                sourceid_name, 'rankid']]
            left_frame = self.frame
            left_frame = left_frame.drop(labels=['rankid'], axis=1)
            left_frame = left_frame.merge(
                right_frame, how='left', on=sourceid_name)
            self.frame = left_frame


class AgentDataset(TableDataset):
    """Dataset corresponding to the agent-table."""
    def __init__(self):
        model = specifymodels.Agent
        key_columns = {
            'agentid': 'agent_sourceid',
            'createdbyagentid': 'createdbyagent_sourceid',
            'modifiedbyagentid': 'modifiedbyagent_sourceid',
            'parentorganizationid': 'parentorganization_sourceid'
        }
        static_content = {
            'divisionid': self.specify_context['divisionid'],
            'specifyuserid': None
        }
        where_clause = (
            specifymodels.Agent.divisionid ==
            self.specify_context['divisionid']
        )
        frame = pandas.DataFrame()
        super(AgentDataset, self).__init__(
            model, key_columns, static_content, where_clause, frame)


class AddressofrecordDataset(TableDataset):
    """Dataset corresponding to the addressofrecord-table."""
    def __init__(self):
        model = specifymodels.Addressofrecord
        key_columns = {
            'addressofrecordid': 'addressofrecord_sourceid',
            'createdbyagentid': 'createdbyagent_sourceid',
            'modifiedbyagentid': 'modifiedbyagent_sourceid'
        }
        static_content = {}
        where_clause = None
        frame = pandas.DataFrame()
        super(AddressofrecordDataset, self).__init__(
            model, key_columns, static_content, where_clause, frame)


class RepositoryagreementDataset(TableDataset):
    """Dataset corresponding to the repositoryagreement-table."""
    def __init__(self):
        model = specifymodels.Repositoryagreement
        key_columns = {
            'repositoryagreementid': 'repositoryagreement_sourceid',
            'createdbyagentid': 'createdbyagent_sourceid',
            'modifiedbyagentid': 'modifiedbyagent_sourceid',
            'addressofrecordid': 'addressofrecord_sourceid',
            'agentid': 'agent_sourceid'
        }
        static_content = {
            'divisionid': self.specify_context['divisionid']
        }
        where_clause = (
            specifymodels.Repositoryagreement.divisionid == 
            self.specify_context['divisionid']
        )
        frame = pandas.DataFrame()
        super(RepositoryagreementDataset, self).__init__(
            model, key_columns, static_content, where_clause, frame)


class AccessionDataset(TableDataset):
    """Dataset corresponding to the accession-table."""
    def __init__(self):
        model = specifymodels.Accession
        key_columns = {
            'accessionid': 'accession_sourceid',
            'createdbyagentid': 'createdbyagent_sourceid',
            'modifiedbyagentid': 'modifiedbyagent_sourceid',
            'addressofrecordid': 'addressofrecord_sourceid',
            'repositoryagreementid': 'repositoryagreement_sourceid'    
        }
        static_content = {
            'divisionid': self.specify_context['divisionid']
        }
        where_clause = (
            specifymodels.Accession.divisionid == 
            self.specify_context['divisionid']
        )
        frame = pandas.DataFrame()
        super(AccessionDataset, self).__init__(
            model, key_columns, static_content, where_clause, frame) 


class GeographytreedefitemDataset(TableDataset):
    """Dataset corresponding to the geographytreedefitem-table."""
    def __init__(self):
        model = specifymodels.Geographytreedefitem
        key_columns = {
            'geographytreedefitemid': 'geographytreedefitem_sourceid',
            'createdbyagentid': 'createdbyagent_sourceid',
            'modifiedbyagentid': 'modifiedbyagent_sourceid',
            'parentitemid': 'parentitem_sourceid'
        }
        static_content = {
            'geographytreedefid': self.specify_context['geographytreedefid']
        }
        where_clause = (
            specifymodels.Geographytreedefitem.geographytreedefid ==
            self.specify_context['geographytreedefid']
        )
        frame = pandas.DataFrame()
        super(GeographytreedefitemDataset, self).__init__(
            model, key_columns, static_content, where_clause, frame)


class GeographyDataset(TableDataset, TreeDataset):
    """Dataset corresponding to the geography-table."""
    def __init__(self):
        model = specifymodels.Geography
        key_columns = {
            'geographyid': 'geography_sourceid',
            'geographytreedefitemid': 'geographytreedefitem_sourceid',
            'createdbyagentid': 'createdbyagent_sourceid',
            'modifiedbyagentid': 'modifiedbyagent_sourceid',
            'parentid': 'parent_sourceid',
            'acceptedid': 'accepted_sourceid'
        }
        static_content = {
            'geographytreedefid': self.specify_context['geographytreedefid']
        }
        where_clause = (
            specifymodels.Geography.geographytreedefid ==
            self.specify_context['geographytreedefid']
        )
        frame = pandas.DataFrame()
        super(GeographyDataset, self).__init__(
            model, key_columns, static_content, where_clause, frame)


class LocalityDataset(TableDataset):
    """Dataset corresponding to the locality-table."""
    def __init__(self):
        model = specifymodels.Locality
        key_columns = {
            'localityid': 'locality_sourceid',
            'geographyid': 'geography_sourceid',
            'createdbyagentid': 'createdbyagent_sourceid',
            'modifiedbyagentid': 'modifiedbyagent_sourceid'
        }
        static_content = {
            'disciplineid': self.specify_context['disciplineid']
        }
        where_clause = (
            specifymodels.Locality.disciplineid ==
            self.specify_context['disciplineid']
        )
        frame = pandas.DataFrame()
        super(LocalityDataset, self).__init__(
            model, key_columns, static_content, where_clause, frame)


class CollectingeventattributeDataset(TableDataset):
    """Dataset corresponding to the collectingeventattribute-table."""
    def __init__(self):
        model = specifymodels.Collectingeventattribute
        key_columns = {
            'collectingeventattributeid': 'collectingeventattribute_sourceid',
            'hosttaxonid': 'hosttaxon_sourceid',
            'createdbyagentid': 'createdbyagent_sourceid',
            'modifiedbyagentid': 'modifiedbyagent_sourceid'
        }
        static_content = {
            'disciplineid': self.specify_context['disciplineid']
        }
        where_clause = (
            specifymodels.Collectingeventattribute.disciplineid ==
            self.specify_context['disciplineid']
        )
        frame = pandas.DataFrame()
        super(CollectingeventattributeDataset, self).__init__(
            model, key_columns, static_content, where_clause, frame)


class CollectingeventDataset(TableDataset):
    """Dataset corresponding to the collectingevent-table."""
    def __init__(self):
        model = specifymodels.Collectingevent
        key_columns = {
            'collectingeventattributeid': 'collectingeventattribute_sourceid',
            'collectingeventid': 'collectingevent_sourceid',
            'localityid': 'locality_sourceid',
            'createdbyagentid': 'createdbyagent_sourceid',
            'modifiedbyagentid': 'modifiedbyagent_sourceid'
        }
        static_content = {
            'disciplineid': self.specify_context['disciplineid']
        }
        where_clause = (
            specifymodels.Collectingevent.disciplineid ==
            self.specify_context['disciplineid']
        )
        frame = pandas.DataFrame()
        super(CollectingeventDataset, self).__init__(
            model, key_columns, static_content, where_clause, frame)


class CollectorDataset(TableDataset):
    """Dataset corresponding to the collector-table."""
    def __init__(self):
        model = specifymodels.Collector
        key_columns = {
            'collectorid': 'collector_sourceid',
            'agentid': 'collector_agent_sourceid',
            'collectingeventid': 'collectingevent_sourceid',
            'createdbyagentid': 'createdbyagent_sourceid',
            'modifiedbyagentid': 'modifiedbyagent_sourceid'
        }
        static_content = {
            'divisionid': self.specify_context['divisionid']
        }
        where_clause = (
            (specifymodels.Collector.divisionid ==
            self.specify_context['divisionid']) & (
            specifymodels.Collectingevent.disciplineid ==
            self.specify_context['disciplineid']))
        frame = pandas.DataFrame()
        super(CollectorDataset, self).__init__(
            model, key_columns, static_content, where_clause, frame)


class CollectionobjectattributeDataset(TableDataset):
    """Dataset corresponding to the collectionobjectattribute-table."""
    def __init__(self):
        model = specifymodels.Collectionobjectattribute
        key_columns = {
            'collectionobjectattributeid':
                'collectionobjectattribute_sourceid',
            'createdbyagentid': 'createdbyagent_sourceid',
            'modifiedbyagentid': 'modifiedbyagent_sourceid'
        }
        static_content = {
            'collectionmemberid': self.specify_context['collectionid']
        }
        where_clause = (
            specifymodels.Collectionobjectattribute.collectionmemberid ==
            self.specify_context['collectionid']
        )
        frame = pandas.DataFrame()
        super(CollectionobjectattributeDataset, self).__init__(
            model, key_columns, static_content, where_clause, frame)


class CollectionobjectDataset(TableDataset):
    """Dataset corresponding to the collectionobject-table."""
    def __init__(self):
        model = specifymodels.Collectionobject
        key_columns = {
            'collectionobjectattributeid':
                'collectionobjectattribute_sourceid',
            'collectionobjectid': 'collectionobject_sourceid',
            'collectingeventid': 'collectingevent_sourceid',
            'catalogerid': 'cataloger_agent_sourceid',
            'createdbyagentid': 'createdbyagent_sourceid',
            'modifiedbyagentid': 'modifiedbyagent_sourceid'
        }
        static_content = {
            'collectionid': self.specify_context['collectionid'],
            'collectionmemberid': self.specify_context['collectionid']
        }
        where_clause = (
            specifymodels.Collectionobject.collectionid ==
            self.specify_context['collectionid']
        )
        frame = pandas.DataFrame()
        super(CollectionobjectDataset, self).__init__(
            model, key_columns, static_content, where_clause, frame)


class StoragetreedefitemDataset(TableDataset):
    """Dataset corresponding to the storagetreedefitem-table."""
    def __init__(self):
        model = specifymodels.Storagetreedefitem
        key_columns = {
            'storagetreedefitemid': 'storagetreedefitem_sourceid',
            'createdbyagentid': 'createdbyagent_sourceid',
            'modifiedbyagentid': 'modifiedbyagent_sourceid',
            'parentitemid': 'parentitem_sourceid'
        }
        static_content = {
            'storagetreedefid': self.specify_context['storagetreedefid']
        }
        where_clause = (
            specifymodels.Storagetreedefitem.storagetreedefid ==
            self.specify_context['storagetreedefid']
        )
        frame = pandas.DataFrame()
        super(StoragetreedefitemDataset, self).__init__(
            model, key_columns, static_content, where_clause, frame)


class StorageDataset(TableDataset, TreeDataset):
    """Dataset corresponding to the storage-table."""
    def __init__(self):
        model = specifymodels.Storage
        key_columns = {
            'storageid': 'storage_sourceid',
            'createdbyagentid': 'createdbyagent_sourceid',
            'modifiedbyagentid': 'modifiedbyagent_sourceid',
            'storagetreedefitemid': 'storagetreedefitem_sourceid',
            'parentid': 'parent_sourceid'
        }
        static_content = {
            'storagetreedefid': self.specify_context['storagetreedefid']
        }
        where_clause = (
            specifymodels.Storage.storagetreedefid ==
            self.specify_context['storagetreedefid']
        )
        frame = pandas.DataFrame()
        super(StorageDataset, self).__init__(
            model, key_columns, static_content, where_clause, frame)


class PreptypeDataset(TableDataset):
    """Dataset corresponding to the preptype-table."""
    def __init__(self):
        model = specifymodels.Preptype
        key_columns = {
            'preptypeid': 'preptype_sourceid',
            'createdbyagentid': 'createdbyagent_sourceid',
            'modifiedbyagentid': 'modifiedbyagent_sourceid'
        }
        static_content = {
            'collectionid': self.specify_context['collectionid']
        }
        where_clause = (
            specifymodels.Preptype.collectionid ==
            self.specify_context['collectionid']
        )
        frame = pandas.DataFrame()
        super(PreptypeDataset, self).__init__(
            model, key_columns, static_content, where_clause, frame)


class PreparationDataset(TableDataset):
    """Dataset corresponding to the preparation-table."""
    def __init__(self):
        model = specifymodels.Preparation
        key_columns = {
            'preparationid': 'preparation_sourceid',
            'collectionobjectid': 'collectionobject_sourceid',
            'preparedbyid': 'preparedby_agent_sourceid',
            'preptypeid': 'preptype_sourceid',
            'storageid': 'storage_sourceid',
            'createdbyagentid': 'createdbyagent_sourceid',
            'modifiedbyagentid': 'modifiedbyagent_sourceid'
        }
        static_content = {
            'collectionmemberid': self.specify_context['collectionid']
        }
        where_clause = (
            specifymodels.Preparation.collectionmemberid ==
            self.specify_context['collectionid']
        )
        frame = pandas.DataFrame()
        super(PreparationDataset, self).__init__(
            model, key_columns, static_content, where_clause, frame)


class TaxontreedefitemDataset(TableDataset):
    """Dataset corresponding to the taxontreedefitem-table."""
    def __init__(self):
        model = specifymodels.Taxontreedefitem
        key_columns = {
            'taxontreedefitemid': 'taxontreedefitem_sourceid',
            'createdbyagentid': 'createdbyagent_sourceid',
            'modifiedbyagentid': 'modifiedbyagent_sourceid',
            'parentitemid': 'parentitem_sourceid'
        }
        static_content = {
            'taxontreedefid': self.specify_context['taxontreedefid']
        }
        where_clause = (
            specifymodels.Taxontreedefitem.taxontreedefid ==
            self.specify_context['taxontreedefid']
        )
        frame = pandas.DataFrame()
        super(TaxontreedefitemDataset, self).__init__(
            model, key_columns, static_content, where_clause, frame)


class TaxonDataset(TableDataset, TreeDataset):
    """Dataset corresponding to the taxon-table."""
    def __init__(self):
        model = specifymodels.Taxon
        key_columns = {
            'taxonid': 'taxon_sourceid',
            'createdbyagentid': 'createdbyagent_sourceid',
            'modifiedbyagentid': 'modifiedbyagent_sourceid',
            'taxontreedefitemid': 'taxontreedefitem_sourceid',
            'parentid': 'parent_sourceid',
            'acceptedid': 'accepted_sourceid'
        }
        static_content = {
            'taxontreedefid': self.specify_context['taxontreedefid']
        }
        where_clause = (
            specifymodels.Taxon.taxontreedefid ==
            self.specify_context['taxontreedefid']
        )
        frame = pandas.DataFrame()
        super(TaxonDataset, self).__init__(
            model, key_columns, static_content, where_clause, frame)


class DeterminationDataset(TableDataset):
    """Dataset corresponding to the determination-table."""
    def __init__(self):
        model = specifymodels.Determination
        key_columns = {
            'determinationid': 'determination_sourceid',
            'determinerid': 'determiner_agent_sourceid',
            'collectionobjectid': 'collectionobject_sourceid',
            'taxonid': 'taxon_sourceid',
            'preferredtaxonid': 'preferredtaxon_sourceid',
            'createdbyagentid': 'createdbyagent_sourceid',
            'modifiedbyagentid': 'modifiedbyagent_sourceid'
        }
        static_content = {
            'collectionmemberid': self.specify_context['collectionid']
        }
        where_clause = (
            specifymodels.Determination.collectionmemberid ==
            self.specify_context['collectionid']
        )
        frame = pandas.DataFrame()
        super(DeterminationDataset, self).__init__(
            model, key_columns, static_content, where_clause, frame)
