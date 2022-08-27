from fractions import Fraction


class Length:
    def __init__(self, length, num=None):
        if isinstance(length, str) and "/" in length:
            self.numerator, self.denominator = (
                int(n) for n in length.split("/"))
        elif isinstance(length, Fraction):
            self.numerator = length.numerator
            self.denominator = length.denominator
        elif isinstance(length, Length) and num is not None:
            self.numerator = length.get_numerator() * num
            self.denominator = length.get_denominator()

    def get(self):
        return Fraction(self.numerator, self.denominator)

    def get_numerator(self):
        return self.numerator

    def get_denominator(self):
        return self.denominator

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"
