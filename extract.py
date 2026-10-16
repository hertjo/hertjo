"""Calendar panel: drop the title line, small stats text with room beside the 3D plot, and the busiest day drawn as
the Empire State Building."""
import re
import sys

src, out, title_h = sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 30
s = open(src).read()
s = re.sub(r'<h2 class="field">.*?</h2>', "", s, count=1, flags=re.S)
# the 3D plot is pulled up under the title (a negative margin); without the title, pull it up that much less
s = re.sub(r'style="margin-top:\s*(-?\d+)px;?"', lambda m: f'style="margin-top: {int(m.group(1)) + title_h}px;"', s, count=1)
s = re.sub(r'(<svg[^>]*?height=")(\d+)(")', lambda m: f"{m.group(1)}{int(m.group(2)) - title_h - 55}{m.group(3)}", s, count=1)  # also the empty space below the plot
# the stats: same size as the other panels' tables (this panel is shown twice as wide), and pushed right
s = s.replace("</style>", ".row h3.field,.row .field{font-size:7.5px!important;margin-bottom:1px}"
              ".row .field svg{width:8px;height:8px;margin:0 4px}"
              ".row>section:last-child{padding-left:96px}</style>", 1)

# ---- the Empire State Building on the busiest day
GROUP = re.compile(r'<g transform="translate\(([-\d.]+), ([-\d.]+)\)">\s*(<path fill="(#[0-9a-f]{6})" d="M1\.7,2 0,1 1\.7,0 3\.4,1 z"/>\s*'
                   r'<path[^>]*?d="M0,1 1\.7,2 1\.7,([-\d.]+) 0,[-\d.]+ z"/>\s*<path[^>]*?/>)\s*</g>')
best = max(GROUP.finditer(s), key=lambda m: float(m.group(5)), default=None)
if best:
    h = float(best.group(5)) - 2           # the bar's height
    H = h * 2.4                            # taller than the bar: it is the Empire State Building
    col = best.group(4)
    cx, cy = 1.7, 1.0

    def box(f, e0, e1, fill=col):
        """An isometric box of footprint scale f, from elevation e0 to e1 (0 = ground, h = the bar's top)."""
        t, b = h - e1, h - e0
        P = lambda x, y, dy: f"{cx + f * (x - cx):.3f},{cy + f * (y - cy) + dy:.3f}"
        top = f'<path fill="{fill}" d="M{P(1.7, 2, t)} {P(0, 1, t)} {P(1.7, 0, t)} {P(3.4, 1, t)} z"/>'
        left = f'<path fill="{fill}" filter="url(#brightness1)" d="M{P(0, 1, t)} {P(1.7, 2, t)} {P(1.7, 2, b)} {P(0, 1, b)} z"/>'
        right = f'<path fill="{fill}" filter="url(#brightness2)" d="M{P(1.7, 2, t)} {P(3.4, 1, t)} {P(3.4, 1, b)} {P(1.7, 2, b)} z"/>'
        return left + right + top

    def floors(f, e0, e1, n):
        """Thin light floor lines across the two visible faces."""
        out = []
        for k in range(1, n):
            e = e0 + (e1 - e0) * k / n
            y = h - e
            a = f"{cx + f * (0 - cx):.3f},{cy + f * (1 - cy) + y:.3f}"
            m = f"{cx:.3f},{cy + f * (2 - cy) + y:.3f}"
            z = f"{cx + f * (3.4 - cx):.3f},{cy + f * (1 - cy) + y:.3f}"
            out.append(f'<path d="M{a} L{m} L{z}" fill="none" stroke="#9be9a8" stroke-width="0.05" stroke-opacity="0.55"/>')
        return "".join(out)

    parts = [box(1.0, 0, H * 0.10), box(0.82, H * 0.10, H * 0.16), box(0.66, H * 0.16, H * 0.74), floors(0.66, H * 0.16, H * 0.74, 22),
             box(0.52, H * 0.74, H * 0.80), box(0.40, H * 0.80, H * 0.85), box(0.28, H * 0.85, H * 0.89),
             box(0.16, H * 0.89, H * 0.95, "#30a14e"),
             f'<path d="M{cx:.3f},{cy + h - H * 0.95:.3f} L{cx:.3f},{cy + h - H:.3f}" stroke="#216e39" stroke-width="0.12" stroke-linecap="round"/>']
    s = s[:best.start(3)] + "".join(parts) + s[best.end(3):]
open(out, "w").write(s)
