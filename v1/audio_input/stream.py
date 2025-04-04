from audio_input.ChunkManager import ChunkManager
from core.const import CHANNELS, CHUNK_SIZE, FORMAT, RATE
from core.pyaudio_client import client as pyaudio_client
from audio_input.device import get_device_index


def stream_audio():
    device_index = get_device_index()
    # Open a stream for input
    stream = pyaudio_client.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
        input_device_index=device_index,
    )

    print("Recording audio...")
    # Read audio data in chunks
    while True:
        chunk = stream.read(CHUNK_SIZE)
        ChunkManager().append_chunk(chunk)
