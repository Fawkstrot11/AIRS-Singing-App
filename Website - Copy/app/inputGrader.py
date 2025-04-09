# Take the user's audio and compare it to the target. Note that, currently, output lists are much longer than the target.
import numpy as np
import math
import noteUtils

def input_length_normalize(input_notes):
    """
     Normalize the notes length.
     :param input_notes: List of notes to be normalized.
     :return: Normalized list of notes.
     """
    x = 0
    output = []
    for note in input_notes:
        # Each note seems to occur 43 times in the output, so just keep every 44th note
        if x % 44 == 0:
            output.append(note)
        x += 1
    print("Time normalized output:", output)
    return output


def get_lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def stretch_list(lst, target_length):
    factor = target_length // len(lst)
    remainder = target_length % len(lst)

    stretched = []
    for i, item in enumerate(lst):
        count = factor + (1 if i < remainder else 0)
        stretched.extend([item] * count)

    return stretched


def stretch_to_common_length(lst1, lst2):
    len1, len2 = len(lst1), len(lst2)
    lcm = get_lcm(len1, len2)  # Least common multiple of both lengths

    return stretch_list(lst1, lcm), stretch_list(lst2, lcm)


def num_grading(original_tone, input_notes, strictness=3):
    for i, item in enumerate(original_tone):
        original_tone[i] = noteUtils.hz_to_note_name(item)

    for i, item in enumerate(input_notes):
        input_notes[i] = noteUtils.hz_to_note_name(item)

    input_grading(original_tone,input_notes, strictness)

# Default strictness=3 means that no marks will be given for inputs 4 or more notes away from the original.
def input_grading(original_tone, input_notes, strictness=3):
    """
    Grades the input notes based on how close it is to the original notes.
    :param original_tone: List of original notes.
    :param input_notes: List of input notes to be compared against the original notes.
    :param strictness: Indicates the strictness of the grading in terms of how many notes away from the original the input can be before it's marked as zero (int) default 3.
    :return: grades for each note.
    """
    notes = {'C' : 1, 'C#' : 2, 'D' : 3, 'D#' : 4, 'E' : 5, 'F' : 6, 'F#' : 7,
             'G' : 8, 'G#' : 9, 'A' : 10, 'A#' : 11, 'B': 12}
    grades = []

    original_tone, input_notes = stretch_to_common_length(original_tone, input_notes)

    for i in range(len(original_tone)):

        if input_notes[i] is None:
            grades.append(0)
            continue

        og_note = original_tone[i][0:-1]
        og_octave = original_tone[i][-1]
        input_note = input_notes[i][0:-1]
        input_octave = input_notes[i][-1]

        og_value = int(og_octave)*12 + notes[og_note]
        input_value = int(input_octave)*12 + notes[input_note]

        if abs(og_value - input_value) > strictness:
            grades.append(0)
        else:
            grades.append(1/(abs(og_value - input_value)+1))
    print("Your grade for each note was:", grades)
    print("Your average grade was:", np.mean(grades))
    return [np.mean(grades), grades]