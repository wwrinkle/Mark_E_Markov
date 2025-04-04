import matplotlib

matplotlib.use("Qt5Agg")
import matplotlib.pyplot as pyplot
import librosa

from core.const import RATE


def display_chunk(chunk, onset_frames, pitch_chunks):
    fig, ax = pyplot.subplots(nrows=1)
    librosa.display.waveshow(chunk, sr=RATE, ax=ax)
    onset_times = librosa.samples_to_time(onset_frames, sr=RATE)
    print(f"***onset times {len(onset_times)}***")
    print(onset_times)
    y_min, y_max = pyplot.gca().get_ylim()

    for onset_frame in onset_frames:
        ax.axvline(x=onset_frame / RATE, color="b")
    for pitch_chunk_frame in pitch_chunks:
        ax.axvline(x=pitch_chunk_frame / RATE, color="g")
    # pyplot.vlines(onset_times, y_min, y_max, color="r")
    # pyplot.vlines(pitch_chunks, y_min, y_max, color="g")
    pyplot.show(block=True)
