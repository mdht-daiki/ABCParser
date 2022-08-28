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
        line = []
        for child in tree.children[1:]:
            if child.data in ["note", "chord"]:
                line.append(n.visit(child, tune))
            elif child.data == "barline":
                barline = self.barline(child)
                line[-1].set_barline(barline)
            elif child.data == "space":
                line[-1].set_beam_end()
        tune.push_line(voice, line)

    def voice_stat_name(self, tree):
        return tree.children[0].value

    def barline(self, tree):
        return tree.children[0].value
