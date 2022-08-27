from visitor.Visitor import Visitor
import os
import sys
from lark import Lark

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

with open("abc_grammar.lark", "r", encoding="utf-8") as grammar:
    parser = Lark(grammar.read(), start="sentence")

input = """X: 1
T: Cooley's
M: 4/4
L: 1/8
K: C
%%score {Right | Left}
V:Right
V:Left clef=bass
[V:Right]D^CDE FGAc | (3efe dc ^cB_B_A || !1!G2
[V:Left]D,2 F,2 A,2 C2 | B,2 A,2 G,2 F,2 || [!5!C,!4!E,!1!C]"""
tree = parser.parse(input)
print(tree.pretty())
Visitor(tree)
