import requests

class FlightSearch:
    
    def __init__(self):
        self.api_key = 'eQ5wocjCwEWaJpSXUqufYy00HOURLQF_'
        self.endpoint = 'https://tequila-api.kiwi.com'
        self.search = '/v2/search'
        self.location_search = '/locations/query'
        self.headers = {'apikey': self.api_key}             # Params should include: fly_from, fly_to, dateFrom, dateTo
    
    def search_flights(self, params: dict): 
        response = requests.get(f'{self.endpoint}{self.search}', headers=self.headers, params=params)
        response.raise_for_status()
        try: 
            return response.json()['data'][0]
        except: 
            print('No results found for this search')
            return None 

    def get_iata_code(self, city): 
        search_params = {'term': city, 'location_types': 'city'}
        response = requests.get(f'{self.endpoint}{self.location_search}', headers=self.headers, params=search_params)
        response.raise_for_status()
        data = response.json()['locations']
        return [item['code'] for item in data if item['code'] != None][0]