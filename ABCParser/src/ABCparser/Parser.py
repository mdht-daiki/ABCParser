import os
from lark import Lark
from visitor.Visitor import Visitor
from encoder.encoder import json_dump
from ABCConverter.Converter import Converter

file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "grammar", "abc_grammar.lark")

with open(file_path, "r", encoding="utf-8") as grammar:
  abc_parser = Lark(grammar.read(), start="sentence")

class Parser:
  def __init__(self, abc):
    self.abc = abc
    self.tree = abc_parser.parse(self.abc)
    self.tune = Visitor(self.tree).env
  
  def json(self):
    print(self.tree.pretty())
    print(json_dump(self.tune))
  
  def convert_to_abc(self):
    print(Converter(self.tune).abc())
  
  def get_finger_list(self):
    return self.tune.get_finger_list()
  
  def set_fingers(self, finger_list):
    self.tune.set_fingers(finger_list)