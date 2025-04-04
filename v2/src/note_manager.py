from const import NOTES_TO_PROCESS


notes = []


def append_notes(incoming_notes):
    global notes
    notes = notes + incoming_notes
    return notes[-NOTES_TO_PROCESS:]


def get_notes():
    global notes
    return notes[-NOTES_TO_PROCESS:]
