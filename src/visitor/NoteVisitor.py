from lark import Token
from environment.Note import Note
from notelength.Offset import Offset
from notelength.Tuplet import create_tuplet

accidentals = ["double_sharp", "sharp", "natural", "flat", "double_flat"]


class NoteVisitor:
    def __init__(self, tune):
        self.offset = Offset(tune.get("base_length"))
        self.current_tuplet = None
        self.tuplet_count = None
        self.in_chord = False
    
    # update
    
    def is_in_chord(self, note):
        return isinstance(note, Note) and self.in_chord
    
    def is_not_in_chord(self, note):
        return isinstance(note, Note) and not self.in_chord

    def is_in_tuplet(self):
        return self.current_tuplet is not None and self.tuplet_count > 0

    def _update_tuplet_length(self, note):
        if self.is_in_tuplet():
            note.set_tuplet(self.current_tuplet)
    
    def _update_tuplet_count(self, note):
        if self.is_in_tuplet() and self.is_not_in_chord(note):
            self.tuplet_count -= 1

    def _update_offset(self, note):
        if self.is_not_in_chord(note):
            self.offset = note.get_next_offset()

    def _update(self, note):
        self._update_tuplet_length(note)
        self._update_tuplet_count(note)
        self._update_offset(note)
    
    def _update_chord(self, note):
        self._update_tuplet_count(note)
        self._update_offset(note)
    
    # visit

    def __default__(self, tree, tune):
        for child in tree.children:
            self.visit(child, tune)

    def visit(self, tree, tune):
        if isinstance(tree, Token):
            return tree.value
        f = getattr(self, tree.data, self.__default__)
        return f(tree, tune)

    def chord(self, tree, tune):
        chord = []
        self.in_chord = True
        for child in tree.children:
            chord.append(self.visit(child, tune))
        self.in_chord = False
        self._update_chord(chord[0])
        return chord

    def note(self, tree, tune):
        n = Note(tune, self.offset)
        for child in tree.children:
            if child.data in accidentals:
                getattr(n, child.data)()
            elif child.data == "tuplet":
                self.tuplet(child, tune)
            elif child.data == "space":
                n.set_beam_end()
            else:
                self.visit(child, n)
        self._update(n)
        return n

    def pitch(self, tree, note):
        note.set_pitch(tree.children[0].value)
        if len(tree.children) > 1:
            for child in tree.children[1:]:
                getattr(note, child.data)()

    def duration(self, tree, note):
        note.set_duration(int(tree.children[0].value))

    def tuplet(self, tree, tune):
        d = {
            "tuplet_denominator": None,
            "tuplet_numerator": None,
            "tuplet_count": None
        }
        for child in tree.children:
            if child.data in d.keys():
                d[child.data] = int(child.children[0].value)
        self.current_tuplet, self.tuplet_count = create_tuplet(tune, d)
