from audio_input.stream import stream_audio
from audio_processing.processor import process_audio
import threading
from queue import Queue
from core.const import BUFFER_SIZE


if __name__ == "__main__":
    print("starting audio stream thread")
    threading.Thread(target=stream_audio).start()
    print("starting audio processing")
    process_audio()
