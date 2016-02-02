from peewee import *
import datetime
# import pandas as pd

DB = SqliteDatabase('ColoradoPropertyData.db')

# DB = MySQLDatabase('heteroskedastic1$codata',
#                    user='heteroskedastic1',
#                    password='Ind5esh8cEv6dy5wOt4Oc4noW',
#                    host='heteroskedastic1.mysql.pythonanywhere-services.com')


##########################################################################################
#### Jeffco Field definitions
##########################################################################################
JeffMailMash= ('MAILSTRNBR', 'MAILSTRDIR', 'MAILSTRNAM', 'MAILSTRTYP', 'MAILSTRSFX', 'MAILSTRUNT', 'MAILCTYNAM', 'MAILSTENAM', 'MAILZIP5')
JeffPropMash = ('PRPSTRNUM', 'PRPSTRDIR', 'PRPSTRNAM', 'PRPSTRTYP', 'PRPSTRSFX', 'PRPSTRUNT', 'PRPCTYNAM', 'PRPSTENAM', 'PRPZIP5')
MailStFields = ('MAILSTRNBR', 'MAILSTRDIR', 'MAILSTRNAM', 'MAILSTRTYP', 'MAILSTRSFX')
PropStFields = ('PRPSTRNUM', 'PRPSTRDIR', 'PRPSTRNAM', 'PRPSTRTYP', 'PRPSTRSFX')
OwnerFields = ('OWNNAM', 'OWNNAM2', 'OWNNAM3', 'OWNICO', 'DBA')


def addresshasher(row, keys):
    """
    row: The row of data
    keys: The row columns to use
    usually this list in this order

    Jeffco
        ('MAILSTRNBR', 'MAILSTRDIR', 'MAILSTRNAM', 'MAILSTRTYP', 'MAILSTRSFX', 'MAILSTRUNT', 'MAILCTYNAM', 'MAILSTENAM', 'MAILZIP5')
        ('PRPSTRNUM', 'PRPSTRDIR', 'PRPSTRNAM', 'PRPSTRTYP', 'PRPSTRSFX', 'PRPSTRUNT', 'PRPCTYNAM', 'PRPSTENAM', 'PRPZIP5')
    """
    h = ''.join(row[a].upper().replace(' ', '') for a in keys if pd.notnull(row[a]))
    h = h.lstrip('0')
    return h

##########################################################################################
#### Define the DB
##########################################################################################

class BaseModel(Model):
    class Meta:
        database = DB


class Parcel(BaseModel):
    Parcel_ID = CharField(unique=True) # Schedule SCH im Jefferson county
    PARID = CharField(null=True)
    County = CharField(null=False)
    Timestamp = DateTimeField(default=datetime.datetime.now)
    class Meta:
        indexes = (
            # create a unique on from/to/date
            (('Parcel_ID', 'County'), True),)


class Account(BaseModel):
    Parcel_ID = ForeignKeyField(Parcel, related_name='Account')
    Tax_Year = IntegerField()
    Tax_Type = CharField()
    Effective_Date = DateField(null = True)
    Amount = FloatField()
    Balance = FloatField()
    Timestamp = DateTimeField(default=datetime.datetime.now)


class LienAuction(BaseModel):
    Parcel_ID = ForeignKeyField(Parcel, related_name='LienAuction')
    Face_Value = FloatField()
    Name = CharField()
    Tax_Year = IntegerField()
    Winning_Bid = FloatField()
    Timestamp = DateTimeField(default=datetime.datetime.now)

class Individuals(BaseModel):
    """
    This is a list of all owners
    Jeffco ASTP600 file:
        OWNNAM
        OWNNAM2
        OWNNAM3
        OWNICO
        DBA
    """
    Name = CharField() # First and last or company and DBA
    DBA = BooleanField(default=False)
    OWNICO = BooleanField(default=False)
    Other = CharField(default=None, null=True) # Maybe use for DBA flag, Care of flag...
    Timestamp = DateTimeField(default=datetime.datetime.now)

class PropertieAddresses(BaseModel):
    """
    This is the list of all propertie addresses
    """


class Owners(BaseModel):
    """
    This links owners with properties
    """
    Parcel_ID = ForeignKeyField(Parcel, related_name='The_Owners')
    Owner = ForeignKeyField(Individuals, related_name='The_Owners')
    Timestamp = DateTimeField(default=datetime.datetime.now)

class Addresses(BaseModel):
    """
    All addresses, owner (mailing) and property
    """
    Parcel_ID = ForeignKeyField(Parcel, related_name='The_Address', null=True)
    Property = BooleanField(default=False)
    Mailing = BooleanField(default = False)
    IdHash = CharField(unique=True)
    Street1 = CharField(default=None, null=True)
    Street2 = CharField(default=None, null=True)
    City = CharField(default=None, null=True)
    State = CharField(default=None, null=True)
    Zipcode = IntegerField(default=None, null=True)
    Zip4 = IntegerField(default=None, null=True)
    Timestamp = DateTimeField(default=datetime.datetime.now)

class OwnerAddresses(BaseModel):
    """
    All Owner (Mailing) Addresses
    """
    Owners = ForeignKeyField(Individuals, related_name='Owners_address')
    Address = ForeignKeyField(Addresses, related_name='Address')
    Timestamp = DateTimeField(default=datetime.datetime.now)

##########################################################################################
#### Usefull data info
##########################################################################################

JeffersonMailAddrDef = {'MAILSTRNBR': 'MAILING STREET ADDRESS NUMBER',
                           'MAILSTRDIR': 'MAILING STREET ADDRESS DIRECTION',
                           'MAILSTRNAM': 'MAILING STREET ADDRESS NAME',
                           'MAILSTRTYP': 'MAILING STREET ADDRESS TYPE',
                           'MAILSTRSFX': 'MAILING STREET ADDRESS SUFFIX',
                           'MAILSTRUNT': 'MAILING STREET ADDRESS UNIT',
                           'MAILCTYNAM': 'MAILING CITY NAME',
                           'MAILSTENAM': 'MAILING STATE NAME',
                           'MAILZIP5': 'MAILING ADDRESS ZIP CODE 5',
                           'MAILZIP4': 'MAILING ADDRESS ZIP CODE 4'}

JeffersonPropAddrDef = {'PRPSTRNUM': 'PROPERTY STREET ADDRESS NUMBER',
                                'PRPSTRDIR': 'PROPERTY STREET ADDRESS DIRECTION',
                                'PRPSTRNAM': 'PROPERTY STREET ADDRESS NAME',
                                'PRPSTRTYP': 'PROPERTY STREET ADDRESS TYPE',
                                'PRPSTRSFX': 'PROPERTY STREET ADDRESS SUFFIX',
                                'PRPSTRUNT': 'PROPERTY STREET ADDRESS UNIT',
                                'PRPCTYNAM': 'PROPERTY CITY NAME',
                                'PRPSTENAM': 'PROPERTY STATE NAME',
                                'PRPZIP5': 'PROPERTY ZIP CODE 5',
                                'PRPZIP4': 'PROPERTY ZIP CODE 4'}

# db.connect()
# db.create_tables([Parcel, Account, LienAuction, RawPages])