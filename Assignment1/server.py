from flask import Flask, request, make_response
from flask_restful import Resource, Api
from flask_api import status
from json import dumps, loads
from RFQ import RFQ
from RFP import RFP
from sqlalchemy import create_engine
from ProtoBufRFQ_pb2 import ProtoBufRFQ
from ProtoBufRFP_pb2 import ProtoBufRFP

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

        # Send response
        return json_rfp

class ProtoBufResponseForPrice(Resource):
    def post(self):

        # Create ProtoBuf
        protobuf_rfq = ProtoBufRFQ()
        protobuf_rfq.ParseFromString(request.data)

        # Deserialize Request for Quote
        rfq = RFQ(0,0,0,0,0)
        RFQ.protobuf_deserialize(rfq, protobuf_rfq)

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

        # Serialize Response for Price to Protobuf
        protobuf_rfp = ProtoBufRFP()
        protobuf_rfp = RFP.protobuf_serialize(rfp, protobuf_rfp)

        # Send response
        response = make_response(protobuf_rfp.SerializeToString())
        response.headers['Content-type'] = 'application/x-protobuf'
        return response

api.add_resource(JSONResponseForPrice, '/json_rfp')
api.add_resource(ProtoBufResponseForPrice, '/protobuf_rfp')

if __name__ == '__main__':
    server.run(host="127.0.0.1", port=80)