import subprocess
from decimal import Decimal
import os


def octave_number_to_liypond(octave):
    if octave == 3:
        return ""
    elif octave < 3:
        number_of_commas = 3 - octave
        return "," * number_of_commas
    else:
        number_of_apostrophes = octave - 3
        return "'" * number_of_apostrophes


def beat_ratio_to_lilypond_subdivision(beat_ratio, pitch):
    if beat_ratio < 0.12:
        return ""
    elif beat_ratio < 0.29:
        return f"{pitch}16"
    elif beat_ratio < 0.57:
        return f"{pitch}8"
    elif beat_ratio < 0.86:
        return f"{pitch}8."
    else:
        return f"{pitch}4"


def subdivision_to_lilypond_duration(subdivision, pitch="r"):
    if subdivision == Decimal(1 / 4):
        return f"{pitch}8"
    elif subdivision == Decimal(1 / 3):
        return f"\\tuplet 3/2 {{ {pitch}8 }}"
    elif subdivision == Decimal(1 / 2):
        return f"{pitch}2"
    elif subdivision == Decimal(2 / 3):
        return f"\\tuplet 3/2 {{ {pitch}4 }}"
    elif subdivision == Decimal(3 / 4):
        return f"{pitch}4."


def beat_length_to_lilypond_duration(beat_length, pitch="r"):
    length_strings = [
        f"{pitch}4",
        f"{pitch}2",
        f"{pitch}2.",
        f"{pitch}1",
        f"{pitch}1..",
        f"{pitch}1.",
        f"{pitch}1~ {pitch}2.",
        f"{pitch}\\breve",
    ]

    if beat_length >= len(length_strings):
        return length_strings[-1]
    else:
        beat_index = beat_length - 1
        return length_strings[beat_index]


def pitch_and_duration_to_lilypond_note(pitch, duration):
    lilypond_note = ""
    if duration["left_offset"] is not None:
        if duration["beats"] == 0 and duration["right_offset"] is not None:
            duration["left_offset"]["beat_ratio"] += duration["right_offset"][
                "beat_ratio"
            ]
            duration["left_offset"]["frames"] += duration["right_offset"]["frames"]
            duration["right_offset"] = None
        lilypond_note += beat_ratio_to_lilypond_subdivision(
            duration["left_offset"]["beat_ratio"], pitch
        )

    if duration["beats"] > 0:
        if len(lilypond_note) > 0:
            lilypond_note += "~ "
        lilypond_note += beat_length_to_lilypond_duration(duration["beats"], pitch)

    if duration["right_offset"] is not None:
        if len(lilypond_note) > 0:
            lilypond_note += "~ "
        lilypond_note += beat_ratio_to_lilypond_subdivision(
            duration["right_offset"]["beat_ratio"], pitch
        )

    return lilypond_note


def notes_to_lilypond_file(notes):
    lilypond_notes = []
    for note in notes:
        lilypond_pitch = "r"
        if note["pitch"] is not None:
            octave = int(note["pitch"][-1])
            lilypond_octave = octave_number_to_liypond(octave)
            lilypond_pitch = (
                note["pitch"][:-1].lower().replace("♯", "s") + lilypond_octave
            )

        lilypond_note = pitch_and_duration_to_lilypond_note(
            lilypond_pitch, note["beat_duration"]
        )
        lilypond_notes.append(lilypond_note)

    file_content = f"""
    \\version "2.24.3"
    \\language "english"

    \\header {{
        title = "Output"
    }}

    {{
        \\time 4/4
        \\numericTimeSignature
        \\clef bass
        {" ".join(lilypond_notes)}
    }}
    """
    file = open("output.ly", "w")
    file.write(file_content)
    file.close()


def render_notes(notes):
    try:
        os.remove("output.ly")
    except FileNotFoundError:
        pass
    notes_to_lilypond_file(notes)
    try:
        subprocess.run("lilypond output.ly && code output.pdf", shell=True)
    except Exception as e:
        raise e
