# Site icons: favicon.svg / favicon.png / apple-touch-icon.png (an eddy, white on ocean blue, coral core).
# Usage: python scripts/make_icons.py svg favicon.svg | python scripts/make_icons.py png <out.png> <size>
import math, sys
from PIL import Image, ImageDraw
# Shared geometry (32x32 units) — keep in sync with favicon.svg
TURNS, R0, R1, STROKE, CORE = 1.55, 3.6, 11.4, 3.4, 2.5
def spiral(n=4000):
    for i in range(n + 1):
        t = i / n; th = -math.pi / 2 + 2 * math.pi * TURNS * t; r = R0 + (R1 - R0) * t
        yield 16 + r * math.cos(th), 16 + r * math.sin(th)
def png(out, size):
    ss = 1024; k = ss / 32
    img = Image.new("RGBA", (ss, ss), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, ss - 1, ss - 1], radius=7 * k, fill="#0b5f86")
    w = STROKE * k / 2
    for x, y in spiral():
        d.ellipse([x * k - w, y * k - w, x * k + w, y * k + w], fill="white")
    c = CORE * k
    d.ellipse([16 * k - c, 16 * k - c, 16 * k + c, 16 * k + c], fill="#e76f51")
    img.resize((size, size), Image.LANCZOS).save(out)
def svg(out):
    pts = list(spiral(300))
    path = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    open(out, "w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="7" fill="#0b5f86"/>
  <path d="{path}" fill="none" stroke="#ffffff" stroke-width="{STROKE}" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="16" cy="16" r="{CORE}" fill="#e76f51"/>
</svg>
''')
if sys.argv[1] == "svg": svg(sys.argv[2])
else: png(sys.argv[2], int(sys.argv[3]))
