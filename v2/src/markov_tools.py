from itertools import count
from random import randint, choice
from const import MIN_OUTPUT_LENGTH, MAX_OUTPUT_LENGTH, MAX_REPEAT_NOTES


def generate_transitions_table(notes):
    transitions = {}
    for i, note in zip(count(), notes[:-1]):
        next_note = notes[i + 1]
        if note in transitions:
            transitions[note].append(next_note)
        else:
            transitions[note] = [next_note]
    return transitions


def generate_sequence(notes):
    notes = [n for n in notes if n is not None]
    sequence_length = randint(MIN_OUTPUT_LENGTH, MAX_OUTPUT_LENGTH)
    transitions = generate_transitions_table(notes)
    available_transitions = list(transitions.keys())
    if len(available_transitions) == 0:
        return []
    sequence = [choice(available_transitions)]
    for i in range(1, sequence_length):
        last_note = sequence[i - 1]
        notes_have_repeated = (
            len(sequence) > MAX_REPEAT_NOTES
            and len(set(sequence[-MAX_REPEAT_NOTES:])) == 1
        )
        potential_next_notes = []
        if last_note not in transitions and notes_have_repeated:
            potential_next_notes = [
                n for n in list(transitions.keys()) if n != last_note
            ]
        elif last_note not in transitions:
            potential_next_notes = list(transitions.keys())
        elif notes_have_repeated:
            potential_next_notes = [n for n in transitions[last_note] if n != last_note]
        else:
            potential_next_notes = transitions[last_note]

        if len(potential_next_notes) == 0:
            potential_next_notes = list(transitions.keys())

        next_note = choice(potential_next_notes)
        sequence.append(next_note)

    return sequence
