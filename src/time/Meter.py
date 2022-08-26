from time.Length import Length


class Meter(Length):
    def __init__(self, str):
        super().__init__(str)

    def is_compound(self):
        return self.numerator % 3 == 0 and self.denominator == 8

    def get_bar_length(self, base_length):
        return self.get() / base_length.get()
