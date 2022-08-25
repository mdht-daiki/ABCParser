import re
from fractions import Fraction

note_ref = re.compile(r"""
    (?P<chord_start>\[)?
    (?P<tuplet>
        \(
            (?P<tuplet_denominator>\d)
            (
                :(?P<tuplet_numerator>\d)?
                :(?P<tuplet_count>\d)?
            )?

    )?
    (!(?P<finger>[1-5])!)?                    # fingering
    (?P<pitch>[\^=_]{0,2}[A-Ga-g][',]*)  # pitch
    (?P<length>\d+)?                         # length
    (?P<chord_end>\])?
    (?P<beam_end>\s*)
    """, re.VERBOSE)


def remove_head(item, head):
    if len(head) == 1:
        head = head + ":"
    return item.replace(head, "").strip()


class Length:
    def __init__(self, str):
        self.numerator, self.denominator = (int(n) for n in str.split("/"))

    def get(self):
        return Fraction(self.numerator, self.denominator)


class Meter(Length):
    def __init__(self, str):
        super().__init__(str)

    def is_compound(self):
        return self.numerator % 3 == 0 and self.denominator == 8

    def get_bar_length(self, base_length):
        return self.get() / base_length.get()


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


class Note:
    def __init__(self, note, voice):
        self.pitch = ""
        self.octave = 4
        self.accidental = 0
        self.pitch_str = ""
        self._init_pitch(note)
        self.finger = int(note.group("finger")) if note.group(
            "finger") else None
        self.length = int(note.group("length")) if note.group("length") else 1
        if voice.in_tuplet():
            self.tuplet = voice.in_tuplet()
            self.tuplet_count = voice.get_tuplet_count()
            self.length *= t.get_ratio()
        self.voice = voice
        self.offset = voice.get_offset()
        if note.group("chord_start"):
            self.voice.chord_start()
        if note.group("chord_end"):
            self.voice.chord_end()

    def get_length(self):
        return self.length

    def _init_pitch(self, note):
        pitch_str = note.group("pitch")
        self.pitch_str = pitch_str
        while pitch_str.startswith(("^", "_")):
            if pitch_str.startswith("^"):
                self.accidental = 1
                pitch_str = pitch_str[1:]
            elif pitch_str.startswith("_"):
                self.accidental = -1
                pitch_str = pitch_str[1:]

        if pitch_str[0].islower():
            self.octave += 1

        self.pitch = pitch_str[0].upper()
        pitch_str = pitch_str[1:]

        while len(pitch_str):
            if pitch_str[0] == "''":
                self.octave += 1
                pitch_str = pitch_str[1:]
            elif pitch_str[0] == ",":
                self.octave -= 1
                pitch_str = pitch_str[1:]
            else:
                print("error: invalid character")
                exit()

        accidental = self.accidental

        while accidental > 0:
            self.pitch += "#"
            accidental -= 1

        while accidental < 0:
            self.pitch += "b"
            accidental += 1

        self.pitch += str(self.octave)

    def set_finger(self, finger):
        self.finger = finger

    def __str__(self):
        rs = ""
        if self.finger:
            rs += f"!{self.finger}!"
        if self.accidental:
            accidental = "^" if self.accidental > 0 else "_"
            rs += accidental * abs(self.accidental)
        return rs


class Voice:
    def __init__(self, str, meter, base_length):
        items = remove_head(str, "V").split(" ")
        self.name = items[0]
        self.params = {}
        self.body = []
        self.notes = []
        self.base_length = base_length
        self.meter = meter
        self.offset = Fraction("0")
        self.chord = False
        self.tuplets = {}
        self.current_tuplet = None
        self.tuplet_count = 0
        if len(items) > 1:
            for item in items[1:]:
                param_name, param = item.split("=")
                self.params[param_name] = param

    def set_tuplet(self, note):
        t = Tuplet(note, self.meter.is_compound())
        self.tuplets[str(self.offset)] = t
        self.tuplet_count = t.get_count()
        self.current_tuplet = t

    def get_tuplet_count(self):
        return self.tuplet_count

    def in_tuplet(self):
        return self.current_tuplet

    def get_name(self):
        return self.name

    def chord_start(self):
        self.chord = True

    def chord_end(self):
        self.chord = False

    def append_body(self, body):
        self.body.append(body)
        res = note_ref.finditer(body)
        for note in res:
            if note.group("tuplet"):
                self.set_tuplet(note)
            n = Note(note, self)
            self.notes.append(n)
            if not self.chord:
                self.update_offset(n)
            if self.tuplet_count > 1:
                self.tuplet_count -= 1
            elif self.tuplet_count == 1:
                self.tuplet_count = 0
                self.current_tuplet = None

    def get_offset(self):
        return self.offset

    def update_offset(self, note):
        self.offset += note.get_length()

    def print_notes(self):
        for note in self.notes:
            print(note)

    def set_finger(self, finger):
        if len(finger) != len(self.notes):
            print("error: length of fingernums are different from notes")
            return
        if not finger.isdecimal():
            print("error: fingernums has something not number")
            return
        for i, note in enumerate(self.notes):
            note.set_finger(int(finger[i]))


class Tune:
    def __init__(self, abc):
        self.abc = abc
        self.params = self._init_params()

    def _init_params(self):
        params = {}
        voices = {}
        abc_list = self.abc.split("\n")

        for item in abc_list:
            if item.startswith("X:"):
                params["id"] = int(remove_head(item, "X"))
            elif item.startswith("T:"):
                params["title"] = remove_head(item, "T")
            elif item.startswith("M:"):
                params["meter"] = Meter(remove_head(item, "M"))
            elif item.startswith("L:"):
                params["base_length"] = Length(remove_head(item, "L"))
            elif item.startswith("K:"):
                params["key"] = remove_head(item, "K")
            elif item.startswith("V:"):
                v = Voice(item, params["meter"], params["base_length"])
                name = v.get_name()
                voices[name] = v

            if item.startswith("[V:"):
                name = item.replace("[V:", "").split("]")[0]
                head = f"[V:{name}]"
                body = remove_head(item, head)
                voices[name].append_body(body)

            if item.startswith("%%score"):
                params["score_directive"] = remove_head(item, "%%score")

        params["voices"] = voices
        return params

    def get_params(self):
        return self.params

    def print_out(self):
        for name, voice in self.params["voices"].items():
            print(name)
            voice.print_notes()

    def create_string(self):
        rsl = []
        x = str(self.params["id"])
        rsl.append(f"X: {x}")
        t = self.params["title"]
        rsl.append(f"T: {t}")

        return "\n".join(rsl)


if __name__ == "__main__":
    abc_string = """X: 1
    T: Cooley's
    M: 4/4
    L: 1/8
    K: C
    %%score {Right | Left}
    V:Right
    V:Left clef=bass
    [V:Right]D^CDE FGAc | (3efe dc ^cB_B_A || !1!G2 
    [V:Left]D,2 F,2 A,2 C2 | B,2 A,2 G,2 F,2 || [!5!C,!4!E,!1!C]"""

    t = Tune(abc_string)
    t.print_out()
    t.get_params()

    finger = "121231234543231321"

    t.params["voices"]["Right"].set_finger(finger)
    t.print_out()
    print(t.create_string())
