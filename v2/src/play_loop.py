from note_manager import get_notes
from chunk_manager import tempo_chunks
from const import NOTES_TO_PROCESS, TEMPOS_TO_PROCESS
from queue import Empty
from process_audio import get_tempo
from sequence_player import play_sequence, is_playing
from time import sleep
from markov_tools import generate_sequence
import numpy


def play_loop():

    next_sequence = None
    tempos = numpy.array([])
    last_recorded_beat = None

    while True:
        if next_sequence is not None and is_playing[0]:
            sleep(0.25)
            continue

        if is_playing[0] is False and next_sequence is not None:
            play_sequence(next_sequence[0], next_sequence[1], next_sequence[2])
            next_sequence = None

        if next_sequence is None:
            notes = get_notes()
            if len(notes) >= NOTES_TO_PROCESS:
                try:
                    tempo_chunk = tempo_chunks.get_nowait()
                    tempo_data = get_tempo(tempo_chunk[1], tempo_chunk[0])
                    last_recorded_beat = tempo_data["last_beat"]
                    tempos = numpy.append(tempos, tempo_data["tempo"])
                except Empty:
                    pass

                if last_recorded_beat is not None:
                    sequence = generate_sequence(notes)
                    next_sequence = (
                        sequence,
                        tempos[-TEMPOS_TO_PROCESS:].mean(),
                        last_recorded_beat,
                    )
            else:
                sleep(0.25)
