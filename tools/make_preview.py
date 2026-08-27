#!/usr/bin/env python3
"""Regenerate preview.png: all 24 type icons on light and dark backgrounds.

Run from anywhere: python3 tools/make_preview.py  (requires Pillow)
"""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "Assets.xcassets"
OUT = ROOT / "preview.png"

ORDER = [
    # sixteen independent CityGML/CityJSON object types
    "Building", "TINRelief", "Road", "LandUse", "TransportSquare", "Bridge",
    "Railway", "GenericCityObject", "SolitaryVegetationObject", "Tunnel",
    "PlantCover", "WaterBody", "CityFurniture", "CityObjectGroup",
    "OtherConstruction", "Waterway",
    # eight building sub-types
    "BuildingPart", "BuildingInstallation", "BuildingUnit", "Storey",
    "Room", "BuildingFurniture", "ConstructiveElement", "HollowSpace",
]

CELL, PAD, LABEL_H, MARGIN, COLS = 128, 14, 26, 24, 6
ROWS = (len(ORDER) + COLS - 1) // COLS
PW = MARGIN * 2 + COLS * CELL + (COLS - 1) * PAD
PH = MARGIN * 2 + ROWS * (CELL + LABEL_H) + (ROWS - 1) * PAD + 44
GAP = 28

FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"
try:
    font = ImageFont.truetype(FONT_PATH, 15)
    small = ImageFont.truetype(FONT_PATH, 12)
except OSError:
    font = small = ImageFont.load_default()

def png_for(name):
    info = json.loads((CATALOG / f"{name}.imageset" / "Contents.json").read_text())
    entry = next(i for i in info["images"] if i["scale"] == "2x")
    return CATALOG / f"{name}.imageset" / entry["filename"]

def draw_panel(im, x0, bg, fg, sub, title):
    d = ImageDraw.Draw(im)
    d.text((x0 + MARGIN, 12), title, fill=sub, font=font)
    for i, name in enumerate(ORDER):
        r, c = divmod(i, COLS)
        x = x0 + MARGIN + c * (CELL + PAD)
        y = 44 + MARGIN + r * (CELL + LABEL_H + PAD)
        icon = Image.open(png_for(name)).convert("RGBA")
        im.paste(icon, (x, y), icon)
        f, tw = font, d.textlength(name, font=font)
        if tw > CELL - 2:
            f, tw = small, d.textlength(name, font=small)
        d.text((x + (CELL - tw) / 2, y + CELL + 7), name, fill=fg, font=f)

im = Image.new("RGB", (PW * 2 + GAP, PH), (255, 255, 255))
draw_panel(im, 0, (255, 255, 255), (60, 60, 67), (140, 140, 150),
           "azul icons — light background (24)")
draw_panel(im, PW + GAP, (28, 28, 30), (235, 235, 245), (130, 130, 140),
           "azul icons — dark background (24)")
im.save(OUT)
print("wrote", OUT, im.size)
