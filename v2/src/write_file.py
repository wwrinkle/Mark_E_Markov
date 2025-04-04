from const import RATE, NUMPY_DATA_TYPE
from scipy.io.wavfile import write
import numpy


def write_wav_file(chunk, file_name):
    # # convert to min -1 max 1
    audio_ratio_chunk = chunk / numpy.max(numpy.abs(chunk))
    # largest number for data type
    max_value_for_data_type = numpy.iinfo(NUMPY_DATA_TYPE).max
    # multiply audio ratios by largest possible number
    # ensures that the entire range of the chunk is written to the .wav
    scaled = NUMPY_DATA_TYPE((audio_ratio_chunk * max_value_for_data_type).astype(int))
    # audio_data = numpy.frombuffer(b"".join(chunk), dtype=NUMPY_DATA_TYPE)

    write(f"{file_name}.wav", RATE, scaled)
