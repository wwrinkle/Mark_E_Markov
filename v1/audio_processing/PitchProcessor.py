import librosa
import numpy
from core.const import (
    HOP_LENGTH,
    LOWER_FREQUENCY_CUTOFF,
    RATE,
    UPPER_FREQUENCY_CUTOFF,
    PITCH_TOLERANCE,
    MINIMUM_NOTE_LENGTH,
)
import statistics


class PitchProcessor(object):

    def __init__(self):
        self.notes = []
        self.frames_window = []

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(PitchProcessor, cls).__new__(cls)
        return cls.instance

    def frames_to_note(self, frames):
        note_average = statistics.mean(frames)
        return librosa.hz_to_note(note_average, octave=False)

    def dump_frames_to_note(self, note_value, is_rest=False):
        if len(self.frames_window) > MINIMUM_NOTE_LENGTH:
            if is_rest:
                self.notes.append("r")
            else:
                self.notes.append(self.frames_to_note(self.frames_window))
        self.frames_window = [note_value]

    def determine_onsets(self, chunk):
        onset_envelope = librosa.onset.onset_strength(y=chunk, sr=RATE)
        return librosa.onset.onset_detect(chunk, onset_envelope=onset_envelope, sr=RATE)

    def get_pitch_of_chunk(self, chunk):
        print(chunk.size)
        f0, voiced_flag, voiced_probabilities = librosa.pyin(
            chunk,
            sr=RATE,
            fmin=LOWER_FREQUENCY_CUTOFF,
            fmax=UPPER_FREQUENCY_CUTOFF,
            hop_length=HOP_LENGTH,
        )
        # pitch = librosa.hz_to_note(statistics.mean(curve), octave=False)
        print(f0, voiced_flag)
        return 'foo'

    def process(self, chunk):
        print(chunk)
        print(f"total chunk size {chunk.size}")
        pitches = []
        for onset in self.determine_onsets(chunk):
            onset_chunk = chunk[onset - 100 : onset + 250]
            pitches.append(self.get_pitch_of_chunk(onset_chunk))
        return pitches
        # self.notes = []
        # self.frames_window = []
        # # print(f"incoming chunk for pitch processing {len(chunk)}")
        # f0, voiced_flag, voiced_probabilities = librosa.pyin(
        #     chunk,
        #     sr=RATE,
        #     fmin=LOWER_FREQUENCY_CUTOFF,
        #     fmax=UPPER_FREQUENCY_CUTOFF,
        #     hop_length=HOP_LENGTH,
        # )
        # print(f"pyin returned {f0.size} frames")
        # for index, flag in enumerate(voiced_flag):
        #     note_value = "r"
        #     if flag and not numpy.isnan(f0[index]):
        #         note_value = librosa.hz_to_note(f0[index], octave=False)
        #     self.notes.append(note_value)

        # return self.notes
