from flask import Flask, render_template, request, make_response
from flask_bootstrap import Bootstrap
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from RFQ import RFQ
from RFP import RFP

engine = create_engine('sqlite:///database.db')

app = Flask(__name__)
Bootstrap(app)
api = Api(app)

class RequestForQuote(Resource):
    def post(self):
        rfq = RFQ(request.form['rfqId'], request.form['acctId'], request.form['productNum'], request.form['productCat'], request.form['quantity'])
        # serialize rfq?
        # send to server
        # get response

    def get(self):
        return make_response(render_template("request.html"))

api.add_resource(RequestForQuote, '/rfq')

if __name__ == '__main__':
     app.run()
