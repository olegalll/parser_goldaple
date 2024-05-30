import requests
import json


class RequestWrapper:
    def __init__(self, payload):
        self.payload = payload


    def post_options(self):
        return self._post(self.payload,self._get_url('options'), self._get_headers('options'), self._get_cookies('options'))

    def post_filters(self):
        return self._post(self.payload,self._get_url('filters'), self._get_headers('filters'), self._get_cookies('filters'))
    
    def post_item(self):
        return self._post(self.payload,self._get_url('item'), self._get_headers('item'), self._get_cookies('item'))

    def _post(self, payload, url, headers, cookies):
        r = requests.post(url, headers=headers, cookies=cookies, json=payload)
        json = r.json()
        return json


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
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,sr;q=0.6',
            'content-type': 'application/json',
            # 'cookie': 'ga-lang=ru; client-store-code=default; advcake_track_id=3b9c1bcd-964d-c0f6-c923-d1dd75380e9b; advcake_session_id=25ce8150-b6fc-c7df-738b-7dd39ec43a4b; isAddressConfirmed=true; ga-plp-simple-layout=true; MCS_SESSID=uordlF1yBkAi1ddC%2BUQrf2HrNBoe7Iun; digi-analytics-sessionId=D-sdVxymcRy1AuZhwgW3a; advcake_track_url=%3D202405278vfaUWQkREQ0q9PIYJI1aON9J2FYforo5%2FX8k7pe4ry8imPXxKsHBP87zQvjhFnBjuBU%2Ft2sUt8PFtStdQ88O9vhDIToti3HhpJlTxmhUa9aUZri03Ad%2FjpVfC3N2gFUNnPZn49YZG3IpGfaaFsaUsRVzFoCtuxBMMol3MyCkLe7fZE0Pl50aTgCqEx3d4jkv6xVpCVhLqrDJbDgDizBpe%2BuOogOU%2BDfEALPQtXAU8GZ6Lf0a%2FkQJdzQzwz4WOyCW8hyLgysd8XVO%2FOg42l7Os89xB0f1lNUy05Qk9ES1QlK8QuOqvH%2FkXVUTg0T7R0M686Dh8K5Illbx0bDxeTjTk0K9xZ1vfORDQKwr%2Fiwx%2Fsifo%2FaE5XENRWmI2HMbjdM4QjC9iJbAGXAoiixuZ7JbGyXrQj8hogBhk0hNKLiPtEMn4Zm%2BlIcBMPAjvwAWPm83rLmmDzgY8t%2BUfrva0SFrzmAP5DlHntAzgFy%2BOJ%2F%2Fu%2BnXKAOnZUbjQqx%2FzNMchZfTyTgvdMKLZeVVQTGIaZemUYQNpF9nzs6XZWsq%2BGSi%2FDzGr6o72Dfz9ilod6ugfuWKA15AIV%2F6ZRMN%2FmoLKmuDSIMBbQFKRgjcHVCBTQsKGSxRQlxeMYPJrmq9hJtuFLjdWzvJwu9fWqQ4%2FMwRzHoJ574tVvtBW1BdMbxPAoYc%2Fqtf9oBspXLv4Q%3D; section_data_ids=%7B%22geolocation%22%3A1717067288%2C%22adult_goods%22%3A1717067288%2C%22cart%22%3A1717067288%7D',
            'dnt': '1',
            'origin': 'https://goldapple.ru',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'traceparent': '00-636901ea7c1986923d732ded94d91548-05b718d65814c03d-01',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        }
        headers_item = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,sr;q=0.6',
    'content-type': 'application/json',
    # 'cookie': 'ga-lang=ru; client-store-code=default; advcake_track_id=3b9c1bcd-964d-c0f6-c923-d1dd75380e9b; advcake_session_id=25ce8150-b6fc-c7df-738b-7dd39ec43a4b; isAddressConfirmed=true; ga-plp-simple-layout=true; MCS_SESSID=uordlF1yBkAi1ddC%2BUQrf2HrNBoe7Iun; digi-analytics-sessionId=GRell03nwpTBEeyWvZz0U; advcake_track_url=%3D20240527KYABHOLVS76YOouFI0h%2FDkUDu9KBfjd%2FHukzrTo5tT0N5fA3twXkhIfrUCnID7lr1iBxRpkdaxCLcDUbXLwM5tMl%2BeapmgEbFFEJPPYaqafrxPvLtwMxoYrK0tTW5iyANmol3sXBBcdZzUKwi3Tsx1yj9pJnJh%2F39kKbsZ1O5FNnB5md9QE3VCaILuch2z5483lUcIgj452ks1VZFQto7%2BUwGwcNYN96pyt%2BbjJ%2FWZv5zGCABcmI02MQ%2Fp2qOuBaj8ZfxikmlPoSGZofQ5lHGMgNOlYWUTwcEd9VTJA3uuVvX3cHp%2Fsbkg1GHIXyX%2FSIngi58G9CA%2F6wUDKQIQ43eA1XZzoDLQeJGDUjZ9tIvHMW2oXx%2F%2BKsQx6W70xnDCAxt66ufnn5MTewulTLW7AZxr9WRO4SkZX9O2UWsMUsWkNmWrh%2BjFE4DrYJMOhvAVMOjNEqtT9zW2TYiHr4XVdT6iew3elnf4MxSD2jzb2nPsv8ZJs%2BXcfRaBgWZHFg1%2FymBfhYepZO3d3o6kCmMFB8rK4MK2xvtZ47102%2F71mip5DzEd2gr1moWrMiJkA19PKLfZhjeMSrwNJVseCjw9km%2FTli2MSEST%2F1qJNd02g%2BgqP2KPUUr6FWuQc7T9A%2Fgo7Y7s4%2F%2BjWxsrNDxF4Y5diSwFeY8H8m58RKdUAVl%2BJZjg4z6h5xqcYeHlk%3D; section_data_ids=%7B%22geolocation%22%3A1717057373%2C%22adult_goods%22%3A1717057372%2C%22cart%22%3A1717057342%7D',
    'dnt': '1',
    'origin': 'https://goldapple.ru',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-33615149598bfac910ca6aa41f0acb40-5748feca47340924-01',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        }

        if type == 'options':
            return headers_options
        if type == 'filters':
            return headers_filters
        if type == 'item':
            return headers_item
        
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
            'ga-lang': 'ru',
            'client-store-code': 'default',
            'advcake_track_id': '3b9c1bcd-964d-c0f6-c923-d1dd75380e9b',
            'advcake_session_id': '25ce8150-b6fc-c7df-738b-7dd39ec43a4b',
            'isAddressConfirmed': 'true',
            'ga-plp-simple-layout': 'true',
            'MCS_SESSID': 'uordlF1yBkAi1ddC%2BUQrf2HrNBoe7Iun',
            'digi-analytics-sessionId': 'D-sdVxymcRy1AuZhwgW3a',
            'advcake_track_url': '%3D202405278vfaUWQkREQ0q9PIYJI1aON9J2FYforo5%2FX8k7pe4ry8imPXxKsHBP87zQvjhFnBjuBU%2Ft2sUt8PFtStdQ88O9vhDIToti3HhpJlTxmhUa9aUZri03Ad%2FjpVfC3N2gFUNnPZn49YZG3IpGfaaFsaUsRVzFoCtuxBMMol3MyCkLe7fZE0Pl50aTgCqEx3d4jkv6xVpCVhLqrDJbDgDizBpe%2BuOogOU%2BDfEALPQtXAU8GZ6Lf0a%2FkQJdzQzwz4WOyCW8hyLgysd8XVO%2FOg42l7Os89xB0f1lNUy05Qk9ES1QlK8QuOqvH%2FkXVUTg0T7R0M686Dh8K5Illbx0bDxeTjTk0K9xZ1vfORDQKwr%2Fiwx%2Fsifo%2FaE5XENRWmI2HMbjdM4QjC9iJbAGXAoiixuZ7JbGyXrQj8hogBhk0hNKLiPtEMn4Zm%2BlIcBMPAjvwAWPm83rLmmDzgY8t%2BUfrva0SFrzmAP5DlHntAzgFy%2BOJ%2F%2Fu%2BnXKAOnZUbjQqx%2FzNMchZfTyTgvdMKLZeVVQTGIaZemUYQNpF9nzs6XZWsq%2BGSi%2FDzGr6o72Dfz9ilod6ugfuWKA15AIV%2F6ZRMN%2FmoLKmuDSIMBbQFKRgjcHVCBTQsKGSxRQlxeMYPJrmq9hJtuFLjdWzvJwu9fWqQ4%2FMwRzHoJ574tVvtBW1BdMbxPAoYc%2Fqtf9oBspXLv4Q%3D',
            'section_data_ids': '%7B%22geolocation%22%3A1717067288%2C%22adult_goods%22%3A1717067288%2C%22cart%22%3A1717067288%7D',
        }
        cookies_item = {
    'ga-lang': 'ru',
    'client-store-code': 'default',
    'advcake_track_id': '3b9c1bcd-964d-c0f6-c923-d1dd75380e9b',
    'advcake_session_id': '25ce8150-b6fc-c7df-738b-7dd39ec43a4b',
    'isAddressConfirmed': 'true',
    'ga-plp-simple-layout': 'true',
    'MCS_SESSID': 'uordlF1yBkAi1ddC%2BUQrf2HrNBoe7Iun',
    'digi-analytics-sessionId': 'GRell03nwpTBEeyWvZz0U',
    'advcake_track_url': '%3D20240527KYABHOLVS76YOouFI0h%2FDkUDu9KBfjd%2FHukzrTo5tT0N5fA3twXkhIfrUCnID7lr1iBxRpkdaxCLcDUbXLwM5tMl%2BeapmgEbFFEJPPYaqafrxPvLtwMxoYrK0tTW5iyANmol3sXBBcdZzUKwi3Tsx1yj9pJnJh%2F39kKbsZ1O5FNnB5md9QE3VCaILuch2z5483lUcIgj452ks1VZFQto7%2BUwGwcNYN96pyt%2BbjJ%2FWZv5zGCABcmI02MQ%2Fp2qOuBaj8ZfxikmlPoSGZofQ5lHGMgNOlYWUTwcEd9VTJA3uuVvX3cHp%2Fsbkg1GHIXyX%2FSIngi58G9CA%2F6wUDKQIQ43eA1XZzoDLQeJGDUjZ9tIvHMW2oXx%2F%2BKsQx6W70xnDCAxt66ufnn5MTewulTLW7AZxr9WRO4SkZX9O2UWsMUsWkNmWrh%2BjFE4DrYJMOhvAVMOjNEqtT9zW2TYiHr4XVdT6iew3elnf4MxSD2jzb2nPsv8ZJs%2BXcfRaBgWZHFg1%2FymBfhYepZO3d3o6kCmMFB8rK4MK2xvtZ47102%2F71mip5DzEd2gr1moWrMiJkA19PKLfZhjeMSrwNJVseCjw9km%2FTli2MSEST%2F1qJNd02g%2BgqP2KPUUr6FWuQc7T9A%2Fgo7Y7s4%2F%2BjWxsrNDxF4Y5diSwFeY8H8m58RKdUAVl%2BJZjg4z6h5xqcYeHlk%3D',
    'section_data_ids': '%7B%22geolocation%22%3A1717057373%2C%22adult_goods%22%3A1717057372%2C%22cart%22%3A1717057342%7D',
        }

        if type == 'options':
            return cookies_options
        if type == 'filters':
            return cookies_filters
        if type == 'item':
            return cookies_item

        raise Exception('Invalid cookies type')
    
    def _get_url(self, type):
        urls = {
            'options': 'https://goldapple.ru/front/api/catalog/products',
            'filters': 'https://goldapple.ru/front/api/catalog/filters',
            'item': 'https://goldapple.ru/front/api/delivery/calculate/item'
        }
        return urls[type]
