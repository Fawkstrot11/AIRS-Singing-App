from flask import Blueprint, render_template, request, redirect, make_response
from werkzeug.security import generate_password_hash
from database import signup as signup_user
import random

# Create a Blueprint for login
signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        theme = random.choice(["standard","standard","standard","princess","rock"])  # Theme is currently random, weighted to standard. Easy to change.
        
        # theme = request.form.get('theme', 'standard')  # Uncomment if using selection box. Default to 'standard' theme if not provided

        # Encrypt the password using bcrypt
        hashed_password = generate_password_hash(password)

        try:
            # Call the signup function to add the user to the database
            signup_user(username, hashed_password, theme)

            # Redirect to the login page after successful signup
            return redirect('/login')

        except Exception as e:
            error = f"Error signing up: {str(e)}"

    return render_template('signup.html', error=error)
