"""Prepares web assets (JPEG stills + compressed MP4 loops) for the 3D portfolio site."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

# (source, output name, max width)
STILLS = [
    ("blender-showpiece/reliquary_hero.png", "reliquary-hero.jpg", 1400),
    ("blender-showpiece/proof.png", "reliquary-proof.jpg", 900),
    ("chicago_2099_ultra_preview.png", "chicago-ultra.jpg", 1600),
    ("chicago_2099_photoreal_preview_graded.png", "chicago-graded.jpg", 1600),
    ("chicago_2099_photoreal_frame_096.png", "chicago-frame-096.jpg", 1200),
    ("chicago_2099_photoreal_frame_193.png", "chicago-frame-193.jpg", 1200),
    ("wetware_neural_frames/frame_0120.png", "wetware-120.jpg", 1600),
    ("wetware_neural_frames/frame_0060.png", "wetware-060.jpg", 1200),
    ("wetware_neural_frames/frame_0200.png", "wetware-200.jpg", 1200),
    ("kinetic_typography_final_preview.png", "kinetic-hero.jpg", 1600),
    ("kinetic_typography_frame_060.png", "kinetic-060.jpg", 1200),
    ("kinetic_typography_frame_241.png", "kinetic-241.jpg", 1200),
]

# (source, output name, width, crf)
CLIPS = [
    ("chicago_2099_ultra_photoreal_loop.mp4", "chicago-loop.mp4", 960, 32),
    ("wetware_neural_cell_division.mp4", "wetware-loop.mp4", 960, 32),
    ("kinetic_typography_chicago_2099_v2.mp4", "kinetic-loop.mp4", 960, 32),
]


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FAILED: {' '.join(cmd[:6])}...\n{result.stderr[-600:]}", file=sys.stderr)
        return False
    return True


def main():
    for src, name, width in STILLS:
        source = ROOT / src
        if not source.exists():
            print(f"missing still: {src}", file=sys.stderr)
            continue
        dest = OUT / name
        run([
            "ffmpeg", "-y", "-loglevel", "error", "-i", str(source),
            "-vf", f"scale='min({width},iw)':-2:flags=lanczos",
            "-q:v", "4", str(dest),
        ])

    for src, name, width, crf in CLIPS:
        source = ROOT / src
        if not source.exists():
            print(f"missing clip: {src}", file=sys.stderr)
            continue
        dest = OUT / name
        run([
            "ffmpeg", "-y", "-loglevel", "error", "-i", str(source),
            "-vf", f"scale={width}:-2:flags=lanczos",
            "-c:v", "libx264", "-crf", str(crf), "-preset", "slow",
            "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart", str(dest),
        ])

    total = 0
    for path in sorted(OUT.iterdir()):
        size = path.stat().st_size
        total += size
        print(f"{path.name:28s} {size/1024:8.0f} KB")
    print(f"{'TOTAL':28s} {total/1048576:8.2f} MB")


if __name__ == "__main__":
    main()
