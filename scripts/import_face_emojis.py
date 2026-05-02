#!/usr/bin/env python3
from pathlib import Path
import shutil
from PIL import Image, ImageOps, ImageSequence


SRC_DIR = Path("/Users/linf/esp/media/face")
OUT_DIR = Path("/Users/linf/esp/xiaozhi-esp32/main/assets/face-emoji")
SIZE = (128, 128)


def fit_image(img: Image.Image) -> Image.Image:
    return ImageOps.fit(img.convert("RGBA"), SIZE, Image.Resampling.LANCZOS)


def save_png(src_name: str, dst_name: str) -> None:
    src = SRC_DIR / src_name
    dst = OUT_DIR / dst_name
    img = Image.open(src)
    fit_image(img).save(dst, format="PNG", optimize=True)


def save_gif(src_name: str, dst_name: str) -> None:
    src = SRC_DIR / src_name
    dst = OUT_DIR / dst_name
    gif = Image.open(src)
    frames = []
    durations = []
    for frame in ImageSequence.Iterator(gif):
        frames.append(fit_image(frame))
        durations.append(frame.info.get("duration", 100))
    if not frames:
        raise RuntimeError(f"No frames found in {src}")
    frames[0].save(
        dst,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )


def copy_alias(src_name: str, *alias_names: str) -> None:
    src = OUT_DIR / src_name
    for name in alias_names:
        shutil.copyfile(src, OUT_DIR / name)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for f in OUT_DIR.glob("*"):
        if f.is_file():
            f.unlink()

    # Base files from user assets
    save_png("idel_ori.png", "idle.png")
    save_gif("idel_ori.gif", "idle_anim.gif")
    save_gif("wakeup.gif", "wakeup.gif")
    save_gif("stop.gif", "stop.gif")
    save_png("Neutral.png", "neutral.png")
    save_png("Delight.png", "happy.png")
    save_png("Sorry.png", "sad.png")
    save_png("Speechless.png", "angry.png")
    save_png("Surprise.png", "surprised.png")
    save_png("Thinking.png", "thinking.png")

    # Emotion aliases used by server/fallbacks
    copy_alias("happy.png", "laughing.png", "funny.png", "loving.png", "winking.png", "cool.png", "delicious.png", "kissy.png", "confident.png", "silly.png")
    copy_alias("sad.png", "crying.png", "embarrassed.png", "confused.png")
    copy_alias("surprised.png", "shocked.png", "speechless.png")
    copy_alias("neutral.png", "relaxed.png", "sleepy.png")

    print(f"Generated face emojis in {OUT_DIR}")


if __name__ == "__main__":
    main()
