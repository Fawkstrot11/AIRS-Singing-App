import time

from flask import Blueprint, render_template, request, make_response, redirect
import os
from part2 import execute as part2_execute  # Import the part2 execute function
import json
import subprocess

def convert_webm_to_wav(webm_path, wav_path):
    try:
        ffmpeg_path = "../ffmpeg-master-latest-win64-gpl-shared/bin/ffmpeg.exe"  # Update path as needed
        command = [ffmpeg_path, '-y', '-i', webm_path, wav_path]
        subprocess.run(command, check=True)
        print(f"Conversion successful: {wav_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return False
    return True

challenge_bp = Blueprint('challenge', __name__)

# Route for the challenge page
@challenge_bp.route('/', methods=['GET', 'POST'])
def challenge():

    print("AAAAAAAAAA")
    temp_id = request.cookies.get('temp_id')
    notes_json = request.cookies.get('part1_notes')
    uid = request.cookies.get('airsID', 1)

    if temp_id and notes_json:
        notes = json.loads(notes_json)
        audio_file = os.path.join("app", "static", "audio", f"{temp_id}.wav")

        if request.method == 'POST':
            user_audio = request.files.get('user_audio')
            if user_audio:
                # Ensure the inputs directory exists, create it if not
                inputs_dir = os.path.join(os.getcwd(), 'inputs')  # Absolute path to inputs directory
                if not os.path.exists(inputs_dir):
                    os.makedirs(inputs_dir)  # Create the directory if it doesn't exist

                user_audio_path = os.path.join(inputs_dir, f"{temp_id}_user.webm")
                user_audio.save(user_audio_path)

                convert_webm_to_wav(os.path.join(inputs_dir, f"{temp_id}_user.webm"), os.path.join(inputs_dir, f"{temp_id}_user.wav"))

                # # Wait until the file is saved (polling for 10 seconds)
                # timeout = 10  # seconds
                # elapsed_time = 0
                # while not os.path.exists(user_audio_path) and elapsed_time < timeout:
                #     time.sleep(1)  # Wait for 1 second before checking again
                #     elapsed_time += 1
                #
                # if not os.path.exists(user_audio_path):
                #     return "Error: File upload timed out", 500

                # Process with part2 and get results
                average_score, per_note_grades = part2_execute(temp_id, notes, uid)

                print("YEEEEEEEEEEEEAH")
                # Display results
                resp = make_response(redirect('/results'))  # Redirect to index route
                resp.set_cookie('score', str(average_score), path='/')
                return resp

        return render_template('challenge.html', temp_id=temp_id, audio_file=audio_file)

    return "Error: Missing temp_id or notes.", 400