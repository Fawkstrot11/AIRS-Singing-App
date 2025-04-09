from flask import Blueprint, render_template, request, redirect, make_response
from werkzeug.security import generate_password_hash

from .database import login as login_user  # Make sure this works from your project root

# Create a Blueprint for login
login_bp = Blueprint('login', __name__)

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Modify the login_user function to return both user_id and theme
        user_id, theme = login_user(username, password)

        if user_id is not None:
            resp = make_response(redirect('/index'))  # Redirect to index route
            resp.set_cookie('airsloggedin', 'true', path='/')
            resp.set_cookie('airsID', str(user_id), path='/')
            resp.set_cookie('style', theme, path='/')  # Set the 'style' cookie to the user's theme
            return resp
        else:
            error = 'Invalid username or password'

    return render_template('login.html', error=error)
