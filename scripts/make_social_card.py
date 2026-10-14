# Link-preview card (1200x630) for the site: photo, name, role, research lines.
# Usage: python scripts/make_social_card.py <photo> <icon.png> <fonts_dir> <out.jpg>
import sys
from PIL import Image, ImageDraw, ImageFont
photo, icon, fonts, out = sys.argv[1:5]
K = 3  # supersampling factor
W, H = 1200 * K, 630 * K
INK, MUTED, LINE = "#1d2733", "#5f6b78", "#e6e9ed"
BLUE, GREEN, CORAL = "#0b5f86", "#2a9d8f", "#e76f51"

def font(name, size, weight):
    f = ImageFont.truetype(f"{fonts}/{name}.ttf", size)
    try: f.set_variation_by_name(weight)
    except Exception: pass
    return f

card = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(card)

# three-color band on top (one per research line)
for i, c in enumerate((BLUE, GREEN, CORAL)):
    d.rectangle([i * W // 3, 0, (i + 1) * W // 3, 12 * K], fill=c)

# round photo
P = 320 * K
ph = Image.open(photo).convert("RGB").resize((P, P), Image.LANCZOS)
mask = Image.new("L", (P * 4, P * 4), 0)
ImageDraw.Draw(mask).ellipse([0, 0, P * 4 - 1, P * 4 - 1], fill=255)
mask = mask.resize((P, P), Image.LANCZOS)
px, py = 90 * K, (H - P) // 2 + 6 * K
card.paste(ph, (px, py), mask)

x = px + P + 70 * K
name = font("SourceSerif4", 70 * K, "SemiBold")
role = font("Inter", 32 * K, "Regular")
pill = font("Inter", 24 * K, "SemiBold")
url = font("Inter", 26 * K, "Medium")

y = 150 * K
d.text((x, y), "Iury Simoes-Sousa", font=name, fill=INK)
y += 100 * K
d.text((x, y), "Computational Oceanographer", font=role, fill=MUTED)
y += 46 * K
d.text((x, y), "Assistant Professor · University of Delaware", font=role, fill=MUTED)

# research-line pills
y += 78 * K
cx = x
for label, c in (("Data-driven", BLUE), ("Dynamics", GREEN), ("Impacts", CORAL)):
    tw = d.textlength(label, font=pill)
    d.rounded_rectangle([cx, y, cx + tw + 36 * K, y + 46 * K], radius=23 * K, outline=c, width=3 * K)
    d.text((cx + 18 * K, y + 9 * K), label, font=pill, fill=c)
    cx += tw + 50 * K

# footer: icon + url
ic = Image.open(icon).convert("RGBA").resize((40 * K, 40 * K), Image.LANCZOS)
card.paste(ic, (x, H - 88 * K), ic)
d.text((x + 54 * K, H - 82 * K), "iuryt.github.io", font=url, fill=BLUE)
card = card.resize((W // K, H // K), Image.LANCZOS)
card.save(out, quality=95, subsampling=0)  # 4:4:4 keeps colored text crisp
