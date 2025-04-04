from chunk_manager import chunks
from process_audio import get_notes, get_tempo
from note_manager import append_notes
from markov_tools import generate_sequence
from const import (
    SEQUENCE_GENERATION_PROBABILITY,
    CHUNKS_TO_ANALYZE_TEMPO,
    TEMPOS_TO_PROCESS,
    RATE,
)
from random import random
from sequence_player import play_sequence, is_playing
from queue import Empty
import numpy
from logger import log


def process_audio_loop():
    chunk_index = 0
    overflow_chunk = numpy.array([])
    # tempo_chunk = numpy.array([])
    # tempo_chunk_end_times = []
    # last_tempos = numpy.array([])

    while True:
        try:
            chunk_data = chunks.get_nowait()
            log(f"PROCESSING CHUNK {chunk_index}")
            # tempo_chunk = numpy.concat((tempo_chunk, chunk_data[1]))
            # tempo_chunk_end_times.append(chunk_data[0])
            # tempo_chunk_end_times = tempo_chunk_end_times[-CHUNKS_TO_ANALYZE_TEMPO:]
            # if len(tempo_chunk) > (CHUNKS_TO_ANALYZE_TEMPO * RATE):
            #     tempo_chunk = tempo_chunk[RATE:]
            # average_tempo = None
            # if len(last_tempos) > 0:
            #     average_tempo = last_tempos.mean()
            # tempo_data = get_tempo(tempo_chunk, tempo_chunk_end_times[0])
            # last_tempos = numpy.append(last_tempos, tempo_data["tempo"])
            # if len(last_tempos) > TEMPOS_TO_PROCESS:
            #     last_tempos = last_tempos[1:]
            notes_data = get_notes(numpy.append(chunk_data[1], overflow_chunk))
            notes = append_notes(notes_data["notes"])
            log(f"NOTES: {", ".join(notes)}")
            # if (
            #     len(notes) > 0
            #     and random() < SEQUENCE_GENERATION_PROBABILITY
            #     and not is_playing[0]
            # ):
            #     sequence = generate_sequence(notes)
            #     # recalculate average tempo using latest tempo
            #     average_tempo = last_tempos.mean()
            #     play_sequence(sequence, average_tempo, tempo_data["last_beat"])

            overflow_chunk = notes_data["overflow"]
            chunk_index += 1
        except Empty:
            pass
        except Exception as e:
            log("!!! UNKNOWN EXCEPTION !!!", e)
            raise e
