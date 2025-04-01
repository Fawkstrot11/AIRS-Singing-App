# The structure that calls all the parts in sequence. This is subject to change if necessary (especially whether
# input should be read here or in the web portion)
import inputProcessor
import noteSelector
import database
import toneGenerator

def execute(temp_id):
    print("Part 1")
    conn = database.create_connection("airs_app.db")
    user_id = 1 #need to have a way to call the user id
    note_count = int(database.get_user_progress(conn, 1)[1]//20+1)
    print("Note amounts" + str(note_count))

    #notes=(noteSelector.get_notes(noteCount, lower_bound=48, upper_bound=48))
    notes = database.get_biased_notes_for_user(conn, user_id, k=note_count)
    toneGenerator.generate_notes(notes, filename=str(temp_id)+".wav")
    print("Part 1 done")
    return notes

