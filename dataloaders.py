import pandas as pd
from db import DB, Parcel, Account, LienAuction, County


def grandco_parcels(parceltable, countytable):
    results = pd.read_csv('data/GrandCo/All_Properties.csv')
    count = 0
    for p in results.Parcel_ID.unique():
        prop = parceltable.create(Parcel_ID=p)
        countytable(Parcel_ID=prop, Co_Name='Grand')
        count += 1
    print('Imported {} Parcels'.format(count))


def grandco_auction(parceltable, lienauction):
    """
    Loads auction result data for grand county
    :param parceltable:
    :param lienauction:
    :return:
    """
    results = pd.read_csv('data/GrandCo/All_Results.csv')
    count = 0
    for p in results.iterrows():
        data = p[1]
        try:
            prop = parceltable.get(parceltable.Parcel_ID == data.Parcel_ID)
        except Exception as e:
            if 'Instance matching query does not exist' in str(e):
                prop = parceltable.create(Parcel_ID=data.Parcel_ID)
            else:
                print('The problem is {}'.format(data.Parcel_ID))
                print(e)

        lienauction.create(Parcel_ID=prop,
                           Bidder_ID=data.Bidder_ID,
                           Face_Value=data.Face_Value,
                           Name=data.Name,
                           Tax_Year=data.Tax_Year,
                           Winning_Bid=data.Winning_Bid)
        count += 1
    print('Imported {} auction results'.format(count))


def grandco_account(parceltable, accounttable):
    """
    Loads tresury account detail for each property
    :param parceltable:
    :param accounttable:
    :return:
    """
    detail = pd.read_csv('data/GrandCo/All_Account_Details.csv', index_col=False)
    count = 0
    for row in detail.iterrows():
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

def jeffco_600_Parcels(parceltable, countytable, datafile):
    """
    Jeffco ASTP600 file:
        OWNNAM
        OWNNAM2
        OWNNAM3
        OWNICO
        DBA
    """
    # "data/JeffersonCo/JeffcoData Nov 2013/ATSDTA_ATSP600.txt"
    jeffco = pd.read_csv(datafile, index_col=False)
    count = 0
    for p in jeffco.SCH.unique():
        prop = parceltable.create(Parcel_ID=p)
        countytable(Parcel_ID=prop, Co_Name='Jefferson')
        count += 1
    print('Imported {} Jefferson Parcels'.format(count))

def jeffco_600_Owners():
    """
    Jeffco ASTP600 file:
        OWNNAM
        OWNNAM2
        OWNNAM3
        OWNICO
        DBA
    """
    owners = pd.read_csv("data/JeffersonCo/JeffcoData Nov 2013/ATSDTA_ATSP600.txt", index_col=False)
    count = 0
    for row in detail.iterrows():
        data = row[1]


