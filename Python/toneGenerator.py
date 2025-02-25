# Take the target notes and turn them into noise

from synthesizer import Synthesizer, Writer
import numpy as np
import noteUtils

def generate_notes(notes, filename="output.wav"):
    """
    Generates an audio .WAV file using the musical notes list passed as a parameter.
    :param notes: List of musical notes.
    :param filename: Name of the file (string) to be created, y default the name is output.wav.
    """
    # Create a Synthesizer object (with default sample rate)
    synth = Synthesizer()

    # Create a writer object for writing to a file
    writer = Writer()

    # Generate the audio for the sequence of notes (frequencies)
    audio_data = []

    for note in notes:
        # Create a single tone for each note with a given duration
        tone = synth.generate_chord([note], 1.0)
        audio_data.append(tone)

    # Concatenate all generated tones to form the full track
    full_audio = np.concatenate(audio_data)

    # Write the final audio to a WAV file
    writer.write_wave(filename, full_audio)
    print(f"Generated audio saved to {filename}")


# Example usage with frequency list for A4, G4, and F4 notes (440 Hz, 392 Hz, 349 Hz)
def main(notes):
    generate_notes(notes, "output.wav")
