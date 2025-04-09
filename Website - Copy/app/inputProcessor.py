# Takes the raw audio file and converts it into notes
import os
import subprocess

import soundfile as sf
import librosa
import ffmpeg

import noteUtils




def detect_notes(audio_file):
    """
        Takes an audio file and returns the detected pitches written as notes in a list.
        :param audio_file: Path to the audio file to be loaded.
        :return notes: List of notes written (e.g. A#, B).
        """
    # Load the audio file with librosa
    # Load the audio file with soundfile (replaces librosa.load)
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
    for i in pitch:
        notes.append(noteUtils.hz_to_note_name(i))

    # Return the detected pitches
    return notes


def main():
    # Test with an audio file
    audio_file = "inputs/990740_user.wav"
    notes = detect_notes(audio_file)
    print("Detected Notes:", notes)
    return notes

if __name__ == "__main__":
    main()