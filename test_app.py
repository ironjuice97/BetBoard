# pytest test_app.py

from flask_testing import TestCase
from unittest.mock import patch
from app import create_app, google
from app.fanduel import FanduelAPI
import unittest

class FlaskTestCase(TestCase):
    def create_app(self):
        return create_app()

class TestGoogleOAuth(FlaskTestCase):
    @patch('app.google.authorized_response')
    def test_authorized_success(self, mock_authorized_response):
        mock_authorized_response.return_value = {'access_token': 'dummy_token'}
        response = self.client.get('/login/authorized?code=12345')
        self.assertEqual(response.status_code, 302)
        self.assertIn('google_token', self.client.session)

    @patch('app.google.authorized_response')
    def test_authorized_failure(self, mock_authorized_response):
        mock_authorized_response.return_value = None
        response = self.client.get('/login/authorized?error_reason=access_denied&error_description=User+denied+access')
        self.assertIn(b'Access denied', response.data)

class TestFanduelAPI(FlaskTestCase):
    @patch('requests.post')
    def test_authenticate_success(self, mock_post):
        mock_post.return_value.json.return_value = {'access_token': 'dummy_token'}
        fanduel_api = FanduelAPI()
        access_token = fanduel_api.authenticate()
        self.assertEqual(access_token, 'dummy_token')

    @patch('requests.get')
    def test_get_contests_success(self, mock_get):
        mock_get.return_value.json.return_value = {'contests': []}
        fanduel_api = FanduelAPI()
        contests = fanduel_api.get_contests()
        self.assertEqual(contests, [])


    @patch('requests.post')
    def test_authenticate_failure(self, mock_post):
        mock_post.side_effect = requests.RequestException('Authentication failed')
        fanduel_api = FanduelAPI()
        with self.assertRaises(Exception):
            fanduel_api.authenticate()

    @patch('requests.get')
    def test_get_contests_failure(self, mock_get):
        mock_get.side_effect = requests.RequestException('Failed to retrieve contests')
        fanduel_api = FanduelAPI()
        with self.assertRaises(Exception):
            fanduel_api.get_contests()

    @patch('requests.get')
    def test_get_betting_history_success(self, mock_get):
        mock_get.return_value.json.return_value = {'betting_history': []}
        fanduel_api = FanduelAPI()
        betting_data = fanduel_api.get_betting_history('dummy_token')
        self.assertEqual(betting_data, {'betting_history': []})

    @patch('requests.get')
    def test_get_betting_history_failure(self, mock_get):
        mock_get.side_effect = requests.RequestException('Failed to retrieve betting history')
        fanduel_api = FanduelAPI()
        with self.assertRaises(Exception):
            fanduel_api.get_betting_history('dummy_token')

if __name__ == '__main__':
    unittest.main()

    
