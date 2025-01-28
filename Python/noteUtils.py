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