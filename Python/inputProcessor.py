# Takes the raw audio file and converts it into notes

import librosa
import noteUtils



def detect_notes(audio_file):
    """
        Takes an audio file and returns the detected pitches written as notes in a list.
        :param audio_file: Path to the audio file to be loaded.
        :return notes: List of notes written (e.g. A#, B).
        """
    # Load the audio file with librosa
    y, sr = librosa.load(audio_file)

    # Compute the Short-Time Fourier Transform (STFT) of the audio signal
    D = librosa.stft(y)

    # Compute the magnitude spectrogram
    magnitudes, _ = librosa.magphase(D)

    # Get the index of the maximum magnitude for each frame
    # Using librosa's harmonic extraction method to avoid out of bounds
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)

    # You might want to extract the most prominent pitch per frame
    pitch = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()  # Get the index of the most prominent frequency
        pitch.append(pitches[index, t])  # Store the pitch (frequency) corresponding to that index

    notes = []
    hzs = []
    for i in pitch:
        if (i == 0 ): # IMPORTANT! Keeps any "Nones" from entering, but will hide all gaps.
            continue
        notes.append(noteUtils.hz_to_note_name(i))
        hzs.append(i)

    # Return the detected pitches
    return notes


def main():
    # Test with an audio file
    audio_file = "input.wav"
    notes = detect_notes(audio_file)
    print("Detected Notes:", notes)
    return notes
