url = 'https://goldapple.ru/front/api/catalog/products'

method = 'POST'

payload = {"categoryId":1000000003,
        "cityId":"0c5b2444-70a0-4932-980c-b4dc0d3f02b5",
        "cityDistrict":"Чертаново Южное",
        "geoPolygons":["EKB-000000370","EKB-000000437"],
        "pageNumber":1,
        "filters":[{"currentMinValue":{"amount":22,
                                        "currency":"RUB",
                                        "denominator":1},
                                        "currentMaxValue":{"amount":4053,
                                                            "currency":"RUB",
                                                            "denominator":1},
                                                            "id":"63568a61bf461b4b2bde3b1a",
                                                            "type":"rangeType",
                                                            "name":"CalculatedPrices",
                                                            "key":"calculatedprices"}]
        }

headers = {
    "authority": "goldapple.ru",
    "method": "POST",
    "path": "/front/api/catalog/products",
    "scheme": "https",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,sr;q=0.6",
    "Content-Length": "431",
    "Content-Type": "application/json",
    "Dnt": "1",
    "Origin": "https://goldapple.ru",
    "Priority": "u=1, i",
    "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "Windows",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Traceparent": "00-628c1aba89abbf4f9ed3e98f8dbc4b27-e031d722f9ec4dab-01",
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
    "advcake_track_url": "%3D20240513FhwLWcynjPLLk5zkkI3nnNxFDcwK8HypbMb1J6pALhmjhgPO1wntuvPn6Mpbz4uZfXrA%2Bbp9mFm0Ma9JURTRXpRIXaC3VTMFz%2FMugQUBG3A64t%2FKoQhWaQvtnAJw3WtDHx91xzsPuthbFRh7FloEBzIeoTcjFGLPDzWk3Fp4cqLlPYPjB5dOryjUFuw96rwXVrs5YksbqrNCKUQb4LCyYiL2mzxAhQORaJylU67PBTdDLPzPDwGSQnWB%2BA1spfXVNJNarmvi4PCr7tywiX3YzipaNsyn%2FttvQCBXAAgCA5tsQg%2BTcu0CJV0nE4m5bqBVyi9SdxdLJvsylQxKqaniPrqNoZRcniN2UWJg23wTZPy8966eks3SUBIeiLbAsAyx2WlkkpdGAN28jfTZuNK8uhUR7d1NfcYLfxbTlLdHDOtRVC6arQ2Lpj292PQrvQp6ONZ4x2qvdhPyNkibXveph590YuBB%2BUKmwJ5IbzEM6JL3qzZ%2F2QHoxTk40hTHA1uVOqHwwZ58c87X5aUqsfuAgRWh3KiQD0vam9A4hG0MoNaJM7QPP9aynj4vAIXitbt1qK9DQnZifYpwwtOcozbe4juOZJ5R6Qn6%2BHpXsWBi%2FDgrjuBcUr0oNu2RCBvuUQ4rLAG9nWVPog2q2i5vWpjnLcw5r8nzUDckC%2Fz2Yfc62CiuwKa%2BhBAkWfo%3D",
    "section_data_ids": "%7B%22geolocation%22%3A1716744658%2C%22adult_goods%22%3A1716743640%2C%22cart%22%3A1716743641%7D"
}

