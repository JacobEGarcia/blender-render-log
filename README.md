# Render Log

A portfolio of Blender work by Jacob E. Garcia — four procedural scenes shown with
the build scripts and render settings behind them.

**Live:** https://jacobegarcia.github.io/blender-render-log/

## What's here

| Piece | Engine | Notes |
| --- | --- | --- |
| The Fibonacci Reliquary | Cycles, GPU (HIP) | 5,281 bronze scales placed at the golden angle, 1600×2000 @ 144 spp |
| Chicago 2099 | EEVEE | Procedural night city, PBR + HDRI, 192-frame seamless loop |
| Wetware — Neural Cell Division | EEVEE | Driver-animated glass and subsurface cells, 240-frame loop |
| Kinetic Typography Field | EEVEE | Extruded text geometry orbiting a fixed centre, 240-frame loop |

Every scene is authored as a Python (`bpy`) build script, run headless from a clean
factory startup, and rendered to a frame sequence. The `.blend` is an output, not a
source — the script is what's version-controlled.

## Building

`index.html` references `assets/` and is what GitHub Pages serves.

```bash
python prep_assets.py   # renders/clips -> web-sized JPEG + MP4 in assets/
python bundle.py        # -> portfolio_selfcontained.html, every asset as a data: URI
```

`prep_assets.py` reads the source renders from the parent working directory and needs
`ffmpeg` on PATH. `bundle.py` produces a single-file version for hosts that block
external requests.

## Contact

jacobegarcia101@gmail.com · [github.com/JacobEGarcia](https://github.com/JacobEGarcia)
