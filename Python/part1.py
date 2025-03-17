# The structure that calls all the parts in sequence. This is subject to change if necessary (especially whether input should be read here or in the web portion)
import inputProcessor
import noteSelector
import database
import toneGenerator

def execute(temp_id):
    conn = database.create_connection("airs_app.db")
    noteCount = int(database.get_user_progress(conn, 1)[1]//20+1)
    print(noteCount)
    notes=(noteSelector.get_notes(noteCount, lower_bound=48, upper_bound=48))
    toneGenerator.generate_notes(notes, filename=str(temp_id)+".wav")
    return notes

