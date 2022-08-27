from notelength.Length import Length


class Offset(Length):
    def __init__(self, base_length, offset=None, duration=None):
        self.base_length = base_length
        if offset is None:
            self.numerator = 0
            self.denominator = self.base_length.get_denominator()
        elif isinstance(offset, Offset) and isinstance(duration, Length):
            a = offset.get() + duration.get()
            self.numerator = a.numerator
            self.denominator = a.denominator

    def get_next_offset(self, duration):
        return Offset(self.base_length, self, duration)
