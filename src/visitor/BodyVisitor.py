from lark import Token

class BodyVisitor:
  def __default__(self, tree, env):
    for child in tree.children:
      self.visit(child, env)
  
  def visit(self, tree, env):
    if isinstance(tree, Token):
      return tree.value
    print(f"now I'm visiting {tree.data}")
    f = getattr(self, tree.data, self.__default__)
    return f(tree, env)
  
  def voice_statement(self, tree, env):
    voice = self.visit(tree.children[0], env)
    for child in tree.children[1:]:
      note = self.visit(child, env)
      env.push_note(voice, note)
  
  def voice_stat_name(self, tree, env):
    return tree.children[0].value
  
  def note(self, tree, env):
    pass