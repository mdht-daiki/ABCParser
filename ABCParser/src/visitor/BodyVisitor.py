from lark import Token
from visitor.NoteVisitor import NoteVisitor


class BodyVisitor:
    def __default__(self, tree, tune):
        for child in tree.children:
            self.visit(child, tune)

    def visit(self, tree, tune):
        if isinstance(tree, Token):
            return tree.value
        f = getattr(self, tree.data, self.__default__)
        return f(tree, tune)

    def voice_statement(self, tree, tune):
        if tree.children[0].data == "voice_stat_name":
            voice = self.voice_stat_name(tree.children[0])
        n = NoteVisitor(tune)
        for child in tree.children[1:]:
            if child.data in ["note", "chord"]:
                note = n.visit(child, tune)
                tune.push_note(voice, note)
            elif child.data == "barline":
                barline = self.barline(child)
                tune.get_voice(voice).get_last_note().set_barline(barline)
            elif child.data == "space":
                tune.get_voice(voice).get_last_note().set_beam_end()

    def voice_stat_name(self, tree):
        return tree.children[0].value

    def barline(self, tree):
        return tree.children[0].value
