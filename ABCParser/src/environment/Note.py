from pitch.Accidental import Accidental
from notelength.Length import Length


class Note:
    def __init__(self, tune, offset):
        self.key = tune.get("key")
        self.base_length = tune.get("base_length")
        self.offset = offset
        self.pitch = ""
        self.octave = 4
        self.accidental = None
        self.default_accidental = False
        self.finger = None
        self.length = self.base_length
        self.duration = 1
        self.beam_end = False
        self.barline = None
        self.tuplet = [0, 0, 0]
    
    def set_fingerings(self, finger):
        self.finger = finger
    
    def get_fingering(self):
        return self.finger

    def double_sharp(self):
        self.accidental = Accidental.DOUBLE_SHARP

    def sharp(self):
        self.accidental = Accidental.SHARP

    def natural(self):
        self.accidental = Accidental.NATURAL

    def flat(self):
        self.accidental = Accidental.FLAT

    def double_flat(self):
        self.accidental = Accidental.DOUBLE_FLAT

    def set_pitch(self, pitch):
        self.pitch = pitch.upper()
        if pitch.islower():
            self.octave += 1
        if self.accidental is None:
            self.default_accidental = True
            self.accidental = self.key.get_default_accidental(self.pitch)
    
    def is_default_accidental(self):
        return self.default_accidental
    
    def get_accidental(self):
        return self.accidental

    def octave_up(self):
        self.octave += 1

    def octave_down(self):
        self.octave -= 1
    
    def get_octave(self):
        return self.octave
    
    def get_pitch(self):
        return self.pitch

    def set_beam_end(self):
        self.beam_end = True
    
    def is_beam_end(self):
        return self.beam_end

    def set_barline(self, barline):
        self.barline = barline
    
    def get_barline(self):
        return self.barline

    def set_duration(self, duration):
        self.duration = duration
        self.length = Length(self.base_length, duration)
    
    def get_duration(self):
        return self.duration

    def get_next_offset(self):
        return self.offset.get_next_offset(self.length)

    def set_tuplet(self, tuplet):
        self.length = tuplet.mul(self.length)
    
    def is_start_tuplet(self, tuplet):
        self.tuplet = tuplet
    
    def get_tuplet(self):
        return self.tuplet

    