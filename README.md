BetBoard - Flask Web Application



Project Structure
The project is organized as follows:

app/: This directory contains the main application code.

__init__.py: Initializes the Flask application and sets up the OAuth integration.
routes.py: Defines the routes and views for the application.
Other modules: Add any additional modules or packages relevant to your project.
main.py: Entry point for running the Flask application.

.env: Configuration file for environment variables (e.g., secret keys, API credentials).

requirements.txt: 
  Flask-OAuthlib==0.9.6
  Werkzeug==2.0.2



Installation
To run the BetBoard web application locally, follow these steps:

1. Clone the repository to your local machine: git clone https://github.com/ironjuice97/BetBoard1.git
2. Navigate to the project directory: cd BetBoard
3. Create a virtual environment (recommended) and activate it: python -m venv venv
source venv/bin/activate
4. Install the required dependencies from requirements.txt:pip install -r requirements.txt



Usage

To run the BetBoard web application:

1. Ensure your virtual environment is activated (if not already): source venv/bin/activate
2. Start the Flask development server: python main.py
Access the application in your web browser at http://127.0.0.1:5000/.



Configuration
The application relies on environment variables for configuration. Ensure that you have set up the following environment variables in your .env file:

FANUEL_CONSUMER_KEY: Your FanDuel API consumer key.
FANUEL_CONSUMER_SECRET: Your FanDuel API consumer secret.
FLASK_SECRET_KEY: A secret key for Flask sessions.







