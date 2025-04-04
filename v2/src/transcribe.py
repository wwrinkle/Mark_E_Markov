from threading import Thread
from stream_audio import stream_audio
from ui import render_notes
from process_audio_with_duration import process_audio_loop_with_duration
from logger import log

notes = []


def main():
    Thread(target=stream_audio).start()

    def append_notes(new_notes):
        log("NEW_NOTES", new_notes)
        global notes
        notes = notes + new_notes
        render_notes(notes)

    process_audio_loop_with_duration(append_notes)


main()
