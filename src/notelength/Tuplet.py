from fractions import Fraction

class Tuplet:
    def __init__(self, note, is_compound):
        self.denominator = int(note.group("tuplet_denominator"))
        self.numerator = int(note.group("tuplet_numerator")) if note.group(
            "tuplet_numerator") else self.get_numerator(is_compound)
        self.count = int(note.group("tuplet_count")) if note.group(
            "tuplet_count") else self.denominator

    def get_numerator(self, is_compound):
        if self.denominator in [2, 4, 8]:
            return 3
        elif self.denominator in [3, 6]:
            return 2
        elif is_compound:
            return 3
        else:
            return 2

    def get_count(self):
        return self.count

    def get_ratio(self):
        return Fraction(self.numerator, self.denominator)
