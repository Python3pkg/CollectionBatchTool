#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *
from sys import byteorder


class BitField(Field):
    """Define a custom field type for MySQL's BIT data type"""
    dbField = 'bit'

    def db_value(self, value):
        return (
            None if value is None
            else (int(value)).to_bytes(1, byteorder=byteorder))

    def python_value(self, value):
        return (
            None if value is None
            else int.from_bytes(value, byteorder=byteorder))


MySQLDatabase.register_fields({'bit': 'BIT'})
database = MySQLDatabase(None)  # Un-initialized database


class BaseModel(Model):
    class Meta:
        database = database

DivisionProxy = Proxy()
TaxontreedefProxy = Proxy()
TaxonProxy = Proxy()


class Geographytreedef(BaseModel):
    geographytreedefid = PrimaryKeyField(db_column='GeographyTreeDefID')

    class Meta:
        db_table = 'geographytreedef'


class Specifyuser(BaseModel):
    name = CharField(db_column='Name', unique=True)
    specifyuserid = PrimaryKeyField(db_column='SpecifyUserID')

    class Meta:
        db_table = 'specifyuser'


class Agent(BaseModel):
    abbreviation = CharField(db_column='Abbreviation', index=True, null=True)
    agentid = PrimaryKeyField(db_column='AgentID')
    agenttype = IntegerField(db_column='AgentType', index=True)
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True,
        rel_model='self', to_field='agentid')
    dateofbirth = DateField(db_column='DateOfBirth', null=True)
    dateofbirthprecision = IntegerField(
        db_column='DateOfBirthPrecision', null=True)
    dateofdeath = DateField(db_column='DateOfDeath', null=True)
    dateofdeathprecision = IntegerField(
        db_column='DateOfDeathPrecision', null=True)
    datetype = IntegerField(db_column='DateType', null=True)
    divisionid = ForeignKeyField(
        db_column='DivisionID', null=True, rel_model=DivisionProxy,
        to_field='usergroupscopeid')
    email = CharField(db_column='Email', null=True)
    firstname = CharField(db_column='FirstName', index=True, null=True)
    guid = CharField(db_column='GUID', index=True, null=True)
    initials = CharField(db_column='Initials', null=True)
    interests = CharField(db_column='Interests', null=True)
    jobtitle = CharField(db_column='JobTitle', null=True)
    lastname = CharField(db_column='LastName', index=True, null=True)
    middleinitial = CharField(db_column='MiddleInitial', null=True)
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model='self',
        related_name='agent_modifiedbyagentid_set', to_field='agentid')
    parentorganizationid = ForeignKeyField(
        db_column='ParentOrganizationID', null=True, rel_model='self',
        related_name='agent_parentorganizationid_set', to_field='agentid')
    remarks = TextField(db_column='Remarks', null=True)
    specifyuserid = ForeignKeyField(
        db_column='SpecifyUserID', null=True,
        rel_model=Specifyuser, to_field='specifyuserid')
    suffix = CharField(db_column='Suffix', null=True)
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    title = CharField(db_column='Title', null=True)
    url = CharField(db_column='URL', null=True)
    version = IntegerField(db_column='Version', null=True)

    class Meta:
        db_table = 'agent'


class Storagetreedef(BaseModel):
    storagetreedefid = PrimaryKeyField(db_column='StorageTreeDefID')

    class Meta:
        db_table = 'storagetreedef'


class Institution(BaseModel):
    institutionid = IntegerField(db_column='institutionId', null=True)
    institution_name = CharField(db_column='Name', index=True, null=True)
    storagetreedefid = ForeignKeyField(
        db_column='StorageTreeDefID', null=True, rel_model=Storagetreedef,
        to_field='storagetreedefid')
    usergroupscopeid = PrimaryKeyField(db_column='UserGroupScopeId')

    class Meta:
        db_table = 'institution'


class Division(BaseModel):
    institutionid = ForeignKeyField(
        db_column='InstitutionID', rel_model=Institution,
        to_field='usergroupscopeid')
    division_name = CharField(db_column='Name', index=True, null=True)
    usergroupscopeid = PrimaryKeyField(db_column='UserGroupScopeId')
    divisionid = IntegerField(db_column='divisionId', null=True)

    class Meta:
        db_table = 'division'


class Discipline(BaseModel):
    divisionid = ForeignKeyField(
        db_column='DivisionID', rel_model=Division,
        to_field='usergroupscopeid')
    geographytreedefid = ForeignKeyField(
        db_column='GeographyTreeDefID', rel_model=Geographytreedef,
        to_field='geographytreedefid')
    discipline_name = CharField(db_column='Name', index=True, null=True)
    taxontreedefid = ForeignKeyField(
        db_column='TaxonTreeDefID', null=True, rel_model=TaxontreedefProxy,
        to_field='taxontreedefid')
    usergroupscopeid = PrimaryKeyField(db_column='UserGroupScopeId')
    disciplineid = IntegerField(db_column='disciplineId', null=True)

    class Meta:
        db_table = 'discipline'


class Addressofrecord(BaseModel):
    address = CharField(db_column='Address', null=True)
    address2 = CharField(db_column='Address2', null=True)
    addressofrecordid = PrimaryKeyField(db_column='AddressOfRecordID')
    agentid = ForeignKeyField(
        db_column='AgentID', null=True, rel_model=Agent, to_field='agentid')
    city = CharField(db_column='City', null=True)
    country = CharField(db_column='Country', null=True)
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True, rel_model=Agent,
        related_name='addressofrecord_createdbyagentid_set',
        to_field='agentid')
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model=Agent,
        related_name='addressofrecord_modifiedbyagentid_set',
        to_field='agentid')
    postalcode = CharField(db_column='PostalCode', null=True)
    remarks = TextField(db_column='Remarks', null=True)
    state = CharField(db_column='State', null=True)
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    version = IntegerField(db_column='Version', null=True)

    class Meta:
        db_table = 'addressofrecord'


class Repositoryagreement(BaseModel):
    addressofrecordid = ForeignKeyField(
        db_column='AddressOfRecordID', null=True, rel_model=Addressofrecord,
        to_field='addressofrecordid')
    agentid = ForeignKeyField(
        db_column='AgentID', rel_model=Agent, to_field='agentid')
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True, rel_model=Agent,
        related_name='repositoryagreement_createdbyagentid_set',
        to_field='agentid')
    datereceived = DateField(db_column='DateReceived', null=True)
    divisionid = ForeignKeyField(
        db_column='DivisionID', rel_model=Division,
        to_field='usergroupscopeid')
    enddate = DateField(db_column='EndDate', null=True)
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model=Agent,
        related_name='repositoryagreement_modifiedbyagentid_set',
        to_field='agentid')
    number1 = FloatField(db_column='Number1', null=True)
    number2 = FloatField(db_column='Number2', null=True)
    remarks = TextField(db_column='Remarks', null=True)
    repositoryagreementid = PrimaryKeyField(db_column='RepositoryAgreementID')
    repositoryagreementnumber = CharField(
        db_column='RepositoryAgreementNumber', index=True)
    startdate = DateField(db_column='StartDate', index=True, null=True)
    status = CharField(db_column='Status', null=True)
    text1 = CharField(db_column='Text1', null=True)
    text2 = CharField(db_column='Text2', null=True)
    text3 = CharField(db_column='Text3', null=True)
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    version = IntegerField(db_column='Version', null=True)
    yesno1 = BitField(db_column='YesNo1', null=True)  # bit
    yesno2 = BitField(db_column='YesNo2', null=True)  # bit

    class Meta:
        db_table = 'repositoryagreement'


class Accession(BaseModel):
    accessioncondition = CharField(db_column='AccessionCondition', null=True)
    accessionid = PrimaryKeyField(db_column='AccessionID')
    accessionnumber = CharField(db_column='AccessionNumber', index=True)
    addressofrecordid = ForeignKeyField(
        db_column='AddressOfRecordID', null=True, rel_model=Addressofrecord,
        to_field='addressofrecordid')
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True, rel_model=Agent,
        to_field='agentid')
    dateaccessioned = DateField(
        db_column='DateAccessioned', index=True, null=True)
    dateacknowledged = DateField(db_column='DateAcknowledged', null=True)
    datereceived = DateField(db_column='DateReceived', null=True)
    divisionid = ForeignKeyField(
        db_column='DivisionID', rel_model=Division,
        to_field='usergroupscopeid')
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model=Agent,
        related_name='accession_modifiedbyagentid_set', to_field='agentid')
    number1 = FloatField(db_column='Number1', null=True)
    number2 = FloatField(db_column='Number2', null=True)
    remarks = TextField(db_column='Remarks', null=True)
    repositoryagreementid = ForeignKeyField(
        db_column='RepositoryAgreementID', null=True,
        rel_model=Repositoryagreement, to_field='repositoryagreementid')
    status = CharField(db_column='Status', null=True)
    text1 = TextField(db_column='Text1', null=True)
    text2 = TextField(db_column='Text2', null=True)
    text3 = TextField(db_column='Text3', null=True)
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    totalvalue = DecimalField(db_column='TotalValue', null=True)
    type = CharField(db_column='Type', null=True)
    verbatimdate = CharField(db_column='VerbatimDate', null=True)
    version = IntegerField(db_column='Version', null=True)
    yesno1 = BitField(db_column='YesNo1', null=True)  # bit
    yesno2 = BitField(db_column='YesNo2', null=True)  # bit

    class Meta:
        db_table = 'accession'

class Accessionagent(BaseModel):
    accessionagentid = PrimaryKeyField(db_column='AccessionAgentID')
    accessionid = ForeignKeyField(
        db_column='AccessionID', null=True, rel_model=Accession,
        to_field='accessionid')
    agentid = ForeignKeyField(
        db_column='AgentID', rel_model=Agent, to_field='agentid')
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True, rel_model=Agent,
        related_name='accessionagent_createdbyagentid_set',
        to_field='agentid')
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model=Agent,
        related_name='accessionagent_modifiedbyagentid_set',
        to_field='agentid')
    remarks = TextField(db_column='Remarks', null=True)
    repositoryagreementid = ForeignKeyField(
        db_column='RepositoryAgreementID', null=True,
        rel_model=Repositoryagreement, to_field='repositoryagreementid')
    role = CharField(db_column='Role')
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    version = IntegerField(db_column='Version', null=True)

    class Meta:
        db_table = 'accessionagent'


class Collection(BaseModel):
    collectionname = CharField(
        db_column='CollectionName', index=True, null=True)
    disciplineid = ForeignKeyField(
        db_column='DisciplineID', rel_model=Discipline,
        to_field='usergroupscopeid')
    usergroupscopeid = PrimaryKeyField(db_column='UserGroupScopeId')
    collectionid = IntegerField(db_column='collectionId', null=True)

    class Meta:
        db_table = 'collection'


class Geographytreedefitem(BaseModel):
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True, rel_model=Agent,
        related_name='geographytreedefitem_createdbyagentid_set',
        to_field='agentid')
    fullnameseparator = CharField(db_column='FullNameSeparator', null=True)
    geographytreedefid = ForeignKeyField(
        db_column='GeographyTreeDefID', rel_model=Geographytreedef,
        to_field='geographytreedefid')
    geographytreedefitemid = PrimaryKeyField(
        db_column='GeographyTreeDefItemID')
    isenforced = BitField(db_column='IsEnforced', null=True)  # bit
    isinfullname = BitField(db_column='IsInFullName', null=True)  # bit
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model=Agent,
        related_name='geographytreedefitem_modifiedbyagentid_set',
        to_field='agentid')
    name = CharField(db_column='Name')
    parentitemid = ForeignKeyField(
        db_column='ParentItemID', null=True, rel_model='self',
        to_field='geographytreedefitemid')
    rankid = IntegerField(db_column='RankID')
    remarks = TextField(db_column='Remarks', null=True)
    textafter = CharField(db_column='TextAfter', null=True)
    textbefore = CharField(db_column='TextBefore', null=True)
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    title = CharField(db_column='Title', null=True)
    version = IntegerField(db_column='Version', null=True)

    class Meta:
        db_table = 'geographytreedefitem'


class Geography(BaseModel):
    abbrev = CharField(db_column='Abbrev', null=True)
    acceptedid = ForeignKeyField(
        db_column='AcceptedID', null=True, rel_model='self',
        to_field='geographyid')
    centroidlat = DecimalField(db_column='CentroidLat', null=True)
    centroidlon = DecimalField(db_column='CentroidLon', null=True)
    commonname = CharField(db_column='CommonName', null=True)
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True, rel_model=Agent,
        related_name='geography_createdbyagentid_set', to_field='agentid')
    fullname = CharField(db_column='FullName', index=True, null=True)
    gml = TextField(db_column='GML', null=True)
    guid = CharField(db_column='GUID', null=True)
    geographycode = CharField(db_column='GeographyCode', null=True)
    geographyid = PrimaryKeyField(db_column='GeographyID')
    geographytreedefid = ForeignKeyField(
        db_column='GeographyTreeDefID', rel_model=Geographytreedef,
        to_field='geographytreedefid')
    geographytreedefitemid = ForeignKeyField(
        db_column='GeographyTreeDefItemID', rel_model=Geographytreedefitem,
        to_field='geographytreedefitemid')
    highestchildnodenumber = IntegerField(
        db_column='HighestChildNodeNumber', null=True)
    isaccepted = BitField(db_column='IsAccepted')  # bit
    iscurrent = BitField(db_column='IsCurrent', null=True)  # bit
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model=Agent,
        related_name='geography_modifiedbyagentid_set', to_field='agentid')
    name = CharField(db_column='Name', index=True)
    nodenumber = IntegerField(db_column='NodeNumber', null=True)
    number1 = IntegerField(db_column='Number1', null=True)
    number2 = IntegerField(db_column='Number2', null=True)
    parentid = ForeignKeyField(
        db_column='ParentID', null=True, rel_model='self',
        related_name='geography_parentid_set', to_field='geographyid')
    rankid = IntegerField(db_column='RankID')
    remarks = TextField(db_column='Remarks', null=True)
    text1 = CharField(db_column='Text1', null=True)
    text2 = CharField(db_column='Text2', null=True)
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    timestampversion = DateTimeField(db_column='TimestampVersion', null=True)
    version = IntegerField(db_column='Version', null=True)

    class Meta:
        db_table = 'geography'


class Locality(BaseModel):
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True, rel_model=Agent,
        related_name='locality_createdbyagentid_set', to_field='agentid')
    datum = CharField(db_column='Datum', null=True)
    disciplineid = ForeignKeyField(
        db_column='DisciplineID', rel_model=Discipline,
        to_field='usergroupscopeid')
    elevationaccuracy = FloatField(db_column='ElevationAccuracy', null=True)
    elevationmethod = CharField(db_column='ElevationMethod', null=True)
    gml = TextField(db_column='GML', null=True)
    guid = CharField(db_column='GUID', null=True)
    geographyid = ForeignKeyField(
        db_column='GeographyID', null=True,
        rel_model=Geography, to_field='geographyid')
    lat1text = CharField(db_column='Lat1Text', null=True)
    lat2text = CharField(db_column='Lat2Text', null=True)
    latlongaccuracy = FloatField(db_column='LatLongAccuracy', null=True)
    latlongmethod = CharField(db_column='LatLongMethod', null=True)
    latlongtype = CharField(db_column='LatLongType', null=True)
    latitude1 = DecimalField(db_column='Latitude1', null=True)
    latitude2 = DecimalField(db_column='Latitude2', null=True)
    localityid = PrimaryKeyField(db_column='LocalityID')
    localityname = CharField(db_column='LocalityName', index=True)
    long1text = CharField(db_column='Long1Text', null=True)
    long2text = CharField(db_column='Long2Text', null=True)
    longitude1 = DecimalField(db_column='Longitude1', null=True)
    longitude2 = DecimalField(db_column='Longitude2', null=True)
    maxelevation = FloatField(db_column='MaxElevation', null=True)
    minelevation = FloatField(db_column='MinElevation', null=True)
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model=Agent,
        related_name='locality_modifiedbyagentid_set', to_field='agentid')
    namedplace = CharField(db_column='NamedPlace', index=True, null=True)
    originalelevationunit = CharField(
        db_column='OriginalElevationUnit', null=True)
    originallatlongunit = IntegerField(
        db_column='OriginalLatLongUnit', null=True)
    relationtonamedplace = CharField(
        db_column='RelationToNamedPlace', index=True, null=True)
    remarks = TextField(db_column='Remarks', null=True)
    shortname = CharField(db_column='ShortName', null=True)
    srclatlongunit = IntegerField(db_column='SrcLatLongUnit')
    text1 = TextField(db_column='Text1', null=True)
    text2 = TextField(db_column='Text2', null=True)
    text3 = TextField(db_column='Text3', null=True)
    text4 = TextField(db_column='Text4', null=True)
    text5 = TextField(db_column='Text5', null=True)
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    verbatimelevation = CharField(db_column='VerbatimElevation', null=True)
    verbatimlatitude = CharField(db_column='VerbatimLatitude', null=True)
    verbatimlongitude = CharField(db_column='VerbatimLongitude', null=True)
    version = IntegerField(db_column='Version', null=True)

    class Meta:
        db_table = 'locality'


class Collectingeventattribute(BaseModel):
    collectingeventattributeid = PrimaryKeyField(
        db_column='CollectingEventAttributeID')
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True, rel_model=Agent,
        related_name='collectingeventattribute_createdbyagentid_set',
        to_field='agentid')
    disciplineid = ForeignKeyField(
        db_column='DisciplineID', rel_model=Discipline,
        to_field='usergroupscopeid')
    hosttaxonid = ForeignKeyField(
        db_column='HostTaxonID', null=True, rel_model=TaxonProxy,
        to_field='taxonid')
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model=Agent,
        related_name='collectingeventattribute_modifiedbyagentid_set',
        to_field='agentid')
    number1 = FloatField(db_column='Number1', null=True)
    number10 = FloatField(db_column='Number10', null=True)
    number11 = FloatField(db_column='Number11', null=True)
    number12 = FloatField(db_column='Number12', null=True)
    number13 = FloatField(db_column='Number13', null=True)
    number2 = FloatField(db_column='Number2', null=True)
    number3 = FloatField(db_column='Number3', null=True)
    number4 = FloatField(db_column='Number4', null=True)
    number5 = FloatField(db_column='Number5', null=True)
    number6 = FloatField(db_column='Number6', null=True)
    number7 = FloatField(db_column='Number7', null=True)
    number8 = FloatField(db_column='Number8', null=True)
    number9 = FloatField(db_column='Number9', null=True)
    remarks = TextField(db_column='Remarks', null=True)
    text1 = TextField(db_column='Text1', null=True)
    text10 = CharField(db_column='Text10', null=True)
    text11 = CharField(db_column='Text11', null=True)
    text12 = CharField(db_column='Text12', null=True)
    text13 = CharField(db_column='Text13', null=True)
    text14 = CharField(db_column='Text14', null=True)
    text15 = CharField(db_column='Text15', null=True)
    text16 = CharField(db_column='Text16', null=True)
    text17 = CharField(db_column='Text17', null=True)
    text2 = TextField(db_column='Text2', null=True)
    text3 = TextField(db_column='Text3', null=True)
    text4 = CharField(db_column='Text4', null=True)
    text5 = CharField(db_column='Text5', null=True)
    text6 = CharField(db_column='Text6', null=True)
    text7 = CharField(db_column='Text7', null=True)
    text8 = CharField(db_column='Text8', null=True)
    text9 = CharField(db_column='Text9', null=True)
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    version = IntegerField(db_column='Version', null=True)
    yesno1 = BitField(db_column='YesNo1', null=True)  # bit
    yesno2 = BitField(db_column='YesNo2', null=True)  # bit
    yesno3 = BitField(db_column='YesNo3', null=True)  # bit
    yesno4 = BitField(db_column='YesNo4', null=True)  # bit
    yesno5 = BitField(db_column='YesNo5', null=True)  # bit

    class Meta:
        db_table = 'collectingeventattribute'


class Collectingevent(BaseModel):
    collectingeventattributeid = ForeignKeyField(
        db_column='CollectingEventAttributeID', null=True,
        rel_model=Collectingeventattribute,
        to_field='collectingeventattributeid')
    collectingeventid = PrimaryKeyField(db_column='CollectingEventID')
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True, rel_model=Agent,
        to_field='agentid')
    disciplineid = ForeignKeyField(
        db_column='DisciplineID', rel_model=Discipline,
        to_field='usergroupscopeid')
    enddate = DateField(db_column='EndDate', index=True, null=True)
    enddateprecision = IntegerField(db_column='EndDatePrecision', null=True)
    enddateverbatim = CharField(db_column='EndDateVerbatim', null=True)
    endtime = IntegerField(db_column='EndTime', null=True)
    guid = CharField(db_column='GUID', index=True, null=True)
    integer1 = IntegerField(db_column='Integer1', null=True)
    integer2 = IntegerField(db_column='Integer2', null=True)
    localityid = ForeignKeyField(
        db_column='LocalityID', null=True, rel_model=Locality,
        to_field='localityid')
    method = CharField(db_column='Method', null=True)
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model=Agent,
        related_name='collectingevent_modifiedbyagentid_set',
        to_field='agentid')
    remarks = TextField(db_column='Remarks', null=True)
    startdate = DateField(db_column='StartDate', index=True, null=True)
    startdateprecision = IntegerField(
        db_column='StartDatePrecision', null=True)
    startdateverbatim = CharField(db_column='StartDateVerbatim', null=True)
    starttime = IntegerField(db_column='StartTime', null=True)
    stationfieldnumber = CharField(
        db_column='StationFieldNumber', index=True, null=True)
    text1 = TextField(db_column='Text1', null=True)
    text2 = TextField(db_column='Text2', null=True)
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    verbatimdate = CharField(db_column='VerbatimDate', null=True)
    verbatimlocality = TextField(db_column='VerbatimLocality', null=True)
    version = IntegerField(db_column='Version', null=True)

    class Meta:
        db_table = 'collectingevent'


class Collector(BaseModel):
    agentid = ForeignKeyField(
        db_column='AgentID', rel_model=Agent, to_field='agentid')
    collectingeventid = ForeignKeyField(
        db_column='CollectingEventID', rel_model=Collectingevent,
        to_field='collectingeventid')
    collectorid = PrimaryKeyField(db_column='CollectorID')
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True,
        rel_model=Agent, related_name='collector_createdbyagentid_set',
        to_field='agentid')
    divisionid = ForeignKeyField(
        db_column='DivisionID', null=True, rel_model=Division,
        to_field='usergroupscopeid')
    isprimary = BitField(db_column='IsPrimary')  # bit
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model=Agent,
        related_name='collector_modifiedbyagentid_set',
        to_field='agentid')
    ordernumber = IntegerField(db_column='OrderNumber')
    remarks = TextField(db_column='Remarks', null=True)
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    version = IntegerField(db_column='Version', null=True)

    class Meta:
        db_table = 'collector'


class Collectionobjectattribute(BaseModel):
    bottomdistance = FloatField(db_column='BottomDistance', null=True)
    collectionmemberid = IntegerField(
        db_column='CollectionMemberID', index=True)
    collectionobjectattributeid = PrimaryKeyField(
        db_column='CollectionObjectAttributeID')
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True, rel_model=Agent,
        related_name='collectionobjectattribute_createdbyagentid',
        to_field='agentid')
    direction = CharField(db_column='Direction', null=True)
    distanceunits = CharField(db_column='DistanceUnits', null=True)
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model=Agent,
        related_name='collectionobjectattribute_modifiedbyagentid_set',
        to_field='agentid')
    number1 = FloatField(db_column='Number1', null=True)
    number10 = FloatField(db_column='Number10', null=True)
    number11 = FloatField(db_column='Number11', null=True)
    number12 = FloatField(db_column='Number12', null=True)
    number13 = FloatField(db_column='Number13', null=True)
    number14 = FloatField(db_column='Number14', null=True)
    number15 = FloatField(db_column='Number15', null=True)
    number16 = FloatField(db_column='Number16', null=True)
    number17 = FloatField(db_column='Number17', null=True)
    number18 = FloatField(db_column='Number18', null=True)
    number19 = FloatField(db_column='Number19', null=True)
    number2 = FloatField(db_column='Number2', null=True)
    number20 = FloatField(db_column='Number20', null=True)
    number21 = FloatField(db_column='Number21', null=True)
    number22 = FloatField(db_column='Number22', null=True)
    number23 = FloatField(db_column='Number23', null=True)
    number24 = FloatField(db_column='Number24', null=True)
    number25 = FloatField(db_column='Number25', null=True)
    number26 = FloatField(db_column='Number26', null=True)
    number27 = FloatField(db_column='Number27', null=True)
    number28 = FloatField(db_column='Number28', null=True)
    number29 = FloatField(db_column='Number29', null=True)
    number3 = FloatField(db_column='Number3', null=True)
    number30 = IntegerField(db_column='Number30', null=True)
    number31 = FloatField(db_column='Number31', null=True)
    number32 = FloatField(db_column='Number32', null=True)
    number33 = FloatField(db_column='Number33', null=True)
    number34 = FloatField(db_column='Number34', null=True)
    number35 = FloatField(db_column='Number35', null=True)
    number36 = FloatField(db_column='Number36', null=True)
    number37 = FloatField(db_column='Number37', null=True)
    number38 = FloatField(db_column='Number38', null=True)
    number39 = FloatField(db_column='Number39', null=True)
    number4 = FloatField(db_column='Number4', null=True)
    number40 = FloatField(db_column='Number40', null=True)
    number41 = FloatField(db_column='Number41', null=True)
    number42 = FloatField(db_column='Number42', null=True)
    number5 = FloatField(db_column='Number5', null=True)
    number6 = FloatField(db_column='Number6', null=True)
    number7 = FloatField(db_column='Number7', null=True)
    number8 = IntegerField(db_column='Number8', null=True)
    number9 = FloatField(db_column='Number9', null=True)
    positionstate = CharField(db_column='PositionState', null=True)
    remarks = TextField(db_column='Remarks', null=True)
    text1 = TextField(db_column='Text1', null=True)
    text10 = CharField(db_column='Text10', null=True)
    text11 = CharField(db_column='Text11', null=True)
    text12 = CharField(db_column='Text12', null=True)
    text13 = CharField(db_column='Text13', null=True)
    text14 = CharField(db_column='Text14', null=True)
    text15 = CharField(db_column='Text15', null=True)
    text2 = TextField(db_column='Text2', null=True)
    text3 = TextField(db_column='Text3', null=True)
    text4 = CharField(db_column='Text4', null=True)
    text5 = CharField(db_column='Text5', null=True)
    text6 = CharField(db_column='Text6', null=True)
    text7 = CharField(db_column='Text7', null=True)
    text8 = CharField(db_column='Text8', null=True)
    text9 = CharField(db_column='Text9', null=True)
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    topdistance = FloatField(db_column='TopDistance', null=True)
    version = IntegerField(db_column='Version', null=True)
    yesno1 = BitField(db_column='YesNo1', null=True)  # bit
    yesno2 = BitField(db_column='YesNo2', null=True)  # bit
    yesno3 = BitField(db_column='YesNo3', null=True)  # bit
    yesno4 = BitField(db_column='YesNo4', null=True)  # bit
    yesno5 = BitField(db_column='YesNo5', null=True)  # bit
    yesno6 = BitField(db_column='YesNo6', null=True)  # bit
    yesno7 = BitField(db_column='YesNo7', null=True)  # bit

    class Meta:
        db_table = 'collectionobjectattribute'


class Collectionobject(BaseModel):
    altcatalognumber = CharField(db_column='AltCatalogNumber', null=True)
    availability = CharField(db_column='Availability', null=True)
    catalognumber = CharField(db_column='CatalogNumber', index=True, null=True)
    catalogeddate = DateField(db_column='CatalogedDate', index=True, null=True)
    catalogeddateprecision = IntegerField(
        db_column='CatalogedDatePrecision', null=True)
    catalogeddateverbatim = CharField(
        db_column='CatalogedDateVerbatim', null=True)
    catalogerid = ForeignKeyField(
        db_column='CatalogerID', null=True, rel_model=Agent,
        to_field='agentid')
    collectingeventid = ForeignKeyField(
        db_column='CollectingEventID', null=True, rel_model=Collectingevent,
        to_field='collectingeventid')
    collectionid = ForeignKeyField(
        db_column='CollectionID', rel_model=Collection,
        to_field='usergroupscopeid')
    collectionmemberid = IntegerField(
        db_column='CollectionMemberID', index=True)
    collectionobjectattributeid = ForeignKeyField(
        db_column='CollectionObjectAttributeID', null=True,
        rel_model=Collectionobjectattribute,
        to_field='collectionobjectattributeid')
    collectionobjectid = PrimaryKeyField(db_column='CollectionObjectID')
    countamt = IntegerField(db_column='CountAmt', null=True)
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True, rel_model=Agent,
        related_name='collectionobject_createdbyagentid_set',
        to_field='agentid')
    deaccessioned = BitField(db_column='Deaccessioned', null=True)  # bit
    description = CharField(db_column='Description', null=True)
    fieldnumber = CharField(db_column='FieldNumber', index=True, null=True)
    guid = CharField(db_column='GUID', index=True, null=True)
    integer1 = IntegerField(db_column='Integer1', null=True)
    integer2 = IntegerField(db_column='Integer2', null=True)
    inventorydate = DateField(db_column='InventoryDate', null=True)
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model=Agent,
        related_name='collectionobject_modifiedbyagentid_set',
        to_field='agentid')
    modifier = CharField(db_column='Modifier', null=True)
    name = CharField(db_column='Name', null=True)
    notifications = CharField(db_column='Notifications', null=True)
    number1 = FloatField(db_column='Number1', null=True)
    number2 = FloatField(db_column='Number2', null=True)
    ocr = TextField(db_column='OCR', null=True)
    objectcondition = CharField(db_column='ObjectCondition', null=True)
    projectnumber = CharField(db_column='ProjectNumber', null=True)
    remarks = TextField(db_column='Remarks', null=True)
    restrictions = CharField(db_column='Restrictions', null=True)
    text1 = TextField(db_column='Text1', null=True)
    text2 = TextField(db_column='Text2', null=True)
    text3 = TextField(db_column='Text3', null=True)
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    totalvalue = DecimalField(db_column='TotalValue', null=True)
    version = IntegerField(db_column='Version', null=True)
    yesno1 = BitField(db_column='YesNo1', null=True)  # bit
    yesno2 = BitField(db_column='YesNo2', null=True)  # bit
    yesno3 = BitField(db_column='YesNo3', null=True)  # bit
    yesno4 = BitField(db_column='YesNo4', null=True)  # bit
    yesno5 = BitField(db_column='YesNo5', null=True)  # bit
    yesno6 = BitField(db_column='YesNo6', null=True)  # bit

    class Meta:
        db_table = 'collectionobject'


class Storagetreedefitem(BaseModel):
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True, rel_model=Agent,
        related_name='storagetreedefitem_createdbyagentid_set',
        to_field='agentid')
    fullnameseparator = CharField(db_column='FullNameSeparator', null=True)
    isenforced = BitField(db_column='IsEnforced', null=True)  # bit
    isinfullname = BitField(db_column='IsInFullName', null=True)  # bit
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model=Agent,
        related_name='storagetreedefitem_modifiedbyagentid_set',
        to_field='agentid')
    name = CharField(db_column='Name')
    parentitemid = ForeignKeyField(
        db_column='ParentItemID', null=True, rel_model='self',
        to_field='storagetreedefitemid')
    rankid = IntegerField(db_column='RankID')
    remarks = TextField(db_column='Remarks', null=True)
    storagetreedefid = ForeignKeyField(
        db_column='StorageTreeDefID', rel_model=Storagetreedef,
        to_field='storagetreedefid')
    storagetreedefitemid = PrimaryKeyField(db_column='StorageTreeDefItemID')
    textafter = CharField(db_column='TextAfter', null=True)
    textbefore = CharField(db_column='TextBefore', null=True)
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    title = CharField(db_column='Title', null=True)
    version = IntegerField(db_column='Version', null=True)

    class Meta:
        db_table = 'storagetreedefitem'


class Storage(BaseModel):
    abbrev = CharField(db_column='Abbrev', null=True)
    acceptedid = ForeignKeyField(
        db_column='AcceptedID', null=True, rel_model='self',
        to_field='storageid')
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True, rel_model=Agent,
        related_name='storage_createdbyagentid_set', to_field='agentid')
    fullname = CharField(db_column='FullName', index=True, null=True)
    highestchildnodenumber = IntegerField(
        db_column='HighestChildNodeNumber', null=True)
    isaccepted = BitField(db_column='IsAccepted')  # bit
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model=Agent,
        related_name='storage_modifiedbyagentid_set', to_field='agentid')
    name = CharField(db_column='Name', index=True)
    nodenumber = IntegerField(db_column='NodeNumber', null=True)
    number1 = IntegerField(db_column='Number1', null=True)
    number2 = IntegerField(db_column='Number2', null=True)
    parentid = ForeignKeyField(
        db_column='ParentID', null=True, rel_model='self',
        related_name='storage_parentid_set', to_field='storageid')
    rankid = IntegerField(db_column='RankID')
    remarks = TextField(db_column='Remarks', null=True)
    storageid = PrimaryKeyField(db_column='StorageID')
    storagetreedefid = ForeignKeyField(
        db_column='StorageTreeDefID', rel_model=Storagetreedef,
        to_field='storagetreedefid')
    storagetreedefitemid = ForeignKeyField(
        db_column='StorageTreeDefItemID', rel_model=Storagetreedefitem,
        to_field='storagetreedefitemid')
    text1 = CharField(db_column='Text1', null=True)
    text2 = CharField(db_column='Text2', null=True)
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    timestampversion = DateTimeField(db_column='TimestampVersion', null=True)
    version = IntegerField(db_column='Version', null=True)

    class Meta:
        db_table = 'storage'


class Preptype(BaseModel):
    collectionid = ForeignKeyField(
        db_column='CollectionID', rel_model=Collection,
        to_field='usergroupscopeid')
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True, rel_model=Agent,
        to_field='agentid')
    isloanable = BitField(db_column='IsLoanable')  # bit
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model=Agent,
        related_name='preptype_modifiedbyagentid_set', to_field='agentid')
    name = CharField(db_column='Name')
    preptypeid = PrimaryKeyField(db_column='PrepTypeID')
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    version = IntegerField(db_column='Version', null=True)

    class Meta:
        db_table = 'preptype'


class Preparation(BaseModel):
    collectionmemberid = IntegerField(
        db_column='CollectionMemberID', index=True)
    collectionobjectid = ForeignKeyField(
        db_column='CollectionObjectID', rel_model=Collectionobject,
        to_field='collectionobjectid')
    countamt = IntegerField(db_column='CountAmt', null=True)
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True, rel_model=Agent,
        to_field='agentid')
    description = CharField(db_column='Description', null=True)
    integer1 = IntegerField(db_column='Integer1', null=True)
    integer2 = IntegerField(db_column='Integer2', null=True)
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model=Agent,
        related_name='preparation_modifiedbyagentid_set', to_field='agentid')
    number1 = FloatField(db_column='Number1', null=True)
    number2 = FloatField(db_column='Number2', null=True)
    preptypeid = ForeignKeyField(
        db_column='PrepTypeID', rel_model=Preptype, to_field='preptypeid')
    preparationid = PrimaryKeyField(db_column='PreparationID')
    preparedbyid = ForeignKeyField(
        db_column='PreparedByID', null=True, rel_model=Agent,
        related_name='agent_preparedbyid_set', to_field='agentid')
    prepareddate = DateField(db_column='PreparedDate', index=True, null=True)
    prepareddateprecision = IntegerField(
        db_column='PreparedDatePrecision', null=True)
    remarks = TextField(db_column='Remarks', null=True)
    samplenumber = CharField(db_column='SampleNumber', null=True)
    status = CharField(db_column='Status', null=True)
    storageid = ForeignKeyField(
        db_column='StorageID', null=True, rel_model=Storage,
        to_field='storageid')
    storagelocation = CharField(db_column='StorageLocation', null=True)
    text1 = TextField(db_column='Text1', null=True)
    text2 = TextField(db_column='Text2', null=True)
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    version = IntegerField(db_column='Version', null=True)
    yesno1 = BitField(db_column='YesNo1', null=True)  # bit
    yesno2 = BitField(db_column='YesNo2', null=True)  # bit
    yesno3 = BitField(db_column='YesNo3', null=True)  # bit

    class Meta:
        db_table = 'preparation'


class Taxontreedef(BaseModel):
    taxontreedefid = PrimaryKeyField(db_column='TaxonTreeDefID')

    class Meta:
        db_table = 'taxontreedef'


class Taxontreedefitem(BaseModel):
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True, rel_model=Agent,
        related_name='taxontreedefitem_createdbyagentid_set',
        to_field='agentid')
    formattoken = CharField(
        db_column='FormatToken', null=True)
    fullnameseparator = CharField(db_column='FullNameSeparator', null=True)
    isenforced = BitField(db_column='IsEnforced', null=True)  # bit
    isinfullname = BitField(db_column='IsInFullName', null=True)  # bit
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model=Agent,
        related_name='taxontreedefitem_modifiedbyagentid_set',
        to_field='agentid')
    name = CharField(db_column='Name')
    parentitemid = ForeignKeyField(
        db_column='ParentItemID', null=True, rel_model='self',
        to_field='taxontreedefitemid')
    rankid = IntegerField(db_column='RankID')
    remarks = TextField(db_column='Remarks', null=True)
    taxontreedefid = ForeignKeyField(
        db_column='TaxonTreeDefID', rel_model=Taxontreedef,
        to_field='taxontreedefid')
    taxontreedefitemid = PrimaryKeyField(db_column='TaxonTreeDefItemID')
    textafter = CharField(db_column='TextAfter', null=True)
    textbefore = CharField(db_column='TextBefore', null=True)
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    title = CharField(db_column='Title', null=True)
    version = IntegerField(db_column='Version', null=True)

    class Meta:
        db_table = 'taxontreedefitem'


class Taxon(BaseModel):
    acceptedid = ForeignKeyField(
        db_column='AcceptedID', null=True, rel_model='self',
        to_field='taxonid')
    author = CharField(db_column='Author', null=True)
    colstatus = CharField(db_column='COLStatus', null=True)
    citesstatus = CharField(db_column='CitesStatus', null=True)
    commonname = CharField(db_column='CommonName', index=True, null=True)
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True, rel_model=Agent,
        related_name='taxon_createdbyagentid_set', to_field='agentid')
    cultivarname = CharField(db_column='CultivarName', null=True)
    environmentalprotectionstatus = CharField(
        db_column='EnvironmentalProtectionStatus', index=True, null=True)
    esastatus = CharField(db_column='EsaStatus', null=True)
    fullname = CharField(db_column='FullName', index=True, null=True)
    guid = CharField(db_column='GUID', index=True, null=True)
    groupnumber = CharField(db_column='GroupNumber', null=True)
    highestchildnodenumber = IntegerField(
        db_column='HighestChildNodeNumber', null=True)
    hybridparent1id = ForeignKeyField(
        db_column='HybridParent1ID', null=True, rel_model='self',
        related_name='taxon_hybridparent1id_set', to_field='taxonid')
    hybridparent2id = ForeignKeyField(
        db_column='HybridParent2ID', null=True, rel_model='self',
        related_name='taxon_hybridparent2id_set', to_field='taxonid')
    isaccepted = BitField(db_column='IsAccepted')  # bit
    ishybrid = BitField(db_column='IsHybrid')  # bit
    isisnumber = CharField(db_column='IsisNumber', null=True)
    labelformat = CharField(db_column='LabelFormat', null=True)
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model=Agent,
        related_name='taxon_modifiedbyagentid_set', to_field='agentid')
    name = CharField(db_column='Name', index=True)
    ncbitaxonnumber = CharField(db_column='NcbiTaxonNumber', null=True)
    nodenumber = IntegerField(db_column='NodeNumber', null=True)
    number1 = IntegerField(db_column='Number1', null=True)
    number2 = IntegerField(db_column='Number2', null=True)
    number3 = FloatField(db_column='Number3', null=True)
    number4 = FloatField(db_column='Number4', null=True)
    number5 = FloatField(db_column='Number5', null=True)
    parentid = ForeignKeyField(
        db_column='ParentID', null=True, rel_model='self',
        related_name='taxon_parentid_set', to_field='taxonid')
    rankid = IntegerField(db_column='RankID')
    remarks = TextField(db_column='Remarks', null=True)
    source = CharField(db_column='Source', null=True)
    taxonid = PrimaryKeyField(db_column='TaxonID')
    taxontreedefid = ForeignKeyField(
        db_column='TaxonTreeDefID', rel_model=Taxontreedef,
        to_field='taxontreedefid')
    taxontreedefitemid = ForeignKeyField(
        db_column='TaxonTreeDefItemID', rel_model=Taxontreedefitem,
        to_field='taxontreedefitemid')
    taxonomicserialnumber = CharField(
        db_column='TaxonomicSerialNumber', index=True, null=True)
    text1 = CharField(db_column='Text1', null=True)
    text2 = CharField(db_column='Text2', null=True)
    text3 = TextField(db_column='Text3', null=True)
    text4 = TextField(db_column='Text4', null=True)
    text5 = TextField(db_column='Text5', null=True)
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    unitind1 = CharField(db_column='UnitInd1', null=True)
    unitind2 = CharField(db_column='UnitInd2', null=True)
    unitind3 = CharField(db_column='UnitInd3', null=True)
    unitind4 = CharField(db_column='UnitInd4', null=True)
    unitname1 = CharField(db_column='UnitName1', null=True)
    unitname2 = CharField(db_column='UnitName2', null=True)
    unitname3 = CharField(db_column='UnitName3', null=True)
    unitname4 = CharField(db_column='UnitName4', null=True)
    usfwscode = CharField(db_column='UsfwsCode', null=True)
    version = IntegerField(db_column='Version', null=True)
    yesno1 = BitField(db_column='YesNo1', null=True)  # bit
    yesno2 = BitField(db_column='YesNo2', null=True)  # bit
    yesno3 = BitField(db_column='YesNo3', null=True)  # bit

    class Meta:
        db_table = 'taxon'


class Determination(BaseModel):
    addendum = CharField(db_column='Addendum', null=True)
    alternatename = CharField(db_column='AlternateName', index=True, null=True)
    collectionmemberid = IntegerField(
        db_column='CollectionMemberID', index=True)
    collectionobjectid = ForeignKeyField(
        db_column='CollectionObjectID', rel_model=Collectionobject,
        to_field='collectionobjectid')
    confidence = CharField(db_column='Confidence', null=True)
    createdbyagentid = ForeignKeyField(
        db_column='CreatedByAgentID', null=True, rel_model=Agent,
        to_field='agentid')
    determinationid = PrimaryKeyField(db_column='DeterminationID')
    determineddate = DateField(
        db_column='DeterminedDate', index=True, null=True)
    determineddateprecision = IntegerField(
        db_column='DeterminedDatePrecision', null=True)
    determinerid = ForeignKeyField(
        db_column='DeterminerID', null=True, rel_model=Agent,
        related_name='agent_determinerid_set', to_field='agentid')
    featureorbasis = CharField(db_column='FeatureOrBasis', null=True)
    guid = CharField(db_column='GUID', index=True, null=True)
    iscurrent = BitField(db_column='IsCurrent')  # bit
    method = CharField(db_column='Method', null=True)
    modifiedbyagentid = ForeignKeyField(
        db_column='ModifiedByAgentID', null=True, rel_model=Agent,
        related_name='determination_modifiedbyagentid_set', to_field='agentid')
    nameusage = CharField(db_column='NameUsage', null=True)
    number1 = FloatField(db_column='Number1', null=True)
    number2 = FloatField(db_column='Number2', null=True)
    preferredtaxonid = ForeignKeyField(
        db_column='PreferredTaxonID', null=True, rel_model=Taxon,
        to_field='taxonid')
    qualifier = CharField(db_column='Qualifier', null=True)
    remarks = TextField(db_column='Remarks', null=True)
    subspqualifier = CharField(db_column='SubSpQualifier', null=True)
    taxonid = ForeignKeyField(
        db_column='TaxonID', null=True, rel_model=Taxon,
        related_name='taxon_taxonid_set', to_field='taxonid')
    text1 = TextField(db_column='Text1', null=True)
    text2 = TextField(db_column='Text2', null=True)
    timestampcreated = DateTimeField(db_column='TimestampCreated')
    timestampmodified = DateTimeField(db_column='TimestampModified', null=True)
    typestatusname = CharField(
        db_column='TypeStatusName', index=True, null=True)
    varqualifier = CharField(db_column='VarQualifier', null=True)
    version = IntegerField(db_column='Version', null=True)
    yesno1 = BitField(db_column='YesNo1', null=True)  # bit
    yesno2 = BitField(db_column='YesNo2', null=True)  # bit

    class Meta:
        db_table = 'determination'


DivisionProxy.initialize(Division)
TaxontreedefProxy.initialize(Taxontreedef)
TaxonProxy.initialize(Taxon)
