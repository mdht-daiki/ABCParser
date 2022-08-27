from pitch.Accidental import Accidental
from notelength.Length import Length
from fractions import Fraction

class Note:
  def __init__(self, tune, offset):
    self.key = tune.get("key")
    self.base_length = tune.get("base_length")
    self.offset = offset
    self.pitch = ""
    self.octave = 4
    self.accidental = None
    self.finger = None
    self.length = self.base_length
    self.beam_end = False
    self.barline = None
  
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
      self.octave -= 1
    if self.accidental is None:
      self.accidental = self.key.get_default_accidental(self.pitch)
  
  def octave_up(self):
    self.octave += 1
  
  def octave_down(self):
    self.octave -= 1
  
  def set_beam_end(self):
    self.beam_end = True
  
  def set_barline(self, barline):
    self.barline = barline
  
  def set_duration(self, duration):
    self.length = Length(self.base_length, duration)
  
  def get_next_offset(self):
    return self.offset.get_next_offset(self.length)
  
  def set_tuplet(self, tuplet):
    self.length = tuplet.mul(self.length)