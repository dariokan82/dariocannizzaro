#!/usr/bin/env python3
"""Generate the placeholder images for every image slot on the site.

Run once (`python3 tools/placeholders.py`) and the slots fill with dithered
grey stand-ins that name themselves and their size. Dario overwrites each
file with his own picture, same filename, and nothing else changes.

Exception: the strips under src/assets/img/strip/ are the real thing — see strips().
For the real hero from a photograph, use tools/hero.py (same recipe, real subject).

Pillow only. Fonts fall back to Pillow's bitmap font if Helvetica isn't found.
"""
from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "src" / "assets" / "img"
STRIP = IMG / "strip"
STRIP.mkdir(parents=True, exist_ok=True)

random.seed(2004)


def font(size):
    for path in (
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def grain(im, amount=18):
    """Film grain: per-pixel noise on an L image."""
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            v = px[x, y] + random.randint(-amount, amount)
            px[x, y] = max(0, min(255, v))
    return im


def dither(im):
    """Two-tone Floyd–Steinberg, then back to L so it saves as JPEG cleanly."""
    return im.convert("1", dither=Image.FLOYDSTEINBERG).convert("L")


def caption(im, lines, size=11, anchor="lb", pad=12):
    d = ImageDraw.Draw(im)
    f = font(size)
    w, h = im.size
    y = h - pad
    for line in reversed(lines):
        bbox = d.textbbox((0, 0), line, font=f)
        lh = bbox[3] - bbox[1] + 4
        d.rectangle((pad - 4, y - lh, pad + bbox[2] + 4, y + 2), fill=0)
        d.text((pad, y - lh + 2), line, font=f, fill=255)
        y -= lh + 2
    return im


def hero():
    """640×340. A soft head-shaped mass on the left, fading to black on the
    right where the greeting sits. High contrast, like the reference."""
    w, h = 640, 340
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    # A blurred oval where a face would be.
    d.ellipse((20, 30, 330, 360), fill=120)
    d.ellipse((90, 90, 230, 250), fill=175)
    im = im.filter(ImageFilter.GaussianBlur(28))
    # Fade to black across the right half.
    mask = Image.linear_gradient("L").rotate(90, expand=True).resize((w, h))
    mask = mask.point(lambda v: 255 if v < 100 else max(0, 255 - int((v - 100) * 3.2)))
    black = Image.new("L", (w, h), 0)
    im = grain(im, 22)
    im = Image.composite(im, black, mask)
    im = dither(im)
    # Hard black from x=400: the greeting sits there and needs a clean ground.
    ImageDraw.Draw(im).rectangle((400, 0, w, h), fill=0)
    caption(im, ["PLACEHOLDER  —  home-hero.jpg  640 × 340",
                 "SUBJECT ON THE LEFT · RIGHT HALF FADES TO BLACK"])
    im.save(IMG / "home-hero.jpg", quality=88)


def portrait():
    w, h = 200, 260
    im = Image.new("L", (w, h), 40)
    d = ImageDraw.Draw(im)
    d.ellipse((40, 30, 160, 170), fill=190)
    d.rectangle((30, 170, 170, 260), fill=170)
    im = im.filter(ImageFilter.GaussianBlur(14))
    im = grain(im, 20)
    im = dither(im)
    caption(im, ["PLACEHOLDER", "portrait.jpg  200 × 260"], size=10, pad=8)
    im.save(IMG / "portrait.jpg", quality=88)


def strips():
    """NOT placeholders any more. Dario saw the dithered static and kept it
    (2026-09-09): "eerie and weird, like some weird static." Six bands of light
    in a black field, one shown at random per visit. No captions."""
    w, h = 640, 40
    shapes = {
        1: lambda d: d.rectangle((0, 22, w, 26), fill=200),                       # horizon
        2: lambda d: d.rectangle((280, 0, 360, h), fill=170),                     # doorway
        3: lambda d: d.polygon([(0, h), (w, h), (330, 0), (310, 0)], fill=160),  # road
        4: lambda d: (d.ellipse((150, 14, 162, 26), fill=230),                    # two lights, far apart
                      d.ellipse((470, 14, 482, 26), fill=230)),
        5: lambda d: d.line([(0, 30), (120, 22), (260, 34), (330, 8), (420, 28), (640, 12)],
                            fill=255, width=5),                                   # the crack
        6: lambda d: d.rectangle((40, 6, 600, 34), outline=220, width=6),         # a window
    }
    for i, draw in shapes.items():
        im = Image.new("L", (w, h), 0)
        draw(ImageDraw.Draw(im))
        im = im.filter(ImageFilter.GaussianBlur(6 if i < 5 else 2))
        im = im.point(lambda v: v if v > 40 else 0)
        im = grain(im, 14)
        im = dither(im)
        im.save(STRIP / f"0{i}.jpg", quality=88)


def signature():
    """240×60, transparent, white ink. A scribble that reads as a signature
    without pretending to be his."""
    w, h = 240, 60
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = []
    x = 8
    while x < w - 40:
        pts.append((x, 30 + random.randint(-16, 16)))
        x += random.randint(6, 14)
    d.line(pts, fill=(255, 255, 255, 255), width=2, joint="curve")
    f = font(9)
    d.text((w - 96, h - 12), "signature.png 240×60", font=f, fill=(255, 255, 255, 160))
    im.save(IMG / "signature.png")


if __name__ == "__main__":
    hero()
    portrait()
    strips()
    signature()
    print("placeholders written to", IMG)
