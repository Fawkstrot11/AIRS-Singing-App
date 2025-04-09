import os
from flask import Blueprint, render_template, request


results_bp = Blueprint('results', __name__)

@results_bp.route('/')
def results():
    # Retrieve temp_id and score from cookies
    temp_id = request.cookies.get('temp_id')
    score = request.cookies.get('score')

    if not temp_id or not score:
        return "Error: Missing temp_id or score.", 400

    # Path to the image
    image_path = os.path.join('outputs', f'{temp_id}.png')

    if not os.path.exists(image_path):
        return "Error: Image file not found.", 404

    return render_template('results.html', temp_id=temp_id, score=score)