import tkinter as tk
from tkinter import simpledialog, messagebox
import sounddevice as sd
import wave
import numpy as np
import noteSelector
import toneGenerator
import inputProcessor
import inputGrader
import outputFormatter
import os


# Initialize main app window
class MultiPageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multipage Interface")
        self.geometry("400x300")
        self.sequence_length = 5
        self.lower_bound = 40
        self.upper_bound = 80
        self.step = 1
        self.notes = []
        self.recording = False
        self.create_first_page()

    def create_first_page(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Sequence Length:").pack()
        self.seq_length_entry = tk.Entry(self)
        self.seq_length_entry.insert(0, "5")
        self.seq_length_entry.pack()

        tk.Label(self, text="Lower Bound:").pack()
        self.lower_bound_entry = tk.Entry(self)
        self.lower_bound_entry.insert(0, "40")
        self.lower_bound_entry.pack()

        tk.Label(self, text="Upper Bound:").pack()
        self.upper_bound_entry = tk.Entry(self)
        self.upper_bound_entry.insert(0, "80")
        self.upper_bound_entry.pack()

        tk.Label(self, text="Step:").pack()
        self.step_entry = tk.Entry(self)
        self.step_entry.insert(0, "1")
        self.step_entry.pack()

        tk.Button(self, text="Submit", command=self.submit_values).pack()

    def submit_values(self):
        try:
            self.sequence_length = int(self.seq_length_entry.get())
            self.lower_bound = int(self.lower_bound_entry.get())
            self.upper_bound = int(self.upper_bound_entry.get())
            self.step = int(self.step_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid integers.")
            return

        self.notes = noteSelector.get_notes(self.sequence_length, self.lower_bound, self.upper_bound, self.step)
        toneGenerator.main(self.notes)
        if os.path.exists("output.wav"):
            self.create_second_page()
        else:
            messagebox.showerror("Error", "Failed to generate output.wav")

    def create_second_page(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Button(self, text="Play output.wav", command=self.play_audio).pack()
        tk.Button(self, text="Next", command=self.create_third_page).pack()

    def play_audio(self):
        with wave.open('output.wav', 'rb') as wf:
            frames = wf.readframes(wf.getnframes())
            data = np.frombuffer(frames, dtype=np.int16)
            sd.play(data, wf.getframerate())
            sd.wait()

    def create_third_page(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.record_button = tk.Button(self, text="Start Recording", command=self.toggle_recording)
        self.record_button.pack()

    def toggle_recording(self):
        if not self.recording:
            self.recording = True
            self.record_button.config(text="Stop Recording")
            self.start_recording()
        else:
            self.recording = False
            self.record_button.config(text="Start Recording")
            self.stop_recording()

    def start_recording(self):
        self.audio_data = []
        self.stream = sd.InputStream(callback=self.audio_callback, channels=1, dtype='int16', samplerate=44100)
        self.stream.start()

    def stop_recording(self):
        self.stream.stop()
        self.stream.close()
        audio = np.concatenate(self.audio_data, axis=0)
        with wave.open('input.wav', 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(44100)
            wf.writeframes(audio.tobytes())
        self.process_input()


    def audio_callback(self, indata, frames, time, status):
        self.audio_data.append(indata.copy())



    def process_input(self):
        input_notes, input_hz = inputProcessor.main()
        grade = inputGrader.input_grading(self.notes, input_notes)
        outputFormatter.setup_formats(self.notes, input_notes,input_hz)
        if os.path.exists("output.png"):
            self.create_final_page(grade)
        else:
            messagebox.showerror("Error", "Failed to generate output.png")

    def create_final_page(self, grade):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text=f"Grade: {grade}").pack()
        img = tk.PhotoImage(file="output.png")
        tk.Label(self, image=img).pack()
        self.mainloop()


def runInterface():
    app = MultiPageApp()
    app.mainloop()
