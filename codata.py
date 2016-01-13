from flask import Flask, render_template, g, request
from db import DB, Parcel, Account, LienAuction
#from flask_table import Table, Col

#DB.connect()

app = Flask(__name__)

@app.before_request
def before_request():
    g.db = DB
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

# # Declare your table
# class ItemTable(Table):
#     name = Col('Name')
#     description = Col('Description')

@app.route('/')
def index():
    return "Hello World"

@app.route('/search')
def search():
    search_query = request.args.get('q')
    if search_query:
        entries = LienAuction.select().where(LienAuction.Tax_Year == search_query)
        #Parcel.get(Parcel.id == e.Parcel_ID).Parcel_ID
    else:
        entries = LienAuction.select().where(LienAuction.Tax_Year == 2014)
    # sample = [(s.Winning_Bid, s.Face_Value) for s in LienAuction.select().where(LienAuction.Tax_Year == 2014)]
    #entries = LienAuction.select().where(LienAuction.Tax_Year == 2014)
    #sample = [1,2,3,4,5]
    #return render_template('accounts.html', entries=entries, Parcel=Parcel)
    return "Hello World, search"

if __name__ == '__main__':
    #app.run()
    app.run(debug=True)

