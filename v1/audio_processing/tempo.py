import librosa
import datetime
from core.const import RATE


def get_tempo(chunk, chunk_start_time, last_tempo=None):
    beat_data = []
    if last_tempo:
        beat_data = librosa.beat.beat_track(y=chunk, sr=RATE, start_bpm=last_tempo)
    else:
        beat_data = librosa.beat.beat_track(y=chunk, sr=RATE)
    last_beat_frame = beat_data[1][-1]
    last_beat_time_since_start = librosa.frames_to_time([last_beat_frame], sr=RATE)[0]
    last_beat_time = chunk_start_time + datetime.timedelta(
        seconds=last_beat_time_since_start
    )
    return [beat_data[0], last_beat_time]
