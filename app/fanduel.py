import requests
from flask import current_app

class FanduelAPI:
    def __init__(self):
        self.base_url = "https://api.fanduel.com"
        self.auth_tokens = {
            'basic_auth_token': current_app.config['FANUEL_BASIC_AUTH_TOKEN'],
            'x_auth_token': current_app.config['FANUEL_X_AUTH_TOKEN']
        }

    def authenticate(self):
        headers = {
            'Authorization': f"Basic {self.auth_tokens['basic_auth_token']}",
            'X-Auth-Token': self.auth_tokens['x_auth_token']
        }
        response = requests.post(f"{self.base_url}/oauth/token", headers=headers)
        response.raise_for_status()
        return response.json()['access_token']

    def get_auth_header(self):
        access_token = self.authenticate()
        return {'Authorization': f"Bearer {access_token}"}

    def get_contests(self):
        response = requests.get(f"{self.base_url}/contests", headers=self.get_auth_header())
        response.raise_for_status()
        return response.json()['contests']

    def safe_request(self, url, headers):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as err:
            print(f"An error occurred: {err}")

            