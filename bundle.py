"""Inlines every asset into a single self-contained HTML file.

index.html references ./assets/* and is what gets deployed to a static host.
This produces portfolio_selfcontained.html, which carries the same page with
every image and clip embedded as a data: URI - needed anywhere external
requests are blocked (Claude Artifacts) or when the page travels as one file.
"""

import base64
import mimetypes
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "index.html"
DEST = HERE / "portfolio_selfcontained.html"

def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def main():
    html = SRC.read_text(encoding="utf-8")

    missing = []

    def swap(match):
        rel = match.group(1)
        asset = HERE / rel
        if not asset.exists():
            missing.append(rel)
            return match.group(0)
        return f'src="{data_uri(asset)}"'

    html = re.sub(r'src="(assets/[^"]+)"', swap, html)

    if missing:
        raise SystemExit(f"missing assets: {missing}")

    DEST.write_text(html, encoding="utf-8")
    size = DEST.stat().st_size
    print(f"{DEST.name}  {size/1048576:.2f} MB  (artifact cap is 16 MB)")
    if size > 16 * 1024 * 1024:
        raise SystemExit("over the 16 MB artifact limit")


if __name__ == "__main__":
    main()
