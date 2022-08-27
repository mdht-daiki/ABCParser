from enum import Enum


class Accidental(str, Enum):
    DOUBLE_SHARP = "double_sharp"
    SHARP = "sharp"
    NATURAL = "natural"
    FLAT = "flat"
    DOUBLE_FLAT = "double_flat"