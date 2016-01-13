import pandas as pd
import numpy as np
from csv import DictReader
from db import Parcel, addresshasher, JeffMailMash, JeffPropMash, MailStFields, PropStFields, OwnerFields


#
def JEFFCO(datafile):
    """
    2013: data/JeffersonCo/JeffcoData Nov 2013/CLEANED_ATSDTA_ATSP600.csv
    2014:
    """
    return pd.read_csv(datafile, na_values=['nan', ''], index_col=False, low_memory=False)

def GRANDCO(datafile):
    """
    data/GrandCo/All_Account_Details.csv
    """
    pd.read_csv(datafile, na_values=['nan', ''], index_col=False)


def grandco_parcels():
    from db import Parcel
    try:
        Parcel.create_table()
    except:
        pass
    results = pd.read_csv('data/GrandCo/All_Properties.csv')
    count = 0
    for p in results.Parcel_ID.unique():
        prop = Parcel.create(Parcel_ID=p, County='Grand')
        count += 1
    print('Imported {} Parcels'.format(count))


def grandco_auction():
    """
    Loads auction result data for grand county
    :param parceltable:
    :param lienauction:
    :return:
    """
    from db import LienAuction, Parcel
    try:
        LienAuction.create_table()
    except:
        pass

    dataframe = pd.read_csv('data/GrandCo/All_Results.csv')
    count = 0
    for p in dataframe.iterrows():
        data = p[1]
        try:
            prop = Parcel.get(Parcel.Parcel_ID == data.Parcel_ID and Parcel.County == 'Grand')
        except Exception as e:
            if 'Instance matching query does not exist' in str(e):
                prop = Parcel.create(Parcel_ID=data.Parcel_ID)
            else:
                print('The problem is {}'.format(data.Parcel_ID))
                print(e)

        LienAuction.create(Parcel_ID=prop,
                           Bidder_ID=data.Bidder_ID,
                           Face_Value=data.Face_Value,
                           Name=data.Name,
                           Tax_Year=data.Tax_Year,
                           Winning_Bid=data.Winning_Bid)
        count += 1
    print('Imported {} auction results'.format(count))


def grandco_account(parceltable, accounttable, dataframe):
    """
    Loads tresury account detail for each property
    :param parceltable:
    :param accounttable:
    :return:
    """
    count = 0
    for row in dataframe.iterrows():
        data = row[1]
        prop = parceltable.get(parceltable.Parcel_ID == data.Parcel_ID)
        accounttable.create(Parcel_ID=prop,
                            Tax_Year=data.Tax_Year,
                            Tax_Type=data.Tax_Type,
                            Effective_Date=data.Effective_Date,
                            Amount=data.Amount,
                            Balance=data.Balance)
        count += 1
    print('Imported {} account details'.format(count))


def jeffco_600_Parcels(dataframe):
    """
    Jeffco ASTP600 file:
        SCH: SCHEDULE NUMBER
    """
    from db import Parcel
    try:
        Parcel.create_table()
    except:
        pass
    # "data/JeffersonCo/JeffcoData Nov 2013/CLEANED_ATSDTA_ATSP600.csv"
    dataframe['SCH'] = pd.to_numeric(dataframe['SCH'], errors='coerce')
    count = 0
    for p in dataframe.SCH.unique():
        prop = Parcel.create(Parcel_ID=p, County='Jefferson')
        count += 1
    print('Imported {} Jefferson Parcels'.format(count))


def jeffco_600_Individuals(dataframe):
    """
    Jeffco ASTP600 file:
        OWNNAM
        OWNNAM2
        OWNNAM3
        OWNICO
        DBA
    """
    from db import Individuals
    try:
        Individuals.create_table()
    except:
        pass
    ownerfields = ['OWNNAM', 'OWNNAM2', 'OWNNAM3', 'OWNICO', 'DBA']
    all_owners = set()
    for o in ownerfields:
        all_owners |= set(dataframe[o][(dataframe[o].notnull())])
    careofnames = set(dataframe['OWNICO'][(dataframe['OWNICO'].notnull())])
    dba = set(dataframe['DBA'][(dataframe['DBA'].notnull())])
    count = 0
    careofnames = set(x.replace('%', '').strip() for x in careofnames)
    dba = set(x.replace('%', '').strip() for x in dba)

    print('ABEL RICHARD A' in all_owners)

    for i in all_owners:
        i.replace('%', '')
        i = i.strip()
        OWNICO = i in careofnames
        DBA = i in dba
        ind = Individuals.create(Name=i, OWNICO=OWNICO, DBA=DBA)
        count += 1
    print('Added {} owners'.format(count))

def Jeffco_600_owners(dataframe):
    """
    Connect owners with property
    :param parceltable:
    :param indvtable:
    :param owntable:
    :param datafile:
    :return:
    """
    from db import Parcel, Individuals, Owners
    try:
        Owners.create_table()
    except:
        pass
    ownerfields = ['OWNNAM', 'OWNNAM2', 'OWNNAM3', 'OWNICO', 'DBA']
    for row in dataframe.iterrows():
        row = row[1]
        print(int(row['SCH']))
        prop = Parcel.get(Parcel.Parcel_ID == int(row['SCH']))
        for i in (row[o] for o in ownerfields):
            if str(i) != 'nan':
                indv = Individuals.get(Individuals.Name == i)
                Owners.create(Owner=indv, Parcel_ID=prop)

def jeffco_600_Addresses(dataframe):
    """
    connect individuals to properties
    :param ownerstable:
    :param datafile:
    :return:
    Jeffco 600
        'MAILSTRNBR': 'MAILING STREET ADDRESS NUMBER'
        'MAILSTRDIR': 'MAILING STREET ADDRESS DIRECTION'
        'MAILSTRNAM': 'MAILING STREET ADDRESS NAME'
        'MAILSTRTYP': 'MAILING STREET ADDRESS TYPE'
        'MAILSTRSFX': 'MAILING STREET ADDRESS SUFFIX'
        'MAILSTRUNT': 'MAILING STREET ADDRESS UNIT'
        'MAILCTYNAM': 'MAILING CITY NAME'
        'MAILSTENAM': 'MAILING STATE NAME'
        'MAILZIP5': 'MAILING ADDRESS ZIP CODE 5'
        'MAILZIP4': 'MAILING ADDRESS ZIP CODE 4'

        'PRPSTRNUM': 'PROPERTY STREET ADDRESS NUMBER'
        'PRPSTRDIR': 'PROPERTY STREET ADDRESS DIRECTION'
        'PRPSTRNAM': 'PROPERTY STREET ADDRESS NAME'
        'PRPSTRTYP': 'PROPERTY STREET ADDRESS TYPE'
        'PRPSTRSFX': 'PROPERTY STREET ADDRESS SUFFIX'
        'PRPSTRUNT': 'PROPERTY STREET ADDRESS UNIT'
        'PRPCTYNAM': 'PROPERTY CITY NAME'
        'PRPSTENAM': 'PROPERTY STATE NAME'
        'PRPZIP5': 'PROPERTY ZIP CODE 5'
        'PRPZIP4': 'PROPERTY ZIP CODE 4'
    """
    from db import Addresses
    try:
        Addresses.create_table()
    except:
        pass
    #dataframe['MAILSTRNBR'] = pd.to_numeric(dataframe['MAILSTRNBR'], errors='coerce')
    #dataframe['PRPSTRNUM'] = pd.to_numeric(dataframe['PRPSTRNUM'], errors='coerce')
    for r in dataframe.iterrows():
        r = r[1]
        street1 = ' '.join(str(r[a]) for a in MailStFields if pd.notnull(r[a]))
        idhashmail = addresshasher(r, JeffMailMash)
        idhashprop = addresshasher(r, JeffPropMash)
        try:
            addr = Addresses.create(Street1=street1.lstrip('0'),
                                       Street2= r['MAILSTRUNT'],
                                       City=r['MAILCTYNAM'],
                                       State=r['MAILSTENAM'],
                                       Zipcode=r['MAILZIP5'],
                                       Zip4=r['MAILZIP4'],
                                       IdHash=idhashmail,
                                       Mailing=True)
            if idhashmail == idhashprop:
                # TODO: need to update exsiting addresses.
                addr.Property = True
                addr.save()
            else:
                street1 = ' '.join(str(r[a]) for a in PropStFields if pd.notnull(r[a]))
                Addresses.create(street1=street1.lstrip('0'),
                                    street2=r['PRPSTRUNT'],
                                    City=r['PRPCTYNAM'],
                                    State=r['PRPSTENAM'],
                                    Zipcode=r['PRPZIP5'],
                                    Zip4=r['PRPZIP4'],
                                    IdHash=idhashprop,
                                    Property=True)
        except Exception as e:
            if 'UNIQUE constraint failed: addresses.IdHash' not in str(e):
                print(e)
                raise
