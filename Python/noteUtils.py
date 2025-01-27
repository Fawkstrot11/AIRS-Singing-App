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