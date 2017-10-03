class RFQ:
    def __init__(self, rfqId, acctId, productNum, productCat, quantity):
        self.rfqId = rfqId
        self.acctId = acctId
        self.productNum = productNum
        self.productCat = productCat
        self.quantity = quantity

    def json_serialize(self):
        return {
            'rfqId': self.rfqId,
            'acctId': self.acctId,
            'productNum': self.productNum,
            'productCat': self.productCat,
            'quantity': self.quantity
        }

    def protobuf_serialize(self, obj):
        obj.rfqId = self.rfqId
        obj.acctId = self.acctId
        obj.productNum = self.productNum
        obj.productCat = self.productCat
        obj.quantity = self.quantity
        return obj

    def json_deserialize(self, obj):
        self.rfqId = obj['rfqId']
        self.acctId = obj['acctId']
        self.productNum = obj['productNum']
        self.productCat = obj['productCat']
        self.quantity = obj['quantity']

    def protobuf_deserialize(self, obj):
        self.rfqId = obj.rfqId
        self.acctId = obj.acctId
        self.productNum = obj.productNum
        self.productCat = obj.productCat
        self.quantity = obj.quantity