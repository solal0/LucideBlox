import base64
import struct
from itertools import groupby
from io import BytesIO
from pathlib import Path

import cairosvg
from PIL import Image

SIZE = 64
COLOR = "#FFFFFF"

ROOT = Path(__file__).resolve().parent
ICONS = ROOT / "icons"
OUTPUT = ROOT / "lua"

def encode(image):
    image = image.convert("RGBA")
    width,height = image.size
    palette = {}
    indices = []

    for pixel in image.getdata():
        rgba = tuple(round(v*99/255) for v in pixel)
        indices.append(palette.setdefault(rgba,len(palette)))

    data = bytearray(struct.pack(">HHH",width,height,len(palette)))
    for rgba in palette:
        data.extend(rgba)

    for index,group in groupby(indices):
        count = sum(1 for _ in group)
        while count:
            run = min(count,65535)
            data.extend(struct.pack(">HH",run,index))
            count -= run

    return base64.b64encode(data).decode("ascii")

def main():
    if not 1 <= SIZE <= 1024:
        raise ValueError("SIZE must be between 1 and 1024.")

    icons = sorted(ICONS.glob("*.svg"))
    if not icons:
        raise FileNotFoundError(f"No SVG icons found in {ICONS}")

    OUTPUT.mkdir(exist_ok=True)
    for i,path in enumerate(icons,1):
        svg = path.read_text(encoding="utf-8").replace("currentColor",COLOR)
        png = cairosvg.svg2png(bytestring=svg.encode("utf-8"),output_width=SIZE,output_height=SIZE)
        with Image.open(BytesIO(png)) as image:
            data = encode(image)
        (OUTPUT / f"{path.stem}.lua").write_text(f"return[[{data}]]",encoding="ascii")
        if i%100 == 0 or i == len(icons):
            print(f"\r{i}/{len(icons)}",end="",flush=True)

    print(f"\nOutput: {OUTPUT}")

if __name__ == "__main__":
    main()
