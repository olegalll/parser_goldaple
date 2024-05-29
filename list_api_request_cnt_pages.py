url = 'https://goldapple.ru/front/api/catalog/filters'

method = 'POST'

payload_products = {
    "categoryId":1000000003,
    "cityId":"0c5b2444-70a0-4932-980c-b4dc0d3f02b5",
    "cityDistrict":"Чертаново Южное",
    "geoPolygons":[
        "EKB-000000370",
        "EKB-000000437"
    ],
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
            "value":'true',
            "id":"63568bc7bf461b4b2bde3b23",
            "type":"checkType",
            "name":"StoreStocks",
            "key":"storestocks"
        }
    ]
    }



headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru-RU, ru;q=0.9, en-US;q=0.8, en;q=0.7, sr;q=0.6",
    "Content-Length": "416",
    "Content-Type": "application/json",
    "Dnt": "1",
    "Origin": "https://goldapple.ru",
    "Priority": "u=1, i",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Traceparent": "00-f44fb61ebff866f529306bf8897a9744-80072897f7f9b354-01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

cookies = {
    "ga-lang": "ru",
    "client-store-code": "default",
    "PHPSESSID": "c79b40b97a134fe50ce2b87c0a7eff95",
    "advcake_track_id": "3b9c1bcd-964d-c0f6-c923-d1dd75380e9b",
    "advcake_session_id": "25ce8150-b6fc-c7df-738b-7dd39ec43a4b",
    "isAddressConfirmed": "true",
    "mage-cache-sessid": "true",
    "ga-plp-simple-layout": "true",
    "digi-analytics-sessionId": "O8Cn_DME7YdtQbya36yyl",
    "advcake_track_url": "%3D20240513YyNVibjMU4K2HpCAvnMMqIYDvxVGf5ZSwEAiie58cWH22Cn48DVLauzd07yiXqBHcpqKgmurLLtfofjjoVYjLIwb%2FIDv%2FwzriqsESq9tDybSPPSDb4F6jqVFbzabY9WjU1O%2Bn8b0ZCPhy7g5cT9uw%2F2aMdhVjM0Mkj1W%2BnvRBswuF8ajBllcyCQjADOTORsPd4HmRKWCtVYcu%2FwAaz99t28LAdfkxUQ4mkTQZOtRvENDeYAlBEsFZHHaEINM3ZpXfrIsIcMO%2FFynR2%2FrLeLK8PsGpOJ3AuFCyniFdwd13BEjdCsDQfWLgcIzOErWrss4vwq7JBFsHgCSiCalni6g%2FXJhD6cd1z41zjWa21LkE4wQrorkirV88%2BfRaDnXNTlIg9kxfZHphM4RJfbFoEDdKRcZ%2F2MtRCx4qx%2BFiMyRYAl18ALWBs9eKnCDhw5Ewn75mSnyQpE%2B0dfSyy0DSVUbWdsvd9WN19BUf%2B3DKFrqN3Tbqx0IRNSFk%2FesJ7UeTvlmmR7WjaXzIqQIxwE7sZ1Q9mBJB%2BcbmG7pwsuLXn%2BTzuzK%2BCkJA3RgCmw4vMpWKURtSCH1emLlt1dU5cuHva8baEpDuUvtGi%2F7hqTEpfxTWgOzPJil58eW8o0Ksthfn7fyDlVNZKqxUyjnlLcHN%2BmCy2VHMCZVmvPY39VaEthkYsPhCv6G3V1Zpk0%3D",
    "section_data_ids": "%7B%22geolocation%22%3A1716745375%2C%22adult_goods%22%3A1716745374%2C%22cart%22%3A1716745374%7D"
}
