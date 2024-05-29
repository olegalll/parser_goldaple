import requests
import json


class RequestWrapper:
    def __init__(self, payload):
        self.payload = payload


    def post_options(self, url):
        self._post(url, self.payload, self._get_headers('options'), self._get_cookies('options'))

    def post_filters(self, url):
        self._post(url, self.payload, self._get_headers('filters'), self._get_cookies('filters'))
    
    def post_item(self, url):
        self._post(url, self.payload, self._get_headers('item'), self._get_cookies('item'))

    def _post(self, url, payload, headers, cookies):
        r = requests.post(url, headers=headers, cookies=cookies, json=payload)
        return r.json()


    def _get_headers(self, type):
        headers_options = {
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
        headers_filters = {
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
        
        if type == 'options':
            return headers_options
        if type == 'filters':
            return headers_filters
        raise Exception('Invalid header type')
    
    def _get_cookies(self, type):
        cookies_options = {
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
        cookies_filters = {
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

        if type == 'options':
            return cookies_options
        if type == 'filters':
            return cookies_filters

        raise Exception('Invalid cookies type')
    
