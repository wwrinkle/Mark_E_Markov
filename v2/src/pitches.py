def quarter_step_above(freq):
    return freq * 2 ** (1 / 24)


def quarter_step_below(freq):
    return freq / 2 ** (1 / 24)
