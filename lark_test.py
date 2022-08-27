import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from ABCparser.Parser import Parser

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
p = Parser(input)
p.print()