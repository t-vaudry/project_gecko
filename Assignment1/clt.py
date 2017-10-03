from flask import Flask, render_template, request, make_response
from flask_bootstrap import Bootstrap
from flask_restful import Resource, Api
from json import dumps, loads
from string import Template
from RFQ import RFQ
from RFP import RFP
import http.client
from ProtoBufRFQ_pb2 import ProtoBufRFQ
from ProtoBufRFP_pb2 import ProtoBufRFP

clt = Flask(__name__)
Bootstrap(clt)
api = Api(clt)

#http_server = "ec2-52-26-40-230.us-west-2.compute.amazonaws.com"
http_server = "127.0.0.1:80"
conn = http.client.HTTPConnection(http_server)

class RequestForQuote(Resource):
    def get(self):
        return make_response(render_template("request.html"))

class JSONRequestForQuote(Resource):
    def post(self):
        # Create Request for Price from request form
        rfq = RFQ(request.form['rfqId'], request.form['acctId'], request.form['productNum'], request.form['productCat'], request.form['quantity'])

        # Serialize Request for Price
        json_rfq = dumps(rfq.json_serialize())

        # Headers
        headers = {'Content-type': 'application/json'}

        # Make request to server
        conn.request("POST", "/json_rfp", json_rfq, headers)

        # Get response
        try:
            response = conn.getresponse()
        except http.client.RemoteDisconnected:
            return make_response(render_template("error.html"))

        # Deserialize Response for Price
        rfp = RFP(0,0)
        RFP.json_deserialize(rfp, loads(loads(response.read())))

        # Return result on webpage
        return make_response(render_template("response.html", unitPrice=rfp.unitPrice, validation=rfp.validationPeriod))

class ProtoBufRequestForQuote(Resource):
    def post(self):
        # Create Request for Quote
        rfq = RFQ(request.form['rfqId'], request.form['acctId'], request.form['productNum'], request.form['productCat'], request.form['quantity'])

        # Serialize Request for Quote to Protobuf
        protobuf_rfq = ProtoBufRFQ()
        protobuf_rfq = RFQ.protobuf_serialize(rfq, protobuf_rfq)

        # Headers
        headers = {'Content-type': 'application/x-protobuf'}

        # Make request to server
        conn.request("POST", "/protobuf_rfp", protobuf_rfq.SerializeToString(), headers)

        # Get response
        try:
            response = conn.getresponse()
        except http.client.RemoteDisconnected:
            return make_response(render_template("error.html"))

        # Create ProtoBufRFP
        protobuf_rfp = ProtoBufRFP()
        protobuf_rfp.ParseFromString(response.read())

        # Deserialize Response for Price
        rfp = RFP(0,0)
        RFP.protobuf_deserialize(rfp, protobuf_rfp)

        # Return result on webpage
        return make_response(render_template("response.html", unitPrice=rfp.unitPrice, validation=rfp.validationPeriod))

api.add_resource(RequestForQuote, '/rfq')
api.add_resource(JSONRequestForQuote, '/json')
api.add_resource(ProtoBufRequestForQuote, '/protobuf')

if __name__ == '__main__':
     clt.run()
