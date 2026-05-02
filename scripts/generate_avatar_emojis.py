#!/usr/bin/env python3
"""
Generate MVP static emoji set from a base avatar image.

Output files are PNGs named by emotion key so they can be loaded by
`emoji_collection` directly.
"""

from pathlib import Path
import shutil
from PIL import Image, ImageDraw, ImageOps


EMOTIONS = ["idle", "neutral", "happy", "sad", "angry", "surprised"]
ALIASES = {
    "laughing": "happy",
    "funny": "happy",
    "loving": "happy",
    "winking": "happy",
    "cool": "happy",
    "delicious": "happy",
    "kissy": "happy",
    "confident": "happy",
    "relaxed": "neutral",
    "embarrassed": "sad",
    "crying": "sad",
    "sleepy": "neutral",
    "silly": "happy",
    "confused": "sad",
    "thinking": "neutral",
    "shocked": "surprised",
}


def load_base(src: Path, size: int = 128) -> Image.Image:
    img = Image.open(src).convert("L")
    img = ImageOps.exif_transpose(img)
    # Keep the middle area and normalize to line-art style.
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    img = ImageOps.autocontrast(img, cutoff=1)
    img = img.point(lambda p: 255 if p > 160 else 0, mode="1").convert("L")
    return img


def draw_mouth(draw: ImageDraw.ImageDraw, emotion: str) -> None:
    # Approximate mouth position for the given portrait orientation.
    if emotion in ("idle", "neutral"):
        draw.line((35, 85, 53, 84), fill=0, width=2)
    elif emotion == "happy":
        draw.line((34, 82, 44, 88), fill=0, width=2)
        draw.line((44, 88, 54, 82), fill=0, width=2)
    elif emotion == "sad":
        draw.line((34, 88, 44, 81), fill=0, width=2)
        draw.line((44, 81, 54, 88), fill=0, width=2)
    elif emotion == "angry":
        draw.line((34, 86, 54, 84), fill=0, width=3)
    elif emotion == "surprised":
        draw.ellipse((39, 79, 50, 90), outline=0, width=2)


def draw_eyebrow(draw: ImageDraw.ImageDraw, emotion: str) -> None:
    # One visible eyebrow near the eye.
    if emotion == "angry":
        draw.line((39, 52, 53, 48), fill=0, width=3)
    elif emotion == "sad":
        draw.line((39, 49, 53, 54), fill=0, width=2)
    elif emotion == "surprised":
        draw.arc((38, 43, 54, 55), start=200, end=340, fill=0, width=2)


def make_emotion(base: Image.Image, emotion: str) -> Image.Image:
    out = base.copy().convert("L")
    draw = ImageDraw.Draw(out)
    # Light patch to overwrite original mouth/eyebrow then redraw expression.
    draw.rectangle((31, 73, 60, 95), fill=255)
    draw.rectangle((36, 43, 57, 57), fill=255)
    draw_mouth(draw, emotion)
    draw_eyebrow(draw, emotion)
    return out


def main() -> None:
    src = Path("/Users/linf/Desktop/TX7TW-Mp_400x400.jpg")
    out_dir = Path("/Users/linf/esp/xiaozhi-esp32/main/assets/custom-avatar-emoji")
    out_dir.mkdir(parents=True, exist_ok=True)

    base = load_base(src)
    for emotion in EMOTIONS:
        img = make_emotion(base, emotion)
        img.save(out_dir / f"{emotion}.png", optimize=True)

    for alias, target in ALIASES.items():
        src_file = out_dir / f"{target}.png"
        dst_file = out_dir / f"{alias}.png"
        shutil.copyfile(src_file, dst_file)

    print(f"Generated {len(EMOTIONS) + len(ALIASES)} files in {out_dir}")


if __name__ == "__main__":
    main()
