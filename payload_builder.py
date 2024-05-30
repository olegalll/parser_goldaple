class PayloadBuilder:
    def __init__(self):
        self.payload = self._get_geo()
        # self.payload.update(func())
    
    def set_item(self, itemId: str):
        self.payload.update({'itemId': itemId})
        return self
    
    def set_category(self, categoryId: int):
        self.payload.update({'categoryId': categoryId})
        return self
    
    def set_page_number(self, page_number: int):
        self.payload.update({'pageNumber': page_number})
        return self
    
    def set_filters(self):      
        self.payload.update(self._get_filter())
        return self

    def get_payload(self):
        return self.payload

    # def func(self):
    #     self.payload.update(self._func())
    #     return self

    def _get_filter(self):
        return {
            "filters":[
                {
                    "currentMinValue":{
                        "amount":22,
                        "currency":"RUB",
                        "denominator":1
                    },
                    "currentMaxValue":{
                        "amount":4053,
                        "currency":"RUB",
                        "denominator":1
                    },
                    "id":"63568a61bf461b4b2bde3b1a",
                    "type":"rangeType",
                    "name":"CalculatedPrices",
                    "key":"calculatedprices"
                },
                {
                    "value": True,
                    "id":"63568bc7bf461b4b2bde3b23",
                    "type":"checkType",
                    "name":"StoreStocks",
                    "key":"storestocks"
                }
            ]
        }
    def _get_geo(self):
        return {
            "cityId":"0c5b2444-70a0-4932-980c-b4dc0d3f02b5",
            "cityDistrict":"Чертаново Южное",
            "geoPolygons":[
                "EKB-000000370",
                "EKB-000000437"
            ],
        }

    # def _func(self):
    #     return {key: value}


# payload = PayloadBuilder().set_item('19000003031').get_payload()
# payload = PayloadBuilder().set_category(1000000003).set_page_number(1).set_filters().get_payload()


{"itemId":"19000003031","cityId":"0c5b2444-70a0-4932-980c-b4dc0d3f02b5","cityDistrict":"Чертаново Южное","geoPolygons":["EKB-000000370","EKB-000000437"]}