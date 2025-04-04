import threading
from stream_audio import stream_audio
from process_loop import process_audio_loop
from play_loop import play_loop
from logger import log


if __name__ == "__main__":
    log("STARTING AUDIO STREAM THREAD")
    threading.Thread(target=stream_audio).start()
    log("STARTING PLAY LOOP")
    threading.Thread(target=play_loop).start()
    log("STARTING AUDIO PROCESSING LOOP")
    process_audio_loop()
