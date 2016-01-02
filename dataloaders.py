import pandas as pd

def load_grandco_data(parceltable, lienauction):
    results = pd.read_csv('data/All_Results.csv')
    for p in results.Parcel_ID.unique():
        parceltable(Parcel_ID=p).save()

    for p in results.iterrows():
        data = p[1]
        print(data)
        prop = parceltable.select().where(parceltable.Parcel_ID == data.Parcel_ID).get()
        lienauction(Parcel_ID=prop,
                    Bidder_ID=data.Bidder_ID,
                    Face_Value=data.Face_Value,
                    Name=data.Name,
                    Tax_Year=data.Tax_Year,
                    Winning_Bid=data.Winning_Bid).save()