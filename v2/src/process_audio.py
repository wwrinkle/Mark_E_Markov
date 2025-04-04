import librosa
from const import MIN_NOTE_LENGTH, RATE, MAX_FREQ, MIN_FREQ
from pitches import quarter_step_above, quarter_step_below
import scipy
import numpy
import math
from matplotlib import pyplot


low_pass_filter = scipy.signal.butter(4, MAX_FREQ, btype="low", fs=RATE, output="sos")


def get_notes(chunk):
    shifted_y = librosa.effects.pitch_shift(chunk, sr=RATE, n_steps=12)
    filtered_y = scipy.signal.sosfiltfilt(low_pass_filter, shifted_y)

    onset_envelope = librosa.onset.onset_strength(y=chunk, sr=RATE)
    starts = librosa.onset.onset_detect(
        onset_envelope=onset_envelope, sr=RATE, backtrack=True
    )
    peaks = librosa.onset.onset_detect(onset_envelope=onset_envelope, sr=RATE)
    ends = numpy.array([])
    for index, (start_index, peak_index) in enumerate(zip(starts, peaks)):
        start_onset_value = onset_envelope[start_index]
        end_index = peak_index

        # first frame after peak that is less than or equal to the start value
        try:
            end_index = (
                numpy.where(onset_envelope[peak_index:] <= start_onset_value)[0][0]
                + peak_index
            )
        except IndexError:
            pass

        try:
            # frame before next index
            next_start_index = starts[index + 1] - 1
            # choose the lowest value between the next start and the calculated
            end_index = min(next_start_index, end_index)
        except IndexError:
            pass

        end_index = int(end_index)
        if end_index > len(chunk):
            starts = numpy.delete(starts, index)
            peaks = numpy.delete(peaks, index)
            break
        ends = numpy.append(ends, end_index)

    f0, voiced_flag, voiced_probs = librosa.pyin(
        filtered_y,
        sr=RATE * 2,
        fmin=MIN_FREQ,
        fmax=MAX_FREQ,
    )
    starts = starts[: len(ends)]

    pitches = []
    for start_index, end_index in zip(starts, ends):
        start_index = int(start_index)
        end_index = int(end_index)

        if (
            # is long enough
            end_index - start_index > MIN_NOTE_LENGTH
            # is voiced
            and voiced_flag[start_index:end_index].mean() > 0.5
        ):
            frequency = f0[start_index:end_index].mean()
            if not math.isnan(frequency):
                pitch = librosa.hz_to_note(frequency)
                pitches.append(pitch)

    # for index, frame in enumerate(f0):
    #     current_note = None
    #     if len(last_note_frames) > 0 and None not in last_note_frames:
    #         current_note = sum(last_note_frames) / len(last_note_frames)

    #     # frame is a note
    #     if frame > 0 and voiced_probs[index] > 0.7:
    #         # lower frame by an octave
    #         frame = frame / 2
    #         # current_note is a float
    #         if isinstance(current_note, numpy.floating):
    #             upper_limit = quarter_step_above(current_note)
    #             lower_limit = quarter_step_below(current_note)

    #             if frame >= lower_limit and frame <= upper_limit:
    #                 last_note_frames.append(frame)
    #             else:
    #                 if len(last_note_frames) > MIN_NOTE_LENGTH:
    #                     note = librosa.hz_to_note(current_note)
    #                     notes.append(note)
    #                 last_note_frames = [frame]
    #         else:
    #             if len(last_note_frames) > MIN_NOTE_LENGTH:
    #                 notes.append(None)
    #             last_note_frames = [frame]
    #     # frame is silence
    #     else:
    #         # current_note is a note
    #         if current_note is float:
    #             if len(last_note_frames) > MIN_NOTE_LENGTH:
    #                 note = librosa.hz_to_note(current_note)
    #                 notes.append(note)
    #             last_note_frames = [None]
    #         else:
    #             last_note_frames.append(None)
    overflow_split_index = librosa.frames_to_samples(ends[-1])

    # plotting code
    # times = librosa.times_like(onset_envelope, sr=RATE)
    # fig, ax = pyplot.subplots(nrows=2, sharex=True)
    # D = librosa.amplitude_to_db(numpy.abs(librosa.stft(chunk)), ref=numpy.max)
    # img = librosa.display.specshow(D, x_axis="time", y_axis="log", ax=ax[0], sr=RATE)
    # ax[0].plot(times, f0, label="f0", color="cyan", linewidth=3)
    # fig.colorbar(img, ax=ax, format="%+2.f dB")
    # ax[1].plot(times, librosa.util.normalize(onset_envelope), label="Onset strength")
    # ax[1].vlines(
    #     times[starts],
    #     0,
    #     1,
    #     alpha=0.5,
    #     color="b",
    #     linestyle="solid",
    #     label="Starts",
    # )
    # ax[1].vlines(
    #     times[ends.astype(int)],
    #     0,
    #     1,
    #     alpha=0.5,
    #     color="r",
    #     linestyle="solid",
    #     label="Ends",
    # )
    # pyplot.show()
    # end plotting code

    return {"notes": pitches, "overflow": chunk[overflow_split_index:]}


def get_tempo(chunk, chunk_start):
    tempo, beats = librosa.beat.beat_track(y=chunk, sr=RATE)
    beat_times = librosa.frames_to_time(beats, sr=RATE)
    last_beat = chunk_start + beat_times[-1]
    return {"tempo": round(tempo[0]), "last_beat": last_beat}
