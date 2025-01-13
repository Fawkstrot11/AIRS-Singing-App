def hz_to_note_name(hz):
    A4 = 440.0
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    if hz == 0:
        return None
    midi_num = int(round(69 + 12 * np.log2(hz / A4)))
    note = notes[midi_num % 12] + str(midi_num // 12 - 1)
    return note