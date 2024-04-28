from flask import Flask, Blueprint
from flask_oauthlib.client import OAuth
import os
from dotenv import load_dotenv

# Loading environment variables at the start
load_dotenv()

app = Flask(__name__)
oauth = OAuth(app)

# Global variables to hold the OAuth remote apps
google = None
fanduel = None

def create_app():
    global google, fanduel

    # Basic configuration settings
    app.config['TESTING'] = True
    app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')
    app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET')
    app.config['FANDUEL_CONSUMER_KEY'] = os.getenv('FANDUEL_CONSUMER_KEY', 'default_key')
    app.config['FANDUEL_CONSUMER_SECRET'] = os.getenv('FANDUEL_CONSUMER_SECRET', 'default_secret')
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True

    # Setup OAuth providers if not already set up
    if google is None:
        google = oauth.remote_app(
            'google',
            consumer_key=app.config['GOOGLE_CLIENT_ID'],
            consumer_secret=app.config['GOOGLE_CLIENT_SECRET'],
            request_token_params={'scope': 'email profile'},
            base_url='https://www.googleapis.com/oauth2/v1/',
            request_token_url=None,
            access_token_method='POST',
            access_token_url='https://accounts.google.com/o/oauth2/token',
            authorize_url='https://accounts.google.com/o/oauth2/auth',
        )

    if fanduel is None:
        fanduel = oauth.remote_app(
            'fanduel',
            consumer_key=app.config['FANDUEL_CONSUMER_KEY'],
            consumer_secret=app.config['FANDUEL_CONSUMER_SECRET'],
            request_token_params={'scope': 'email'},
            base_url='https://api.fanduel.com/',
            access_token_method='POST',
            access_token_url='https://api.fanduel.com/oauth/token',
            authorize_url='https://api.fanduel.com/oauth/authorize'
        )

    # Register the main blueprint
    main_blueprint = Blueprint('main', __name__, template_folder='templates')
    if 'main' not in app.blueprints:
        app.register_blueprint(main_blueprint)

    return app
