from notelength.Length import Length


class Meter(Length):
    def is_compound(self):
        return self.numerator % 3 == 0 and self.denominator == 8

    def get_bar_length(self, base_length):
        return self.get() / base_length.get()
