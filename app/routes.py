from flask import render_template, request, redirect, url_for, session, jsonify
from app import oauth, main_blueprint, google
from app.fanduel import FanduelAPI

@main_blueprint.route('/')
def home():
    return render_template('homepage.html')

@main_blueprint.route('/login')
def login():
    return google.authorize(callback=url_for('main.authorized', _external=True))

@main_blueprint.route('/logout')
def logout():
    session.pop('google_token', None)
    session.pop('fanduel_token', None)
    return redirect(url_for('main.home'))

@main_blueprint.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        error_reason = request.args.get('error_reason', 'Unknown')
        error_description = request.args.get('error_description', 'Unknown')
        return f"Access denied: reason={error_reason} error={error_description}", 401
    session['google_token'] = (resp['access_token'], '')
    return redirect(url_for('main.profile'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@main_blueprint.route('/profile')
def profile():
    if 'google_token' not in session:
        return redirect(url_for('main.login'))
    return render_template('profile.html')

@main_blueprint.route('/connect_fanduel', methods=['GET', 'POST'])
def connect_fanduel():
    if request.method == 'POST':
        fanduel_api = FanduelAPI()
        try:
            access_token = fanduel_api.authenticate()
            session['fanduel_token'] = access_token
            return redirect(url_for('main.profile'))
        except Exception as e:
            return f"Failed to authenticate with FanDuel: {str(e)}", 500
    return render_template('connect_fanduel.html')

@main_blueprint.route('/betting-data')
def betting_data():
    # Simulate some betting data
    betting_data = [
        {
            'username': 'user1',
            'wins': 10,
            'losses': 5,
            'win_percentage': 0.67
        },
        {
            'username': 'user2',
            'wins': 8,
            'losses': 7,
            'win_percentage': 0.53
        }
    ]
    return jsonify(betting_data)

@main_blueprint.route('/leaderboard')
def leaderboard():
    if 'google_token' not in session or 'fanduel_token' not in session:
        return redirect(url_for('main.login'))
    fanduel_api = FanduelAPI()
    try:
        contests = fanduel_api.get_contests()
        # TODO: Process the contests data and generate leaderboard
        return render_template('leaderboard.html', contests=contests)
    except Exception as e:
        return f"Failed to retrieve contests data: {str(e)}", 500
    

