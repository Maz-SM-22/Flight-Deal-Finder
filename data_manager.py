import requests 

class DataManager:
    
    def __init__(self):
        self.auth_token = 'Bearer wDNR2LDl9FKzbVTJyPdSXr8JbcBavox1cDr5RbNa6N'
        self.headers = {'Authorization': self.auth_token}
        self.endpoint = 'https://api.sheety.co/8682e61342225b4b2474a915f342cf1d/flightDeals/prices'
        self.data = {}

    def read_rows(self): 
        response = requests.get(self.endpoint, headers=self.headers)
        response.raise_for_status()
        self.data = response.json()['prices']
        return self.data

    def edit_rows(self, row_id: int, iata: str): 
        new_data = self.data[row_id]
        new_data['iataCode'] = iata 
        _id = new_data['id']
        response = requests.put(f'{self.endpoint}/{_id}', headers=self.headers, json={'price': new_data})
        response.raise_for_status()
        return response.status_code