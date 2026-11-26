"""Export the MobileNet feature layer and reference embeddings. Photos stay outside mobile/."""
import argparse
import json
from pathlib import Path

import numpy as np
import onnx
from onnx import utils
import onnxruntime as ort
from PIL import Image, ImageOps


def embed(session, filename):
    with Image.open(filename) as photo:
        image = ImageOps.exif_transpose(photo).convert("RGB")
        side = min(image.size)
        x = (image.width - side) // 2
        y = (image.height - side) // 2
        image = image.crop((x, y, x + side, y + side)).resize((224, 224), Image.Resampling.BILINEAR)
        pixels = np.asarray(image, dtype=np.float32) / 255
    pixels = (pixels - np.float32([.485, .456, .406])) / np.float32([.229, .224, .225])
    vector = session.run(None, {"pixel_values": pixels.transpose(2, 0, 1)[None].copy()})[0].reshape(-1)
    norm = np.linalg.norm(vector)
    if not np.isfinite(norm) or norm == 0:
        raise ValueError(f"Invalid embedding: {filename}")
    return (vector / norm).round(6).tolist()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("photos", type=Path)
    args = parser.parse_args()
    mobile = Path(__file__).resolve().parents[1]
    if args.photos.resolve().is_relative_to(mobile):
        parser.error("Keep reference photographs outside mobile/")
    target = mobile / "assets" / "vision"
    classes = json.loads((target / "classes.json").read_text(encoding="utf-8-sig"))
    encoder = target / "encoder.onnx"
    utils.extract_model(str(args.model), str(encoder), ["pixel_values"], ["/flatten/Flatten_output_0"])
    onnx.checker.check_model(str(encoder))
    session = ort.InferenceSession(str(encoder), providers=["CPUExecutionProvider"])
    refs = []
    for label in [*classes, "other"]:
        directory = args.photos / label
        if label == "other" and not directory.exists():
            continue
        paths = sorted(path for path in directory.iterdir() if path.suffix.lower() in {".jpg", ".jpeg", ".png"})
        if len(paths) < 2:
            parser.error(f"Supply at least two independent references for {label}")
        refs.extend({"classId": label, "vector": embed(session, path)} for path in paths)
    (target / "index.json").write_text(
        json.dumps(refs, separators=(",", ":"), allow_nan=False) + "\n", encoding="utf-8"
    )
    print(f"{len(refs)} references, {len(refs[0]['vector'])} dimensions")


if __name__ == "__main__":
    main()
