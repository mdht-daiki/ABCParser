import os
from lark import Lark
from visitor.Visitor import Visitor
from encoder.encoder import json_dump

file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "grammar", "abc_grammar.lark")

with open(file_path, "r", encoding="utf-8") as grammar:
  abc_parser = Lark(grammar.read(), start="sentence")

class Parser:
  def __init__(self, input_str):
    self.input = input_str
    self.tree = abc_parser.parse(self.input)
    self.tune = Visitor(self.tree).env
  
  def print(self):
    print(json_dump(self.tune))