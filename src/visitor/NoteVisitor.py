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

    def _update(self, note):
        if self.current_tuplet and self.tuplet_count > 0:
            note.set_tuplet(self.current_tuplet)
            self.tuplet_count -= 1
        self.offset = note.get_next_offset()

    def __default__(self, tree, tune):
        for child in tree.children:
            self.visit(child, tune)

    def visit(self, tree, tune):
        if isinstance(tree, Token):
            return tree.value
        print(f"now I'm visiting {tree.data}")
        f = getattr(self, tree.data, self.__default__)
        return f(tree, tune)

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
