from enum import Enum, auto


key_accidental_order = ["F", "C", "G", "D", "A", "E", "B"]


class Accidental(Enum):
    DOUBLE_SHARP = auto()
    SHARP = auto()
    NATURAL = auto()
    FLAT = auto()
    DOUBLE_FLAT = auto()


def get_default_accidental(accidental_num, pitch):
    if accidental_num < 0 and pitch in key_accidental_order[accidental_num:]:
        return Accidental.FLAT
    elif accidental_num > 0 and pitch in key_accidental_order[:accidental_num]:
        return Accidental.SHARP
    return Accidental.NATURAL
