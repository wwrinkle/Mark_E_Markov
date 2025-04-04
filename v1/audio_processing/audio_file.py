from core.const import RATE
from scipy.io.wavfile import write
import numpy


def chunk_to_wav_file(chunk, file_index):
    # convert to min -1 max 1
    audio_ratio_chunk = chunk / numpy.max(numpy.abs(chunk))
    # largest number for data type
    max_value_for_data_type = numpy.iinfo(numpy.int32).max
    # multiply audio ratios by largest possible number
    # ensures that the entire range of the chunk is written to the .wav
    scaled = numpy.int32((audio_ratio_chunk * max_value_for_data_type).astype(int))
    write(f"audio_sample_{file_index}.wav", RATE, scaled)
