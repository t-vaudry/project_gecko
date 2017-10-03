class RFP:
    def __init__(self, unitPrice, validationPeriod):
        self.unitPrice = unitPrice
        self.validationPeriod = validationPeriod

    def json_serialize(self):
        return {
            'unitPrice': self.unitPrice,
            'validationPeriod': self.validationPeriod
        }

    def protobuf_serialize(self, obj):
        obj.unitPrice = self.unitPrice
        obj.validationPeriod = self.validationPeriod
        return obj

    def json_deserialize(self, obj):
        self.unitPrice = obj['unitPrice']
        self.validationPeriod = obj['validationPeriod']

    def protobuf_deserialize(self, obj):
        self.unitPrice = obj.unitPrice
        self.validationPeriod = obj.validationPeriod