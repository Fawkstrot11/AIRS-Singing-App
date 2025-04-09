import unittest
import inputGrader
import inputProcessor
import unittest
import noteSelector
import unittest
import noteUtils
import unittest
import os
import outputFormatter

class TestOutputFormatter(unittest.TestCase):

    def test_output_file_created(self):
        output_file = "output.png"

        # Step 1: Delete output.png if it already exists
        if os.path.exists(output_file):
            os.remove(output_file)

        self.assertFalse(os.path.exists(output_file), "output.png should not exist before the test")

        # Step 2: Call the grade function
        outputFormatter.create([1, 2, 3, 4, 5], [2, 3, 4])

        # Step 3: Check that output.png now exists
        self.assertTrue(os.path.exists(output_file), "output.png was not created")


class TestNoteUtils(unittest.TestCase):

    def test_hz_to_note_name_basic(self):
        self.assertEqual(noteUtils.hz_to_note_name(440.0), "A4")
        self.assertEqual(noteUtils.hz_to_note_name(261.63), "C4")  # Close to middle C
        self.assertEqual(noteUtils.hz_to_note_name(0), None)

    def test_note_name_to_hz_basic(self):
        self.assertAlmostEqual(noteUtils.note_name_to_hz("A4"), 440.0, places=1)
        self.assertAlmostEqual(noteUtils.note_name_to_hz("C4"), 261.63, places=1)
        self.assertAlmostEqual(noteUtils.note_name_to_hz("E5"), 659.26, places=1)

    def test_note_all_to_hz(self):
        notes = ["A4", "C4", "E5"]
        expected = [440.0, 261.63, 659.26]
        result = noteUtils.note_all_to_hz(notes)
        for r, e in zip(result, expected):
            self.assertAlmostEqual(r, e, places=1)

    def test_hz_all_to_notes(self):
        freqs = [440.0, 261.63, 659.26]
        expected = ["A4", "C4", "E5"]
        result = noteUtils.hz_all_to_notes(freqs)
        for r, e in zip(result, expected):
            self.assertEqual(r, e)

    def test_note_to_order_and_back(self):
        notes = ["A0", "C4", "B9"]
        for note in notes:
            order = noteUtils.note_to_order(note)
            self.assertEqual(noteUtils.order_to_note(order), note)

    def test_order_to_note_edges(self):
        self.assertEqual(noteUtils.order_to_note(0), "C0")
        self.assertEqual(noteUtils.order_to_note(119), "B9")

    def test_note_to_order_range(self):
        notes = ["C4", "A4", "E5"]
        low, high = noteUtils.order_range(notes)
        self.assertEqual(noteUtils.order_to_note(low), "C4")
        self.assertEqual(noteUtils.order_to_note(high), "E5")

    def test_invalid_hz_rounding(self):
        hz = noteUtils.note_name_to_hz("A4")
        back = noteUtils.hz_to_note_name(hz)
        self.assertEqual(back, "A4")  # Check round-trip accuracy

    def test_order_range_single_note(self):
        notes = ["G4"]
        low, high = noteUtils.order_range(notes)
        self.assertEqual(low, high)
        self.assertEqual(noteUtils.order_to_note(low), "G4")


class TestGetNotes(unittest.TestCase):

    def test_sequence_length(self):
        result = noteSelector.get_notes(sequence_length=5, lower_bound=40, upper_bound=80, step=1)
        self.assertEqual(len(result), 5)

    def test_notes_within_bounds(self):
        result = noteSelector.get_notes(sequence_length=10, lower_bound=48, upper_bound=72, step=2)
        for note in result:
            midi_number = note_to_midi(note)
            self.assertGreaterEqual(midi_number, 48)
            self.assertLess(midi_number, 72)

    def test_single_note(self):
        result = noteSelector.get_notes(sequence_length=1)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], str)

    def test_step_limit(self):
        # Large step size but still within 0–11
        result = noteSelector.get_notes(sequence_length=5, step=11)
        self.assertEqual(len(result), 5)

def note_to_midi(note):
    """
    Helper function to convert note name (e.g. 'C#4') to MIDI number.
    """
    notes = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6,
             'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    if note[:-1] in notes:
        pitch = notes[note[:-1]]
    else:
        # Handles note names like 'A#' in 'A#4'
        pitch = notes[note[:-2]]
    octave = int(note[-1]) if note[-2].isdigit() == False else int(note[-2:])
    return octave * 12 + pitch


class TestDetectNotes(unittest.TestCase):
    def test_detect_notes_returns_non_empty_list(self):
        result = inputProcessor.detect_notes("input.wav")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0, "detect_notes() returned an empty list")

class TestInputGrading(unittest.TestCase):


    def test_exact_match(self):
        original = ['C4', 'D4', 'E4']
        input_notes = ['C4', 'D4', 'E4']


        avg_grade, grades = inputGrader.input_grading(original, input_notes)
        self.assertEqual(grades, [1.0, 1.0, 1.0])
        self.assertEqual(avg_grade, 1.0)

    def test_notes_within_strictness(self):
        original = ['C4', 'D4', 'E4']
        input_notes = ['C#4', 'D#4', 'F4']  # All one semitone away
        expected_grades = [1/2, 1/2, 1/2]

        avg_grade, grades = inputGrader.input_grading(original, input_notes)
        self.assertEqual(grades, expected_grades)
        self.assertEqual(avg_grade, sum(expected_grades)/3)

    def test_notes_outside_strictness(self):
        original = ['C4']
        input_notes = ['G5']  # More than 3 semitones away


        avg_grade, grades = inputGrader.input_grading(original, input_notes, strictness=3)
        self.assertEqual(grades, [0])
        self.assertEqual(avg_grade, 0.0)

    def test_none_input(self):
        original = ['C4', 'D4']
        input_notes = [None, 'D4']
        expected_grades = [0, 1.0]

        avg_grade, grades = inputGrader.input_grading(original, input_notes)
        self.assertEqual(grades, expected_grades)
        self.assertEqual(avg_grade, sum(expected_grades)/2)

    def test_custom_strictness(self):
        original = ['C4']
        input_notes = ['E4']  # 4 semitones away

        avg_grade, grades = inputGrader.input_grading(original, input_notes, strictness=2)
        self.assertEqual(grades, [0])
        self.assertEqual(avg_grade, 0.0)



if __name__ == '__main__':
    unittest.main()
