from fraction import Fraction


class Length:
    def __init__(self, str):
        self.numerator, self.denominator = (int(n) for n in str.split("/"))

    def get(self):
        return Fraction(self.numerator, self.denominator)
