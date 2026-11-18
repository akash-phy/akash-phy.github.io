#!/usr/bin/env python3
"""Build the site-wide Open Graph / social preview image (1200x630).

Run:  python3 scripts/make-og-image.py
Output: assets/img/og-preview.png
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img" / "og-preview.png"
PORTRAIT = ROOT / "assets" / "img" / "akash.png"

W, H = 1200, 630
BG = (15, 23, 42)         # slate-900
FG = (248, 250, 252)      # slate-50
MUTED = (148, 163, 184)   # slate-400
ACCENT = (56, 189, 248)   # sky-400

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, size, max_width):
    """Shrink font size until `text` fits inside max_width."""
    while size > 12:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 1
    return font(path, size)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # subtle vertical gradient
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(BG[i] + 8 * t) for i in range(3)))

    # accent bar on the left
    d.rectangle([0, 0, 10, H], fill=ACCENT)

    # portrait on the right, circular, with ring
    right_col = W - 90
    if PORTRAIT.exists():
        size = 300
        p = Image.open(PORTRAIT).convert("RGBA").resize(
            (size, size), Image.Resampling.LANCZOS
        )
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
        cx, cy = right_col - size, (H - size) // 2
        ring = Image.new("RGBA", (size + 12, size + 12), (0, 0, 0, 0))
        ImageDraw.Draw(ring).ellipse(
            (0, 0, size + 11, size + 11), outline=ACCENT + (140,), width=3
        )
        img.paste(ring, (cx - 6, cy - 6), ring)
        img.paste(p, (cx, cy), mask)
        max_w = cx - 80 - 50
    else:
        max_w = W - 160

    x = 80
    d.text((x, 120), "Akash Yadav", font=font(SERIF, 72), fill=FG)

    role1 = "PhD Research Scholar"
    role2 = "IISER Thiruvananthapuram"
    f_role = font(SANS, 30)
    d.text((x, 235), role1, font=f_role, fill=MUTED)
    d.text((x, 277), role2, font=f_role, fill=MUTED)

    # divider
    d.rectangle([x, 345, x + 120, 349], fill=ACCENT)

    y = 385
    for line in ("Complex Systems", "Network Science", "Nonlinear Dynamics"):
        f = fit(d, line, SANS_B, 38, max_w)
        d.text((x, y), line, font=f, fill=FG)
        y += 58

    d.text((x, H - 62), "akash-phy.github.io", font=font(SANS, 26), fill=MUTED)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")
    print(f"text column width limit: {max_w}px")


if __name__ == "__main__":
    main()
