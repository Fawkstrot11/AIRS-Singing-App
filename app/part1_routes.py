import random
import json
from flask import Blueprint, render_template, request, redirect, url_for, make_response
from .part1 import execute as part1_execute  # Import your part1 execute function

part1_bp = Blueprint('part1', __name__)

@part1_bp.route('/', methods=['GET', 'POST'])
def start_challenge():
    if request.method == 'POST':
        # Generate a random temp_id
        temp_id = random.randint(100000, 999999)
        uid = request.cookies.get('airsID', 1)  # Get the user id from the cookie

        # Execute part1 and get the note list
        notes = part1_execute(temp_id, uid=int(uid))

        # Convert notes list to JSON string to store in cookies
        notes_json = json.dumps(notes)

        # Create response and set cookies for temp_id and notes
        resp = make_response(redirect(url_for('challenge.challenge', temp_id=temp_id)))
        resp.set_cookie('temp_id', str(temp_id), path='/')
        resp.set_cookie('part1_notes', notes_json, path='/')

        return resp

    return render_template('start_challenge.html')
