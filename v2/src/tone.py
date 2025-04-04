import pyaudio
import numpy as np


def generate_tone(frequency, duration, sample_rate=44100, amplitude=1):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, output=True)

    num_samples = int(sample_rate * duration)
    samples = (
        amplitude * np.sin(2 * np.pi * np.arange(num_samples) * frequency / sample_rate)
    ).astype(np.float32)

    stream.write(samples.tobytes())

    stream.stop_stream()
    stream.close()

    p.terminate()
