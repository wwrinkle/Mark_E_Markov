import numpy
from time import time
from const import NUMPY_DATA_TYPE, RATE, CHUNK_SECONDS
from queue import Queue

TEMPO_CHUNK_SIZE = (RATE * CHUNK_SECONDS) * 1
chunks = Queue(maxsize=RATE * CHUNK_SECONDS)
tempo_chunks = Queue(maxsize=RATE * CHUNK_SECONDS)
current_tempo_chunk = None


def append_chunk(chunk):
    global chunks, TEMPO_CHUNK_SIZE, current_tempo_chunk
    chunk_array = numpy.frombuffer(chunk, dtype=NUMPY_DATA_TYPE)
    chunk_array = chunk_array / numpy.max(numpy.abs(chunk_array))

    # manage larger tempo chunk queue
    if current_tempo_chunk is None:
        current_tempo_chunk = (time(), chunk_array)
    elif len(current_tempo_chunk[1]) < TEMPO_CHUNK_SIZE:
        numpy.append(current_tempo_chunk[1], chunk_array)
    else:
        tempo_chunks.put(current_tempo_chunk)
        current_tempo_chunk = None

    chunks.put((time(), chunk_array))
