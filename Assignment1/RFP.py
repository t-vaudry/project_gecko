class RFP:
    def __init__(self, unitPrice, validationPeriod):
        self.unitPrice = unitPrice
        self.validationPeriod = validationPeriod

    def json_serialize(self):
        return {
            'unitPrice': self.unitPrice,
            'validationPeriod': self.validationPeriod
        }

    def json_deserialize(self, obj):
        self.unitPrice = obj['unitPrice']
        self.validationPeriod = obj['validationPeriod']