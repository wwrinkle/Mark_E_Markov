from musicpy import chord, write
from const import MIDI_INSTRUMENT
from time import time
import pygame
import threading
from logger import log

is_playing = [False]


def play_midi_with_delay(midi_file, delay):
    global is_playing
    pygame.mixer.music.load(midi_file)
    pygame.time.delay(int(delay * 1000))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.delay(100)
    is_playing[0] = False


def play_sequence(notes, tempo, last_beat):
    global is_playing
    is_playing[0] = True

    transposed_notes = []
    for note in notes:
        octave = int(note[-1:])
        new_octave = octave + 1
        transposed_notes.append(note[:-1] + str(new_octave))

    notes_string = ", ".join(transposed_notes).replace("♯", "#")
    lengths = [1 / 4 for n in notes]
    try:
        midi_file = write(
            chord(notes_string, interval=lengths, duration=lengths),
            bpm=tempo,
            instrument=MIDI_INSTRUMENT,
            save_as_file=False,
        )
        midi_file.seek(0)

        now = time()
        beat_duration = 60 / tempo
        seconds_since_last_recorded_beat = now - last_beat
        delay = 0
        if seconds_since_last_recorded_beat < beat_duration:
            delay = beat_duration - seconds_since_last_recorded_beat
        else:
            seconds_since_last_theoretical_beat = (
                seconds_since_last_recorded_beat % beat_duration
            )
            delay = beat_duration - seconds_since_last_theoretical_beat
        log(
            f"ABOUT TO PLAY SEQUENCE: {", ".join(notes)} AT {str(int(tempo))} BPM IN {str(round(delay, 2))}s"
        )

        def thread_target():
            play_midi_with_delay(midi_file, delay)

        threading.Thread(target=thread_target).start()
    except Exception as e:
        log("SEQUENCE ERROR", e)
        raise e
