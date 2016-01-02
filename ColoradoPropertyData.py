from flask import Flask, render_template, g
from db import DB, Parcel, Account, LienAuction
from flask_table import Table, Col

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
def hello_world():
    # sample = [(s.Winning_Bid, s.Face_Value) for s in LienAuction.select().where(LienAuction.Tax_Year == 2014)]
    entries = LienAuction.select().where(LienAuction.Tax_Year == 2014)
    #sample = [1,2,3,4,5]
    return render_template('base.html', entries=entries)

if __name__ == '__main__':
    app.run()
