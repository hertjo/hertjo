"""Keep only the isometric calendar from the metrics SVG (no title, no stats)."""
import re
import sys

src, out = sys.argv[1], sys.argv[2]
s = open(src).read()
start = s.index('<svg version="1.1"')
depth, pos = 0, start
for m in re.finditer(r"<svg\b|</svg>", s[start:]):
    depth += 1 if m.group(0) == "<svg" else -1
    if depth == 0:
        end = start + m.end()
        break
inner = s[start:end]
inner = re.sub(r'\sstyle="margin-top:\s*-?\d+px;?"', "", inner, count=1)
inner = inner.replace('<svg version="1.1"', '<svg version="1.1" width="480" height="270"', 1)
open(out, "w").write(inner)
