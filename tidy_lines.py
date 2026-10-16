"""Lines-of-code panel: drop the repositories summary above the table and hide private repository names."""
import re
import sys

src, out, private_list = sys.argv[1], sys.argv[2], sys.argv[3]
private = {l.strip() for l in open(private_list) if l.strip()}
s = open(src).read()
# the first top-level section is the repositories summary; the lines table is the next one
start = s.index('<section class="largeable')
depth, end = 0, None
for m in re.finditer(r"<section\b[^>]*>|</section>", s[start:]):
    depth += 1 if m.group(0).startswith("<section") else -1
    if depth == 0:
        end = start + m.end()
        break
summary_h = 118
s = s[:start] + s[end:]
s = re.sub(r'(<svg[^>]*?height=")(\d+)(")', lambda m: f"{m.group(1)}{int(m.group(2)) - summary_h}{m.group(3)}", s, count=1)
s = re.sub(r"hertjo/([\w.-]+)", lambda m: "private-repo" if m.group(1) in private else m.group(0), s)
open(out, "w").write(s)
