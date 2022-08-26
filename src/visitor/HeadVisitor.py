from encoder.encoder import json_dump
from environment.Voice import Voice
from notelength.Length import Length
from notelength.Meter import Meter
from lark import Token

class HeadVisitor: 
  def __default__(self, tree, env):
    for child in tree.children:
      self.visit(child, env)
  
  def visit(self, tree, env):
    if isinstance(tree, Token):
      return tree.value
    print(f"now I'm visiting {tree.data}")
    f = getattr(self, tree.data, self.__default__)
    return f(tree, env)
  
  def field(self, tree, env):
    self.visit(tree.children[0], env)
    print(json_dump(env))
  
  def id(self, tree, env):
    env.set("id", tree.children[0].value)
  
  def title(self, tree, env):
    env.set("title", tree.children[0].value)

  def meter(self, tree, env):
    env.set("meter", Meter(tree.children[0].value))
  
  def base_length(self, tree, env):
    env.set("base_length", Length(tree.children[0].value))
  
  def key(self, tree, env):
    env.set("key", tree.children[0].value)

  def directive(self, tree, env):
    rl = []
    for child in tree.children:
      r = self.visit(child, env)
      if r:
        rl.append(r)
    env.set(rl[0], rl[1])
    print(json_dump(env))
  
  def directive_name(self, tree, env):
    return tree.children[0].value
  
  def directive_content(self, tree, env):
    return tree.children[0].value
  
  def voice(self, tree, env):
    v = Voice()
    for child in tree.children:
      self.visit(child, v)
    env.set_voice(v)
    print(json_dump(env))
  
  def voice_name(self, tree, v):
    v.set_name(tree.children[0].value)
    # print(v.getall())
  
  def voice_param(self, tree, v):
    key = tree.children[0].value
    value = tree.children[1].value
    v.set_param(key, value)
    # print(v.getall())