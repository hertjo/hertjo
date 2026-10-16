"""Drop the title line from a metrics SVG and shrink it by that height."""
import re
import sys

src, out, title_h = sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 30
s = open(src).read()
s = re.sub(r'<h2 class="field">.*?</h2>', "", s, count=1, flags=re.S)
s = re.sub(r'(<svg[^>]*?height=")(\d+)(")', lambda m: f"{m.group(1)}{int(m.group(2)) - title_h}{m.group(3)}", s, count=1)
open(out, "w").write(s)
