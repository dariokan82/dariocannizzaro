#!/usr/bin/env python3
"""Turn one of Dario's photographs into the home hero.

Same recipe as the strips and the placeholder hero (tools/placeholders.py):
grey → tone → blur → grain → fade to black on the right → Floyd–Steinberg
to pure black and white. The dither is what makes it read as a ghost in the
static; everything before it only shapes the tonal curve the dither sees.

    python3 tools/hero.py path/to/photo.jpg              # writes home-hero.jpg
    python3 tools/hero.py photo.jpg --sheet /tmp/sheet.jpg  # + contact sheet of variants
    python3 tools/hero.py photo.jpg --anchor center --flip --gamma 1.6 --blur 2

Start from a CLEAN photo: unfiltered, colour is fine, wider than 640px.
Side light and a dark background dither best; flat light turns to mush.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

from placeholders import IMG, dither, grain

W, H = 640, 340
BLACK_FROM = 400  # the greeting sits right of here and needs clean ground


def frame(im, anchor="left", zoom=1.0, fit=False):
    """Cover-crop to 640×340. `anchor` picks which part of the photo survives
    when the aspect doesn't match; `zoom` > 1 crops tighter. `fit` instead
    scales the whole photo to the frame height and sets it on black at the
    anchor — right for a portrait that already sits on a dark ground."""
    im = ImageOps.exif_transpose(im).convert("L")
    if fit:
        scale = H / im.height * zoom
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        canvas = Image.new("L", (W, H), 0)
        x = {"left": 0, "center": (W - im.width) // 2, "right": W - im.width}[anchor]
        canvas.paste(im, (x, (H - im.height) // 2))
        return canvas
    scale = max(W / im.width, H / im.height) * zoom
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    x = {"left": 0, "center": (im.width - W) // 2, "right": im.width - W}[anchor]
    y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def tone(im, gamma=1.3, cutoff=1):
    """Stretch the levels, then sink the midtones so the face rises out of
    black instead of floating on grey."""
    im = ImageOps.autocontrast(im, cutoff=cutoff)
    lut = [round(255 * (v / 255) ** gamma) for v in range(256)]
    return im.point(lut)


def fade(im, start=100):
    """Right-hand fade to black, same mask as the placeholder hero, then a
    hard black block where the text goes. `start` (0–255 across the width,
    100 ≈ x=250) is where the fade begins; the placeholder used 100."""
    mask = Image.linear_gradient("L").rotate(90, expand=True).resize((W, H))
    span = max(1, 180 - start)
    mask = mask.point(lambda v: 255 if v < start else max(0, 255 - int((v - start) * 255 / span)))
    im = Image.composite(im, Image.new("L", (W, H), 0), mask)
    ImageDraw.Draw(im).rectangle((BLACK_FROM, 0, W, H), fill=0)
    return im


def render(src, anchor="left", zoom=1.0, flip=False, fit=False, fade_start=100,
           invert=False, trim=0, gamma=1.3, blur=1.5, grain_amount=18):
    src = ImageOps.exif_transpose(src).convert("L")
    if trim:
        src = src.crop((trim, trim, src.width - trim, src.height - trim))
    if invert:
        src = ImageOps.invert(src)
    im = frame(src, anchor, zoom, fit)
    if flip:
        im = ImageOps.mirror(im)
    im = tone(im, gamma)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    if grain_amount:
        im = grain(im, grain_amount)
    return dither(fade(im, fade_start))


def contact_sheet(src, path, **kw):
    """A few gamma/blur pairings side by side, labelled, so the pick is by eye."""
    variants = [(1.0, 1.0), (1.3, 1.5), (1.6, 1.5), (1.6, 3.0), (2.0, 2.0), (1.3, 0)]
    cols, pad = 2, 16
    rows = (len(variants) + cols - 1) // cols
    sheet = Image.new("L", (cols * (W + pad) + pad, rows * (H + pad + 18) + pad), 60)
    d = ImageDraw.Draw(sheet)
    for i, (g, b) in enumerate(variants):
        tile = render(src, gamma=g, blur=b, **kw)
        x = pad + (i % cols) * (W + pad)
        y = pad + (i // cols) * (H + pad + 18)
        sheet.paste(tile, (x, y))
        d.text((x, y + H + 4), f"gamma {g}   blur {b}", fill=255)
    sheet.save(path, quality=85)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("photo")
    p.add_argument("--out", default=str(IMG / "home-hero.jpg"))
    p.add_argument("--anchor", choices=["left", "center", "right"], default="left")
    p.add_argument("--zoom", type=float, default=1.0)
    p.add_argument("--flip", action="store_true", help="mirror, if the face is on the wrong side")
    p.add_argument("--trim", type=int, default=0, help="crop this many px off every edge of the source first (kills scan borders)")
    p.add_argument("--invert", action="store_true", help="negative first, for a subject on white")
    p.add_argument("--fit", action="store_true", help="scale to frame height and set on black instead of cover-cropping")
    p.add_argument("--fade-start", type=int, default=100, help="0-255 across the width; where the fade to black begins")
    p.add_argument("--gamma", type=float, default=1.3, help=">1 darkens midtones")
    p.add_argument("--blur", type=float, default=1.5)
    p.add_argument("--grain", type=float, default=18)
    p.add_argument("--sheet", help="also write a contact sheet of variants here")
    a = p.parse_args()

    src = Image.open(a.photo)
    kw = dict(anchor=a.anchor, zoom=a.zoom, flip=a.flip, fit=a.fit, fade_start=a.fade_start, invert=a.invert, trim=a.trim)
    render(src, gamma=a.gamma, blur=a.blur, grain_amount=int(a.grain), **kw).save(a.out, quality=88)
    print("wrote", a.out)
    if a.sheet:
        contact_sheet(src, a.sheet, grain_amount=int(a.grain), **kw)
        print("wrote", a.sheet)


if __name__ == "__main__":
    main()
