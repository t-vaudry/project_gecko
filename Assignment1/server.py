from flask import Flask, request
from flask_restful import Resource, Api
from flask_api import status
from json import dumps, loads
from RFQ import RFQ
from RFP import RFP
from sqlalchemy import create_engine

server = Flask(__name__)
api = Api(server)

engine = create_engine('sqlite:///database.db')

class JSONResponseForPrice(Resource):
    def post(self):
        # Deserialize Request for Quote
        rfq = RFQ(0,0,0,0,0)
        RFQ.json_deserialize(rfq, loads(request.data))

        # Connect to database
        conn = engine.connect()

        # Query database for data
        query = conn.execute("select * from database where Number=? and Category=?", rfq.productNum, rfq.productCat)

        # Create Response for Price
        count = 0
        for row in query:
            count += 1
            rfp = RFP(row['Price'], row['Validation'])

        # No result
        if (count == 0):
            return 0, status.HTTP_404_NOT_FOUND

        # Serialize Response for Price
        json_rfp = dumps(rfp.json_serialize())
        return json_rfp

class ProtoBufResponseForPrice(Resource):
    def post(self):
        print(request.data)

api.add_resource(JSONResponseForPrice, '/json_rfp')
api.add_resource(ProtoBufResponseForPrice, '/proto_rfp')

if __name__ == '__main__':
    server.run(host="127.0.0.1", port=80)