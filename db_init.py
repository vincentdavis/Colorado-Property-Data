import os
from db import DB, Parcel, Account, LienAuction
from dataloaders import load_grandco_data

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
        load_grandco_data(Parcel, LienAuction)