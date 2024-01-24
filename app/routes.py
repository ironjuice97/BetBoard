from flask import request, redirect, url_for, session, jsonify
from app import oauth

# Import 'main_blueprint' from the '__init__.py' file
from app import create_app

app, main_blueprint = create_app()

# Route for initiating the OAuth flow
@main_blueprint.route('/login')
def login():
    # Redirect the user to the FanDuel authorization page
    return oauth.fanduel.authorize_redirect(callback=url_for('main.authorized', _external=True))

# Route for logging out
@main_blueprint.route('/logout')
def logout():
    # Clear the FanDuel token from the session
    session.pop('fanduel_token', None)
    return redirect(url_for('main.index'))

# Route for handling the OAuth callback
@main_blueprint.route('/login/authorized')
def authorized():
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
    # Retrieve user information from the session or database
    # Example: user_id = session.get('user_id')
    # Fetch user-specific data from your application's database
    # Example: user_data = fetch_user_data_from_database(user_id)

    if 'fanduel_token' in session:
        # Display a welcome message with the user's name if logged in
        return f"Welcome to your profile, {user_data['username']}!"
    else:
        return "You are not logged in."

# Add more routes and logic as needed
