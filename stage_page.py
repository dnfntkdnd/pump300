"""Stage a viewer HTML into this GitHub Pages repo with a proper document head and Open Graph tags.
    python stage_page.py <src.html> <subdir or .> <og_image.png> "<og title>" "<og description>"
Example:
    python stage_page.py ../../demo09_igc/viewer/igc_viewer.html igc ../../demo09_igc/out/thumbs/yt_explode.png "기어 압축기 676조각" "..."
"""
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "https://dnfntkdnd.github.io/pump300/"


def stage(src, sub, og_img, title, desc):
    sub = "" if sub in (".", "") else sub.strip("/") + "/"
    dst_dir = HERE / sub if sub else HERE
    dst_dir.mkdir(parents=True, exist_ok=True)
    og_name = (sub.rstrip("/") or "pump300") + ".png"
    shutil.copy(og_img, HERE / "og" / og_name)
    s = Path(src).read_text(encoding="utf-8")
    s = re.sub(r"^<!doctype html>\s*<html[^>]*>\s*<head>\s*", "", s, flags=re.I)
    assert s.count('<meta charset="utf-8">') == 1
    og = ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
          f'<meta property="og:type" content="website">\n<meta property="og:title" content="{title}">\n<meta property="og:description" content="{desc}">\n'
          f'<meta property="og:url" content="{BASE}{sub}">\n<meta property="og:image" content="{BASE}og/{og_name}">\n<meta property="og:image:width" content="1280">\n<meta property="og:image:height" content="720">\n'
          f'<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="{title}">\n<meta name="twitter:image" content="{BASE}og/{og_name}">')
    s = s.replace('<meta charset="utf-8">', og, 1)
    s = re.sub(r'<meta name="viewport"[^>]*>\n(?=(?:.*\n)*?<meta name="viewport")', "", s)   # drop a second viewport tag if the source had one
    out = dst_dir / "index.html"
    out.write_text('<!doctype html>\n<html lang="ko">\n<head>\n' + s, encoding="utf-8")
    print(f"[ok] {out.relative_to(HERE)}  {out.stat().st_size / 1e6:.2f} MB  og/{og_name}")


if __name__ == "__main__":
    stage(*sys.argv[1:6])
