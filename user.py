import os 
import requests

class User: 

    def __init__(self, name: str, surname: str, email: str):
        self.auth_token = os.environ['SHEETY_AUTH_TOKEN']
        self.headers = {"Authorization": self.auth_token, "Content-Type": "application/json"}
        self.endpoint = os.environ['SHEETY_FLIGHT_URL']
        self.name = name
        self.surname = surname
        self.email = email 

    def add_user(self, user): 
        payload = {
            "user": {
                "firstName": user.name[0], 
                "lastName": user.surname[0], 
                "email": user.email
            }
        }
        response = requests.post(self.endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.status_code

    def get_user_emails(self): 
        response = requests.get(self.endpoint, headers=self.headers)
        users = response.json()['users']
        return [item['email'] for item in users]