from chunk_manager import append_chunk
import pyaudio
from device import get_device_index
from const import FORMAT, CHANNELS, RATE, CHUNK_SECONDS
from logger import log


def stream_audio():
    client = pyaudio.PyAudio()
    device_index = get_device_index(client)

    def stream_callback(in_data, frame_count, time_info, status_flags):
        append_chunk(in_data)
        return (None, pyaudio.paContinue)

    # Open a stream for input
    stream = client.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=int(RATE * CHUNK_SECONDS),
        input_device_index=device_index,
        stream_callback=stream_callback,
    )

    log("RECORDING AUDIO...")
    stream.start_stream()

    while stream.is_active():
        pass

    stream.stop_stream()
    stream.close()
    client.terminate()
