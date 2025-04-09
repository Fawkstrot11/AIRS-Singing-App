# The structure that calls all the parts in sequence. This is subject to change if necessary (especially whether
# input should be read here or in the web portion)
import inputProcessor
import noteSelector
import database
import toneGenerator
import os

#Luke : needed to import OS so it could put the audio where it needs to go

def execute(temp_id, uid=1):
    print("Part 1")
    conn = database.create_connection("airs_app.db")
    user_id = uid #need to have a way to call the user id
    note_count = int(database.get_user_progress(conn, 1)[1]//20+1)
    print("Note amounts" + str(note_count))

    #notes=(noteSelector.get_notes(noteCount, lower_bound=48, upper_bound=48))    
    notes = database.get_biased_notes_for_user(conn, user_id, k=note_count)
    
    # Luke code starts here. This is to check for a directory to save the audio to.
    # If it can't find one, it makes one. 

    audio_directory = os.path.join("..", "static", "audio")
    os.makedirs(audio_directory, exist_ok=True)

    audio_path = os.path.join(audio_directory, f"{temp_id}.wav")
    
    #Luke code ends here. Changed the line below this comment to use the new path tho.

    toneGenerator.generate_notes(notes, filename=audio_path)
    print("Part 1 done")
    return notes
