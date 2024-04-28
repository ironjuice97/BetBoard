import requests
from flask import current_app

class FanduelAPI:
    def __init__(self):
        self.base_url = "https://api.fanduel.com"

    def authenticate(self, username, password):
        try:
            response = requests.post(f"{self.base_url}/oauth/token", data={
                "grant_type": "password",
                "username": username,
                "password": password,
                "client_id": current_app.config['FANUEL_CONSUMER_KEY'],
                "client_secret": current_app.config['FANUEL_CONSUMER_SECRET']
            })
            response.raise_for_status()
            return response.json()['access_token']
        except requests.RequestException as e:
            raise Exception(f"FanDuel API authentication failed: {str(e)}")

    def get_betting_history(self, access_token):
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(f"{self.base_url}/users/self/betting_history", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to retrieve betting history: {str(e)}")
        
        