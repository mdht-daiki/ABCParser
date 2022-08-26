from lark import Token


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
        for child in tree.children[1:]:
            note = self.visit(child, tune)
            tune.push_note(voice, note)

    def voice_stat_name(self, tree, tune):
        return tree.children[0].value

    def note(self, tree, tune):
        pass
