from chunk_manager import chunks
from const import RATE, MIN_FREQ, MAX_FREQ
import librosa
import scipy
import numpy
from queue import Empty
from write_file import write_wav_file
from matplotlib import pyplot

low_pass_filter = scipy.signal.butter(4, MAX_FREQ, btype="low", fs=RATE, output="sos")


def process_audio_loop_with_duration(on_notes):
    overflow_chunk = numpy.array([])
    while True:
        try:
            chunk_data = chunks.get_nowait()
            chunk = numpy.concat((overflow_chunk, chunk_data[1]))
            # chunk, sr = librosa.load(
            #     "/home/willie/Projects/Mark_E_Markov/v2/audio/c_scale.wav"
            # )
            onset_envelope = librosa.onset.onset_strength(y=chunk, sr=RATE)
            starts = librosa.onset.onset_detect(
                onset_envelope=onset_envelope, sr=RATE, backtrack=True
            )

            peaks = librosa.onset.onset_detect(onset_envelope=onset_envelope, sr=RATE)

            filtered_chunk = scipy.signal.sosfiltfilt(low_pass_filter, chunk)
            shifted_chunk = librosa.effects.pitch_shift(
                filtered_chunk, sr=RATE, n_steps=12
            )
            f0, voiced_flag, voiced_probs = librosa.pyin(
                shifted_chunk,
                sr=RATE,
                fmin=MIN_FREQ,
                fmax=MAX_FREQ,
                fill_na=0,
            )

            ends = numpy.array([])
            pitches = numpy.array([])
            for index, (start_index, peak_index) in enumerate(zip(starts, peaks)):
                start_onset_value = onset_envelope[start_index]
                end_index = peak_index

                # first frame after peak that is less than or equal to the start value
                try:
                    end_index = (
                        numpy.where(onset_envelope[peak_index:] <= start_onset_value)[
                            0
                        ][0]
                        + peak_index
                    )
                except IndexError:
                    pass

                try:
                    # frame before next index
                    next_start_index = starts[index + 1] - 1
                    # choose the lowest value between the next start, the calculated end and the last frame of the chunk
                    end_index = min(next_start_index, end_index, len(onset_envelope))
                except IndexError:
                    pass

                # are more than half the frames marked as voiced
                is_voiced = voiced_flag[start_index:end_index].mean() > 0.5
                if is_voiced:
                    ends = numpy.append(ends, end_index)
                    note_chunk = f0[start_index:end_index]

                    average_frequency = note_chunk.mean()
                    # transpose back down an octave to compensate for shifting up an octave before analysis
                    pitch = librosa.hz_to_note(average_frequency / 2)
                    pitches = numpy.append(pitches, pitch)
                else:
                    # if not voiced, delete
                    starts = numpy.delete(starts, index)
                    peaks = numpy.delete(peaks, index)
            starts = starts[: len(ends)]

            pitches = pitches[: len(ends)]

            onset_end_index = len(onset_envelope)
            if len(ends) > 0:
                onset_end_index = int(ends[-1])
            onset_envelope = onset_envelope[:onset_end_index]
            overflow_index = librosa.frames_to_samples(len(onset_envelope))
            overflow_chunk = chunk[overflow_index:]
            chunk = chunk[:overflow_index]
            tempo, beat_frames = librosa.beat.beat_track(y=chunk, sr=RATE, trim=False)

            sections = numpy.split(
                onset_envelope, numpy.sort(numpy.concat((starts, ends)).astype(int))
            )

            frame_index = 0
            pitch_index = 0
            notes = []
            for section in sections:
                note_duration = len(section)
                if note_duration == 0:
                    continue
                end_index = frame_index + note_duration

                left_offset_beat_end = end_index
                try:
                    left_offset_beat_end = beat_frames[beat_frames > frame_index][0]
                except IndexError:
                    pass
                left_offset_frame_duration = left_offset_beat_end - frame_index
                left_offset_beat_start = 0
                try:
                    left_offset_beat_start = beat_frames[beat_frames < frame_index][-1]
                except IndexError:
                    pass
                left_offset_beat_duration = (
                    left_offset_beat_end - left_offset_beat_start
                )
                left_offset_beat_ratio = (
                    left_offset_frame_duration / left_offset_beat_duration
                )

                right_offset_beat_start = 0
                try:
                    right_offset_beat_start = beat_frames[beat_frames < end_index][-1]
                except IndexError:
                    pass
                right_offset_frame_duration = end_index - right_offset_beat_start
                right_offset_beat_end = end_index
                try:
                    right_offset_beat_end = beat_frames[beat_frames > end_index][0]
                except IndexError:
                    pass
                right_offset_beat_duration = (
                    right_offset_beat_end - right_offset_beat_start
                )
                right_offset_beat_ratio = (
                    right_offset_frame_duration / right_offset_beat_duration
                )

                pitch = None
                # if current frame index is in starts array it is the beginning of a pitch
                if frame_index in starts:
                    pitch = pitches[pitch_index]
                    pitch_index += 1

                start_sample = librosa.frames_to_samples(frame_index)
                end_sample = librosa.frames_to_samples(end_index)
                sound_chunk = chunk[start_sample:end_sample]

                if len(sound_chunk) > 0:
                    write_wav_file(sound_chunk, f"sec-{str(index)}.wav")

                # number of beats within start and end of a note
                note_beats = len(
                    beat_frames[
                        (
                            (beat_frames > frame_index)
                            & (beat_frames < frame_index + note_duration)
                        )
                    ]
                )
                beat_duration = {"beats": max(note_beats - 1, 0)}

                beat_duration["left_offset"] = None
                if left_offset_frame_duration > 0:
                    beat_duration["left_offset"] = {
                        "frames": left_offset_frame_duration,
                        "beat_ratio": left_offset_beat_ratio,
                    }

                beat_duration["right_offset"] = None
                if right_offset_frame_duration > 0:
                    beat_duration["right_offset"] = {
                        "frames": right_offset_frame_duration,
                        "beat_ratio": right_offset_beat_ratio,
                    }

                notes.append(
                    {
                        "pitch": pitch,
                        "start_index": frame_index,
                        "frame_duration": note_duration,
                        "beat_duration": beat_duration,
                    }
                )

                frame_index += note_duration

            # plotting code
            # notes_y = numpy.array([])
            # for note in notes:
            #     if note["pitch"] is None:
            #         notes_y = numpy.append(notes_y, numpy.zeros(note["frame_duration"]))
            #     else:
            #         note_frequency = librosa.note_to_hz(note["pitch"])
            #         notes_y = numpy.append(
            #             notes_y, numpy.array(note["frame_duration"] * [note_frequency])
            #         )
            # times = librosa.times_like(notes_y, sr=RATE)
            # fig, ax = pyplot.subplots(nrows=2, sharex=True)
            # D = librosa.amplitude_to_db(numpy.abs(librosa.stft(chunk)), ref=numpy.max)
            # img = librosa.display.specshow(
            #     D, x_axis="time", y_axis="log", ax=ax[0], sr=RATE
            # )
            # ax[0].plot(times, notes_y, label="f0", color="cyan", linewidth=3)
            # fig.colorbar(img, ax=ax, format="%+2.f dB")
            # ax[1].plot(
            #     times, librosa.util.normalize(onset_envelope), label="Onset strength"
            # )
            # ax[1].vlines(
            #     times[beat_frames[beat_frames < len(times)]],
            #     0,
            #     1,
            #     alpha=0.5,
            #     color="r",
            #     linestyle="--",
            #     label="Beats",
            # )
            # ax[1].vlines(
            #     times[numpy.array([n["start_index"] for n in notes])],
            #     0,
            #     1,
            #     alpha=0.5,
            #     color="b",
            #     linestyle="solid",
            #     label="Notes",
            # )
            # pyplot.show()
            # end plotting code

            if len(notes) > 0:
                on_notes(notes)

        except Empty:
            pass
