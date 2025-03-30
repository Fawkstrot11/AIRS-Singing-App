<<<<<<< Updated upstream
import numpy as np

def hz_to_note_name(hz):
    """
    Converts a frequency given in Hertz (hz) to the corresponding musical note.
    :param hz: Frequency in Hertz (float).
    :return: Musical note name as a string or None if input is 0.
    """
    A4 = 440.0
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    if hz == 0:
        return None
    midi_num = int(round(69 + 12 * np.log2(hz / A4)))
    note = notes[midi_num % 12] + str(midi_num // 12 - 1)
    return note

def note_name_to_hz(note):
    """
    Converts a musical note to the corresponding frequency in Hertz (hz).
    :param note: Musical note (str).
    :return: Frequency in Hertz, rounded to 3 decimals places (float).
    """
    A4 = 440
    notes = {'C' : -9, 'C#' : -8, 'D' : -7, 'D#' : -6, 'E' : -5, 'F' : -4, 'F#' : -3,
             'G' : -2, 'G#' : -1, 'A' : 0, 'A#' : 1, 'B': 2}
    octave = int(note[-1])
    letter = note[0:-1]
    distance = (octave - 4)*12 + notes[letter]
    hz = A4 * (2**(1/12)) ** distance
    return round(hz, 3)
=======
import numpy as np

def hz_to_note_name(hz):
    """
    Converts a frequency given in Hertz (hz) to the corresponding musical note.
    :param hz: Frequency in Hertz (float).
    :return: Musical note name as a string or None if input is 0.
    """
    A4 = 440.0
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    if hz == 0:
        return None
    midi_num = int(round(69 + 12 * np.log2(hz / A4)))
    note = notes[midi_num % 12] + str(midi_num // 12 - 1)
    return note

def note_name_to_hz(note):
    """
    Converts a musical note to the corresponding frequency in Hertz (hz).
    :param note: Musical note (str).
    :return: Frequency in Hertz, rounded to 3 decimals places (float).
    """
    A4 = 440
    notes = {'C' : -9, 'C#' : -8, 'D' : -7, 'D#' : -6, 'E' : -5, 'F' : -4, 'F#' : -3,
             'G' : -2, 'G#' : -1, 'A' : 0, 'A#' : 1, 'B': 2}
    octave = int(note[-1])
    letter = note[0:-1]
    distance = (octave - 4)*12 + notes[letter]
    hz = A4 * (2**(1/12)) ** distance
    return round(hz, 3)


def note_all_to_hz(notes):
    output = []
    for i in notes:
        output.append(note_name_to_hz(i))
    return output


def hz_all_to_notes(notes):
    output = []
    for i in notes:
        output.append(hz_to_note_name(i))
    return output

#May be wrong
def note_to_order_old(note): #where A0 is 0 and B9 is 119
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    letter = note[:-1]
    octave = int(note[-1])
    return notes.index(letter)+octave*12

#So quick note on this the code above may or may not correctly translate all notes to MIDI numbers
#The one below does so we need to delete the one above idk
def note_to_order(note):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    for i in range(1, 4):  #handle multi-digit octaves
        letter = note[:-i]
        octave_str = note[-i:]
        if letter in notes and octave_str.isdigit():
            midi = notes.index(letter) + int(octave_str) * 12 + 12
            return midi
    raise ValueError(f"Invalid note format: {note}")

def order_to_note(number):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = number//12
    letter = notes[number%12]
    return letter + str(octave)

def order_range(notes):
    min = 120
    max = 0
    for i in notes:
        val = note_to_order(i)
        if val > max:
            max = val
        if val < min:
            min = val
    return min, max
>>>>>>> Stashed changes
