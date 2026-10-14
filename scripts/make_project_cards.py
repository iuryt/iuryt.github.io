# Link-preview images (1200x630 JPG) for research project pages, from the first gallery image;
# also points each page's `image:` at its card. Usage: python scripts/make_project_cards.py <project_root>
import pathlib, re, sys
from PIL import Image, ImageDraw
root = pathlib.Path(sys.argv[1])
W, H, K = 1200, 630, 3
COLORS = ("#0b5f86", "#2a9d8f", "#e76f51")
for q in sorted((root / "research").glob("*.qmd")):
    s = q.read_text()
    srcs = re.findall(r"- src: \.\./(\S+)", s)
    src = next(x for x in srcs if not x.endswith(".mp4"))
    fig = Image.open(root / src).convert("RGBA")
    card = Image.new("RGB", (W * K, H * K), "white")
    d = ImageDraw.Draw(card)
    for i, c in enumerate(COLORS):
        d.rectangle([i * W * K // 3, 0, (i + 1) * W * K // 3, 12 * K], fill=c)
    bw, bh = (W - 80) * K, (H - 12 - 60) * K
    scale = min(bw / fig.width, bh / fig.height)
    fig = fig.resize((int(fig.width * scale), int(fig.height * scale)), Image.LANCZOS)
    bg = Image.new("RGBA", fig.size, "white"); bg.alpha_composite(fig)
    card.paste(bg.convert("RGB"), ((W * K - fig.width) // 2, 12 * K + (H * K - 12 * K - fig.height) // 2))
    out = root / "img/social" / f"{q.stem}.jpg"
    card.resize((W, H), Image.LANCZOS).save(out, quality=92, subsampling=0)
    s = re.sub(r"^image: .*$", f"image: ../img/social/{q.stem}.jpg", s, count=1, flags=re.M)
    q.write_text(s)
    print(q.stem, src, out.stat().st_size // 1024, "KB")
