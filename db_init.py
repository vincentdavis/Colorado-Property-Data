import os
from db import DB, Parcel, Account, LienAuction, County
from dataloaders import grandco_auction, grandco_account, grandco_parcels

def DB_INIT(remove=False, loaddata=False):
    """
    Nothing will happen with remove and loaddata set to false
    :param remove: Remove exisiting database
    :param loaddata: load data, into database, empty or not.
    :return: nothing
    """
    if remove:
        try:
            os.remove('ColoradoPropertyData.db')
        except:
            pass
        DB.connect()
        DB.create_tables([Parcel, Account, LienAuction])
    if loaddata:
        # TODO Need to have more generic data loader
        grandco_parcels(Parcel, County)
        grandco_auction(Parcel, LienAuction)
        grandco_account(Parcel, Account)