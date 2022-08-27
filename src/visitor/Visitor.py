from .HeadVisitor import HeadVisitor
from .BodyVisitor import BodyVisitor
from environment.Tune import Tune
from lark import Token

class Visitor:
  def __init__(self, tree):
    self.h = HeadVisitor()
    self.b = BodyVisitor()
    self.tree = tree
    self.env = Tune(None)
    self.visit(self.tree, self.env)

  def __default__(self, tree, env):
    for child in tree.children:
      self.visit(child, env)

  def visit(self, tree, env):
    if isinstance(tree, Token):
      return tree.value
    print(f"now I'm visiting {tree.data}")
    f = getattr(self, tree.data, self.__default__)
    return f(tree, env)
  
  def head(self, tree, env):
    getattr(self.h, tree.data, self.h.__default__)(tree, env)
  
  def body(self, tree, env):
    getattr(self.b, tree.data, self.b.__default__)(tree, env)
    