"""
Prep a portrait photo for ASCII conversion:
1. Remove the background (rembg) so the subject is isolated.
2. Boost local contrast with CLAHE so a flat headshot gets real
   highlights/shadows once it's reduced to a handful of ASCII glyphs.
3. Composite onto pure white so the background maps to the blank
   end of the ASCII ramp (white -> spaces).

Usage: python prep_photo.py source-photo.png
Output: source-prepped.png (grayscale, subject on white)
"""
import sys
import numpy as np
import cv2
from PIL import Image
from rembg import remove


def main(src_path: str) -> None:
    with open(src_path, "rb") as f:
        src_bytes = f.read()

    # 1. Remove background -> RGBA with alpha mask around the subject.
    cutout_bytes = remove(src_bytes)
    cutout = Image.open(__import__("io").BytesIO(cutout_bytes)).convert("RGBA")

    # 2. Composite onto pure white, with breathing room around the subject
    #    so the ASCII render reads as a portrait floating in space rather
    #    than a solid block filling the whole frame.
    pad_frac = 0.16
    w, h = cutout.size
    pad_w, pad_h = int(w * pad_frac), int(h * pad_frac)
    canvas_size = (w + 2 * pad_w, h + 2 * pad_h)
    white_bg = Image.new("RGBA", canvas_size, (255, 255, 255, 255))
    white_bg.alpha_composite(cutout, (pad_w, pad_h))
    composited = white_bg.convert("RGB")

    # 3. Mild CLAHE contrast boost (operates on the L channel in LAB space) —
    #    a soft, large-tile pass gives real highlights/shadows without
    #    amplifying skin/fabric texture into noise.
    arr = cv2.cvtColor(np.array(composited), cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(arr)
    clahe = cv2.createCLAHE(clipLimit=1.2, tileGridSize=(16, 16))
    l = clahe.apply(l)
    arr = cv2.merge((l, a, b))
    contrasted = cv2.cvtColor(arr, cv2.COLOR_LAB2RGB)

    gray = cv2.cvtColor(contrasted, cv2.COLOR_RGB2GRAY)
    # Smooth out the CLAHE-amplified texture (fabric weave, skin pores)
    # while keeping the actual facial/edge structure legible.
    gray = cv2.bilateralFilter(gray, d=9, sigmaColor=45, sigmaSpace=9)

    out_path = src_path.rsplit(".", 1)[0] + "-prepped.png"
    Image.fromarray(gray).save(out_path)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python prep_photo.py <source-photo>")
        sys.exit(1)
    main(sys.argv[1])
