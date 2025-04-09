# picks the notes to be used for a tone sequence. should, at some point, be adaptive.
from . import random
from . import noteUtils
from .database import get_user_progress
from .noteUtils import note_name_to_hz


def get_notes(sequence_length, lower_bound=40, upper_bound=80, step=1):
    """
    Picks the notes to be used for a tone sequence.
    :param sequence_length: The desired number of notes.
    :param lower_bound: The lowest possible note (inclusive) that will be generated (with C0 being 0 and B9 being 119).
    :param upper_bound: The highest possible note (exclusive) that will be generated (with C0 being 0 and B9 being 119).
    :param step: the distance between each note in the sequence (max 11).
    :return: A list of notes.
    """
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    seed = random.randint(lower_bound, upper_bound)
    octave = seed//12
    letter = seed%12
    output = [notes[letter] + str(octave)]
    for i in range(sequence_length-1):
        next_note = random.randint(-1, 1) * step
        if octave*12 + letter + next_note < lower_bound or octave*12 + letter + next_note >= upper_bound:
            next_note *= -1
        if (letter + next_note) % 12 > letter and next_note < 0:
            octave -= 1
            letter = (letter + next_note) % 12
        elif (letter + next_note) % 12 < letter and next_note > 0:
            octave += 1
            letter = (letter + next_note) % 12
        else:
            letter += next_note
        output.append((notes[letter] + str(octave)))
    print("Output:", output)
    return output

def get_notes_difficulty(connection, user_id, sequence_length):
    user_progress = get_user_progress(connection, user_id)
    avg_grade = user_progress[1] if user_progress else 50 #default option

    lower_bound = 40 + int(avg_grade // 20) * 5
    upper_bound = 80 + int(avg_grade // 20) * 5

    return get_notes(sequence_length, lower_bound, upper_bound)

# TODO: add some error checking between the bounds and the step size
