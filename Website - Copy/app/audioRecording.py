import sounddevice as sd
import numpy as np
import wave

def record_audio(filename = "audio_file.wav", duration = 5, samplerate = None):
    """
    Records audio to the specified file. Only save as .wav files.
    :param samplerate: Sample rate (integer). Default None, will check what samplerate it defaults to
    :param filename: File name of the new audio file (string). Default audio_file.wav
    :param duration: Duration of the recording (integer). Default 5 seconds
    :return: None
    """
    try:
        audio_data = sd.rec(int(duration * samplerate), samplerate = samplerate, channels = 1, dtype = np.int16)
        sd.wait()

        with wave.open(filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(audio_data.tobytes())


    except Exception as e:
        print(f"Some error happened: {e}")

#So if the user has more than one input device we need a way to set it in the website, for now this works,
#but we should revisit once the website is finished
def set_input_device(device_id):
    """
    Sets the input device from which audio will be recorded.
    :param device_id: ID of the device to be selected (integer).
    :return: None
    """
    try:
        sd.default.device = device_id
    except Exception as e:
        print(f"Error selecting input device: {e}")

def get_samplerate(device_id):
    """
    Returns the samplerate of the specified device
    :param device_id: ID of the device which samplerate is being returned (integer).
    :return: Samplerate of the device (integer).
    """
    try:
        return int(sd.query_devices(device_id)["default_samplerate"])
    except Exception as e:
        print(f"Error returning samplerate: {e} ")
        print("Returning default samplerate of 44100")
        return 44100

#Small testing to make sure this works!
if __name__ == "__main__":
    set_input_device(1)
    samrate = get_samplerate(1)
    record_audio("test.wav", 5, samrate)
