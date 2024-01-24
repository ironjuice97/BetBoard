from flask import Flask
from flask_oauthlib.client import OAuth
import os

# Initialize the Flask app
def create_app():
    app = Flask(__name__)

    # Load sensitive information from environment variables
    app.config['FANUEL_CONSUMER_KEY'] = os.environ.get('FANUEL_CONSUMER_KEY')
    app.config['FANUEL_CONSUMER_SECRET'] = os.environ.get('FANUEL_CONSUMER_SECRET')
    app.secret_key = os.environ.get('FLASK_SECRET_KEY')  # Set a secret key for Flask sessions

    # Check if the necessary environment variables are set
    if not all([app.config['FANUEL_CONSUMER_KEY'], app.config['FANUEL_CONSUMER_SECRET'], app.secret_key]):
        raise EnvironmentError("Missing required environment variables: FANUEL_CONSUMER_KEY, FANUEL_CONSUMER_SECRET, or FLASK_SECRET_KEY")

    # Initialize OAuth
    oauth = OAuth(app)

    # Configure Fanduel OAuth
    fanduel = oauth.remote_app(
        'fanduel',
        consumer_key=app.config['FANUEL_CONSUMER_KEY'],
        consumer_secret=app.config['FANUEL_CONSUMER_SECRET'],
        request_token_params={'scope': 'email'},
        base_url='https://api.fanduel.com/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://api.fanduel.com/oauth/token',
        authorize_url='https://api.fanduel.com/oauth/authorize'
    )

    # Import and register the blueprint from routes.py
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)  # Registers the main_blueprint Blueprint instance with the Flask app

    return app
