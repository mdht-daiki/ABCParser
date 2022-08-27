from lark import Token
from encoder.encoder import json_dump
from visitor.NoteVisitor import NoteVisitor


class BodyVisitor:
    def __default__(self, tree, tune):
        for child in tree.children:
            self.visit(child, tune)

    def visit(self, tree, tune):
        if isinstance(tree, Token):
            return tree.value
        print(f"now I'm visiting {tree.data}")
        f = getattr(self, tree.data, self.__default__)
        return f(tree, tune)

    def voice_statement(self, tree, tune):
        voice = self.visit(tree.children[0], tune)
        n = NoteVisitor(tune)
        for child in tree.children[1:]:
            if child.data in ["note", "chord"]:
                note = n.visit(child, tune)
                tune.push_note(voice, note)
                print(json_dump(tune))
            elif child.data == "barline":
                barline = self.visit(child, tune)
                tune.get_voice(voice).get_last_note().set_barline(barline)

    def voice_stat_name(self, tree, tune):
        return tree.children[0].value

    def barline(self, tree, note):
        return tree.children[0].value
