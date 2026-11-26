"""Vector terrain for the Recorrido tab, traced from satellite tiles.

The map is the 2x3 block of zoom-15 Esri World Imagery tiles around the Brisas -> Valle de las
Tumbas road (the six "chunks"). Their zoom-16 children are stitched, clouds over the north are
masked and filled from the terrain around them, every pixel gets one of a few terrain classes
(paramo greens, volcanic ash and rock, the ash-covered glacier) and each chunk's classes are traced
with potrace into flat paths colored from the scene palette at runtime.

Writes mobile/src/recorrido/trailMap.generated.ts. Tiles are cached under .cache/ (gitignored);
the imagery itself is never committed.

Run: uv run --with pillow --with numpy python -I experiments/trail_map/build_trail_map.py
Needs the potrace binary on PATH. --preview DIR also writes an SVG and a PNG of the map per run.
"""

from __future__ import annotations

import argparse
import math
import re
import subprocess
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
CACHE = Path(__file__).resolve().parent / ".cache"
OUT = ROOT / "mobile/src/recorrido/trailMap.generated.ts"
TILE_URL = (
    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
)

# The user's six chunks are zoom-15 tiles x 9524..9525, y 15934..15936 (2 columns, 3 rows),
# with one more row on each side: the app shows the map south-up, and these rows give terrain
# around both ends of the route on a phone screen. Hand-tuned zones below are fractions of the
# six chunks' height, measured from their first row (TUNED_ROW0).
CHUNK_Z = 15
CHUNK_X0 = 9524
CHUNK_Y0 = 15933
COLS = 2
ROWS = 5
TUNED_ROW0 = 1
TUNED_ROWS = 3
DETAIL = 1  # trace zoom = CHUNK_Z + DETAIL, so each chunk is 2**DETAIL tiles across
TILE = 256
CHUNK_PX = TILE * 2**DETAIL
# Classes are found at the detail zoom, then traced at this many units per chunk: the map shows
# a chunk at 300-500 pt, so finer paths only add bytes.
TRACE_PX = 256
# Paths overlap their neighbours by this many units, so smoothed edges never leave a seam.
PAD = 4

# Paint order, bottom to top. Each layer is traced as the union of its class and every class
# above it, so the layers nest and the base never shows through a gap between two shapes.
CLASSES = ("rock", "ash", "ashPale", "rockDark", "paramoDry", "paramo", "paramoDark", "ravine")

# Potrace: drop specks under TURD units², corner smoothing ALPHA, curve merge tolerance OPT.
TURD = 260
ALPHA = 1.3
OPT = 1.2


@dataclass(frozen=True)
class Bounds:
    north: float
    south: float
    west: float
    east: float


def tile_lon(x: float, z: int) -> float:
    return x / 2**z * 360 - 180


def tile_lat(y: float, z: int) -> float:
    return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / 2**z))))


def map_bounds() -> Bounds:
    return Bounds(
        north=tile_lat(CHUNK_Y0, CHUNK_Z),
        south=tile_lat(CHUNK_Y0 + ROWS, CHUNK_Z),
        west=tile_lon(CHUNK_X0, CHUNK_Z),
        east=tile_lon(CHUNK_X0 + COLS, CHUNK_Z),
    )


def fetch_mosaic() -> Image.Image:
    z = CHUNK_Z + DETAIL
    n = 2**DETAIL
    CACHE.mkdir(exist_ok=True)
    mosaic = Image.new("RGB", (COLS * CHUNK_PX, ROWS * CHUNK_PX))
    for j in range(ROWS * n):
        for i in range(COLS * n):
            x, y = CHUNK_X0 * n + i, CHUNK_Y0 * n + j
            path = CACHE / f"z{z}_{y}_{x}.jpg"
            if not path.exists():
                req = urllib.request.Request(
                    TILE_URL.format(z=z, y=y, x=x), headers={"User-Agent": "trail-map-build"}
                )
                with urllib.request.urlopen(req, timeout=30) as res:
                    path.write_bytes(res.read())
            with Image.open(path) as tile:
                mosaic.paste(tile.convert("RGB"), (i * TILE, j * TILE))
    return mosaic


def _box(a: np.ndarray, r: int, axis: int) -> np.ndarray:
    a = np.moveaxis(a, axis, 0)
    padded = np.concatenate([np.repeat(a[:1], r + 1, 0), a, np.repeat(a[-1:], r, 0)], 0)
    cs = np.cumsum(padded, 0, dtype=np.float64)
    return np.moveaxis(
        ((cs[2 * r + 1 :] - cs[: -2 * r - 1]) / (2 * r + 1)).astype(np.float32), 0, axis
    )


def blur(a: np.ndarray, sigma: float) -> np.ndarray:
    """Gaussian-like blur of a 2D float array: three box passes per axis."""
    r = max(1, round(sigma * 0.87))
    for _ in range(3):
        a = _box(_box(a, r, 0), r, 1)
    return a


def remove_clouds(rgb: np.ndarray) -> np.ndarray:
    """Clouds sit over the green north: bright and grey there (ash and the glacier are warmer or
    lie outside that zone). Masked pixels are filled from the terrain around them, coarser rings
    first reaching into the middle of each cloud."""
    h, w, _ = rgb.shape
    yy, xx = np.mgrid[0:h, 0:w]
    ref = w * TUNED_ROWS / COLS
    yy = yy - w * TUNED_ROW0 / COLS
    lum = rgb.mean(-1)
    warmth = rgb[..., 0] - rgb[..., 2]
    zone = (yy < 0.43 * ref) & ~((xx > 0.67 * w) & (yy > 0.29 * ref))
    cloud = ((lum > 88) & (warmth < 38) & zone).astype(np.float32)
    cloud = (blur(cloud, 7 * w / 1024) > 0.12) & zone
    known = ~cloud
    out = rgb.copy()
    for r in (3, 6, 12, 24, 48, 96):
        sigma = r * w / 1024
        k = known.astype(np.float32)
        den = blur(k, sigma)
        est = (
            np.stack([blur(out[..., c] * k, sigma) for c in range(3)], -1)
            / np.maximum(den, 1e-6)[..., None]
        )
        new = ~known & (den > 0.2)
        out[new] = est[new]
        known |= new
    out[~known] = est[~known]
    return out


def classify(rgb: np.ndarray) -> np.ndarray:
    """One class index (into CLASSES) per pixel: vegetated (saturated, darker, mostly north) vs
    volcanic, each split by brightness; near-black ravines and shadows on top."""
    h, w, _ = rgb.shape
    s = w / 1024
    yy = np.mgrid[0:h, 0:w][0]
    lum = rgb.mean(-1)
    warmth = rgb[..., 0] - rgb[..., 2]
    top, low = rgb.max(-1), rgb.min(-1)
    sat = (top - low) / np.maximum(top, 1)
    # Tones from a wide blur: the map shows terrain, not every rock and shadow in the photo.
    soft = blur(lum, 9 * s)
    near = blur(lum, 10 * s)
    # The north is paramo under its clouds and shadows; the prior fades out by the ash plateau.
    ref = w * TUNED_ROWS / COLS
    yy = yy - w * TUNED_ROW0 / COLS
    north = np.clip((0.4 * ref - yy) / (0.14 * ref), 0, 1)
    score = np.minimum(blur(sat, 10 * s) - 0.47, blur(sat, 30 * s) - 0.43)
    score += north * np.clip((104 - near) / 40, 0, 1) * 0.25
    veg = (blur(score, 6 * s) > 0) & (near < 110)

    idx = {name: i for i, name in enumerate(CLASSES)}
    lab = np.full(lum.shape, idx["rock"], np.uint8)
    lab[~veg & (soft >= 118)] = idx["ash"]
    lab[~veg & (soft >= 118) & (warmth < 30)] = idx["ashPale"]
    lab[~veg & (soft < 80)] = idx["rockDark"]
    lab[veg & (soft >= 82)] = idx["paramoDry"]
    lab[veg & (soft < 82) & (soft >= 55)] = idx["paramo"]
    lab[veg & (soft < 55)] = idx["paramoDark"]
    lab[soft < 30] = idx["ravine"]
    im = Image.fromarray(lab, mode="L")
    for _ in range(3):
        im = im.filter(ImageFilter.ModeFilter(13))
    return np.asarray(im)


_NUM = re.compile(r"-?\d+(?:\.\d+)?")


def trace(mask: np.ndarray, dx: int, dy: int) -> str:
    """Potrace one boolean mask into SVG path data in mask pixels, y down, shifted by (dx, dy).
    The bitmap goes in upside down so potrace's y-up output reads as y-down."""
    if not mask.any():
        return ""
    with tempfile.TemporaryDirectory() as tmp:
        pbm = Path(tmp) / "m.pbm"
        Image.fromarray(np.where(np.flipud(mask), 0, 255).astype(np.uint8)).convert("1").save(pbm)
        svg = subprocess.run(
            [
                "potrace",
                "-b",
                "svg",
                "-u",
                "1",
                "--flat",
                "-t",
                str(TURD),
                "-a",
                str(ALPHA),
                "-O",
                str(OPT),
                "-o",
                "-",
                str(pbm),
            ],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    if "scale(1.000000,-1.000000)" not in svg:
        raise RuntimeError("potrace output changed: expected a y-flip transform")
    parts = re.findall(r'<path d="([^"]*)"', svg)
    d = " ".join(" ".join(p.split()) for p in parts)
    # Only absolute moves (M) carry a position; everything after them is relative.
    return re.sub(
        r"M(-?\d+) (-?\d+)",
        lambda m: f"M{int(m.group(1)) + dx} {int(m.group(2)) + dy}",
        d,
    )


def chunk_layers(labels: np.ndarray, col: int, row: int) -> list[tuple[int, str]]:
    h, w = labels.shape
    x0, y0 = col * TRACE_PX - PAD, row * TRACE_PX - PAD
    ys = np.clip(np.arange(y0, y0 + TRACE_PX + 2 * PAD), 0, h - 1)
    xs = np.clip(np.arange(x0, x0 + TRACE_PX + 2 * PAD), 0, w - 1)
    crop = labels[np.ix_(ys, xs)]
    layers = []
    for k in range(1, len(CLASSES)):
        d = trace(crop >= k, -PAD, -PAD)
        if d:
            layers.append((k, d))
    return layers


def emit(chunks: list[list[tuple[int, str]]], bounds: Bounds) -> str:
    lines = [
        "// Generated by experiments/trail_map/build_trail_map.py. Do not edit.",
        "// Terrain traced from Esri World Imagery (sources: Esri, Maxar, Earthstar Geographics).",
        "",
        f"export const TRAIL_CLASSES = [{', '.join(repr(c) for c in CLASSES)}] as const;",
        "",
        "/** [index into TRAIL_CLASSES, path data]; a chunk's base is class 0. */",
        "export type TrailLayer = readonly [number, string];",
        "",
        "export const TRAIL_MAP = {",
        f"  bounds: {{ north: {bounds.north!r}, south: {bounds.south!r}, west: {bounds.west!r}, east: {bounds.east!r} }},",
        f"  cols: {COLS},",
        f"  rows: {ROWS},",
        "  /** Path units across one chunk; paths spill PAD units past its edges. */",
        f"  size: {TRACE_PX},",
        "  /** Row-major, north-west first. */",
        "  chunks: [",
    ]
    for layers in chunks:
        lines.append("    [")
        lines += [f"      [{k}, '{d}']," for k, d in layers]
        lines.append("    ],")
    lines += ["  ] as readonly (readonly TrailLayer[])[],", "};", ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", type=Path, help="write map.svg and map.png here")
    args = parser.parse_args()

    rgb = np.asarray(fetch_mosaic().filter(ImageFilter.GaussianBlur(2)), dtype=np.float32)
    labels = classify(remove_clouds(rgb))
    step = CHUNK_PX // TRACE_PX
    # The mode filter in classify() already smoothed the classes, so plain subsampling is safe.
    labels = labels[step // 2 :: step, step // 2 :: step]
    chunks = [chunk_layers(labels, c, r) for r in range(ROWS) for c in range(COLS)]
    text = emit(chunks, map_bounds())
    OUT.write_text(text)
    for i, layers in enumerate(chunks):
        size = sum(len(d) for _, d in layers)
        print(f"chunk {i + 1}: {len(layers)} layers, {size / 1024:.1f} KB path data")
    print(f"total {len(text.encode()) / 1024:.1f} KB -> {OUT.relative_to(ROOT)}")
    if args.preview:
        write_preview(chunks, args.preview)


def write_preview(chunks: list[list[tuple[int, str]]], out: Path) -> None:
    """Flat preview colors (the app derives its own from the scene palette)."""
    colors = [
        "#9a7f72",
        "#d4ae95",
        "#dcd6e6",
        "#5f4c47",
        "#a7a16f",
        "#93984a",
        "#5a5d2b",
        "#3d3233",
    ]
    out.mkdir(parents=True, exist_ok=True)
    body = []
    for i, layers in enumerate(chunks):
        c, r = i % COLS, i // COLS
        body.append(
            f'<svg x="{c * TRACE_PX}" y="{r * TRACE_PX}" width="{TRACE_PX}" height="{TRACE_PX}" '
            f'viewBox="0 0 {TRACE_PX} {TRACE_PX}"><rect width="{TRACE_PX}" height="{TRACE_PX}" fill="{colors[0]}"/>'
            + "".join(f'<path fill="{colors[k]}" d="{d}"/>' for k, d in layers)
            + "</svg>"
        )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{COLS * TRACE_PX}" height="{ROWS * TRACE_PX}">'
        + "".join(body)
        + "</svg>"
    )
    (out / "map.svg").write_text(svg)
    subprocess.run(["rsvg-convert", "-o", str(out / "map.png"), str(out / "map.svg")], check=True)


if __name__ == "__main__":
    main()
