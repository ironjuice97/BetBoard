from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from app import oauth, main_blueprint  # Import the Flask app and the OAuth object from app/__init__.py

@main_blueprint.route('/')
def home():
    print("Home route accessed")  # Add a debugging message
    return "Welcome to the home page!"

# Route for initiating the OAuth flow
@main_blueprint.route('/login')
def login():
    print("Login route accessed")  # Add a debugging message
    # Redirect the user to the FanDuel authorization page
    return oauth.fanduel.authorize_redirect(callback=url_for('main.authorized', _external=True))

# Route for logging out
@main_blueprint.route('/logout')
def logout():
    print("Logout route accessed")  # Add a debugging message
    # Clear the FanDuel token from the session
    session.pop('fanduel_token', None)
    return redirect(url_for('main.index'))

# Route for handling the OAuth callback
@main_blueprint.route('/login/authorized')
def authorized():
    print("Authorized route accessed")  # Add a debugging message
    try:
        # Authorize access and retrieve the access token
        response = oauth.fanduel.authorize_access_token()
        session['fanduel_token'] = (response['access_token'], '')

        # Fetch user information from FanDuel after successful OAuth
        user_info = oauth.fanduel.get('user')
        if user_info.status_code == 200:
            user_data = user_info.json()
            
            # Store user_data in your application's database or session as needed
            # Example: session['user_id'] = user_data['id']

            # Redirect to the user's profile page
            return redirect(url_for('main.profile'))
        else:
            return "Error fetching user information from FanDuel."

    except Exception as e:
        return f"OAuth authorization failed: {str(e)}"

# Route for displaying the user's profile
@main_blueprint.route('/profile')
def profile():
    print("Profile route accessed")  # Add a debugging message
    # Retrieve user information from the session or database
    # Example: user_id = session.get('user_id')
    # Fetch user-specific data from your application's database
    # Example: user_data = fetch_user_data_from_database(user_id)

    if 'fanduel_token' in session:
        # Display a welcome message with the user's name if logged in
        return f"Welcome to your profile, {session['fanduel_token'][1]}!"  # Use the stored token data
    else:
        return "You are not logged in."

# Add more routes and logic as needed
