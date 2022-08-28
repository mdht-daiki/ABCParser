from pitch.Accidental import Accidental
tonic_order = ["Fb", "Cb", "Gb", "Db", "Ab", "Eb", "Bb",
               "F", "C", "G", "D", "A", "E", "B",
               "F#", "C#", "G#", "D#", "A#", "E#", "B#"]
scale_order = ["Lydian", "Ionian", "Mixolydian",
               "Dorian", "Aeolian", "Phrygian", "Locrian"]
key_accidental_order = ["F", "C", "G", "D", "A", "E", "B"]


def get_tonic_list(scale_type):
    start = scale_order.index(scale_type)
    end = start + 15
    return tonic_order[start:end]


def get_accidental_num(tonic, scale_type):
    tonic_list = get_tonic_list(scale_type)
    return tonic_list.index(tonic) - 7


class Key:
    def __init__(self, char):
        self.char = char
        self.accidental_num = self._set_accidental()

    def is_major(self):
        return len(self.char) == 1 or self.char.endswith(("b", "#"))

    def is_minor(self):
        return self.char.endswith("m")

    def _set_accidental(self):
        if self.is_major():
            tonic = self.char
            scale_type = "Ionian"
        elif self.is_minor():
            tonic = self.char[:-1]
            scale_type = "Aeolian"
        else:
            tonic = self.char[:-3]
            if self.char.endswith("Mix"):
                scale_type = "Mixolydian"
            elif self.char.endswith("Dor"):
                scale_type = "Dorian"
            elif self.char.endswith("Phr"):
                scale_type = "Phrygian"
            elif self.char.endswith("Loc"):
                scale_type = "Locrian"
            else:
                print("error: invalid key string")
                exit()
        return get_accidental_num(tonic, scale_type)

    def get_default_accidental(self, pitch):
        if self.accidental_num < 0 and pitch in key_accidental_order[self.accidental_num:]:
            return Accidental.FLAT
        elif self.accidental_num > 0 and pitch in key_accidental_order[:self.accidental_num]:
            return Accidental.SHARP
        return Accidental.NATURAL
    
    def __str__(self):
        return self.char
