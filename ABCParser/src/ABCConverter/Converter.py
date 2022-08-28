from pitch.Accidental import Accidental
from copy import deepcopy

class Converter:
  def __init__(self, tune):
    self.tuneobj = tune
  
  def abc(self):
    return self.visit(self.tuneobj)
  
  def visit(self, obj):
    return getattr(self, obj.__class__.__name__.lower())(obj)
  
  def tune(self, tune):
    abc_text = ""
    for param in ["id", "title", "meter", "base_length", "key", "score"]:
      abc_text += getattr(self, param)(tune.get(param))
    voices = tune.get_voices().values()
    for voice in voices:
      abc_text += self.voice_head(voice)
    
    def body_generator(voices):
      bodies = []
      for voice in voices:
        bodies.append(deepcopy(voice.get_body()))
      for lines in zip(*bodies):
        for line, voice in zip(lines, voices):
          yield line, voice.get_name()

    bg = body_generator(voices)

    for line, name in bg:
      abc_text += self.line(line, name)
    return abc_text
  
  def id(self, id):
    return f"X: {id}\n"
  
  def title(self, title):
    return f"T: {title}\n"
  
  def meter(self, meter):
    return f"M: {meter}\n"
  
  def base_length(self, base_length):
    return f"L: {base_length}\n"
  
  def key(self, key):
    return f"K: {key}\n"

  def score(self, score):
    return f"%%score {score}\n"
  
  def voice_head(self, voice):
    rs = f"V:{voice.get_name()}"
    if voice.get_params():
      for key, value in voice.get_params().items():
        rs += f" {key}={value}"
    return rs + "\n"
  
  def line(self, line, name):
    rs = f"[V:{name}]"
    for note in line:
      if isinstance(note, list):
        rs += self.chord(note)
      else:
        rs += self.visit(note)
    rs += "\n"
    return rs
  
  def note(self, note):
    rs = ""
    for param in ["tuplet", "finger", "accidental", "pitch", "duration", "space", "barline"]:
      rs += getattr(self, param)(note)
    return rs

  def tuplet(self, note):
    rs = ""
    tuplet = note.get_tuplet()
    if tuplet[0] != 0:
      rs += f"({tuplet[0]}"
      if tuplet[1] or tuplet[2]:
        rs += f":{tuplet[1] or ''}:{tuplet[2] or ''}"
    return rs
  
  def finger(self, note):
    rs = ""
    if note.get_fingering():
      rs += f"!{note.get_fingering()}!"
    return rs
  
  def accidental(self, note):
    rs = ""
    if not note.is_default_accidental():
      d = {
            Accidental.DOUBLE_SHARP: "^^",
            Accidental.SHARP: "^",
            Accidental.NATURAL: "=",
            Accidental.FLAT: "_",
            Accidental.DOUBLE_FLAT: "__"
      }
      rs += d[note.get_accidental()]
    return rs
  
  def pitch(self, note):
    rs = ""
    pitch = note.get_pitch()
    octave = note.get_octave()
    if octave >= 5:
      pitch = pitch.lower()
    rs += pitch
    while octave <= 3:
      rs += ","
      octave += 1
    while octave >= 6:
      rs += "'"
      octave -= 1
    return rs
  
  def duration(self, note):
    rs = ""
    if note.get_duration() != 1:
      rs += f"{note.get_duration()}"
    return rs
  
  def space(self, note):
    rs = ""
    if note.is_beam_end():
      rs = " "
    return rs

  def barline(self, note):
    rs = ""
    if note.get_barline():
      rs += note.get_barline()
    return rs
  
  def chord(self, chord):
    rs = "["
    for note in chord:
      rs += self.visit(note)
    rs += "]"
    return rs
