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


# db.connect()
# db.create_tables([Parcel, Account, LienAuction, RawPages])