from notelength.Length import Length


class Tuplet(Length):
    def __init__(self, denominator, numerator):
        self.denominator = denominator
        self.numerator = numerator

    def mul(self, length):
        return Length(length.get() * self.get())


def get_numerator(denominator, is_compound):
    if denominator in [2, 4, 8]:
        return 3
    elif denominator in [3, 6]:
        return 2
    elif is_compound:
        return 3
    else:
        return 2


def create_tuplet(tune, d):
    denominator = d["tuplet_denominator"]
    numerator = d["tuplet_numerator"] or get_numerator(
        denominator, tune.get("meter").is_compound)
    count = d["tuplet_count"] or denominator
    return Tuplet(denominator, numerator), count
