import re
from fractions import Fraction

inline_field_ref = re.compile(r"""
\[
  (?P<field>[A-Z]):(?P<param>.*)
\]
""", re.VERBOSE)
chord_ref = re.compile(r"""
\[
    (
      (!(?P<finger>[1-5])!)?                   # fingering
      (?P<pitch>[\^=_]{0,2}[A-Ga-g][',]*)      # pitch
    )*
\]
(?P<length>\d+)?                               # length
""", re.VERBOSE)
note_ref = re.compile(r"""
(?P<tuplet>
    \(
        (?P<tuplet_denominator>\d)
        (
            :(?P<tuplet_numerator>\d)?
            :(?P<tuplet_count>\d)?
        )?
)?
(!(?P<finger>[1-5])!)?                   # fingering
(?P<pitch>[\^=_]{0,2}[A-Ga-g][',]*)      # pitch
(?P<length>\d+)?                         # length
""", re.VERBOSE)

body = "D,2 F,2 A,2 C2 | B,2 A,2 G,2 F,2 || [!5!C,!4!E,!1!C]"
inline_field_ref