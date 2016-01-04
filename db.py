from peewee import *
import datetime

DB = SqliteDatabase('ColoradoPropertyData.db')

class BaseModel(Model):
    class Meta:
        database = DB


class Parcel(BaseModel):
    Parcel_ID = CharField(unique=True)
    Timestamp = DateTimeField(default=datetime.datetime.now)


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

class County(BaseModel):
    Parcel_ID = ForeignKeyField(Parcel, related_name='County')
    Co_Name = CharField()

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
    Other = CharField() # Maybe use for DBA flag, Care of flag...


class PropertieAddresses(BaseModel):
    """
    This is the list of all propertie addresses
    """

class OwnerAddresses(BaseModel):
    """
    All Owner (Mailing) Addresses
    """

class Owners(BaseModel):
    """
    This links owners with properties
    """
    Parcel_ID = ForeignKeyField(Parcel, related_name='The_Owners')
    Owners = ForeignKeyField(Individuals, related_name='The_Owners')


# db.connect()
# db.create_tables([Parcel, Account, LienAuction, RawPages])