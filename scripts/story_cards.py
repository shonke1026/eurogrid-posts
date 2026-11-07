"""Make Instagram Story frames (1080x1920 JPEG) for race flashes.

python3 scripts/story_cards.py spec.json out_dir
spec: {"event": "カタールGP", "session": "MotoGP スプリント",
       "frames": [
         {"kind": "spoiler"},
         {"kind": "result", "heading": "結果", "rows": [["1", "名前", "チーム"], ...], "note": "…"},
         {"kind": "quote", "pos": "1位", "name": "名前", "quote": "訳", "source": "出典"},
         {"kind": "end", "text": "論調比較は翌朝に"}]}
Frame 1 should always be "spoiler" so the result is only seen after a tap.
Needs rsvg-convert and Pillow; fonts: Noto Sans CJK JP, Inter.
"""
import json, pathlib, subprocess, sys, textwrap
from xml.sax.saxutils import escape as e
from PIL import Image

NAVY, CREAM, YEL, GREY = "#0B1220", "#F2EEE6", "#F5B700", "#3A4558"
W, H = 1080, 1920
JP = "Noto Sans CJK JP, Noto Sans JP, sans-serif"


def grid(y0=1400):
    s = ""
    for i, x in enumerate(range(140, 1000, 170)):
        c = YEL if i == 2 else GREY
        yy = y0 + (40 if i % 2 else 0)
        s += f'<path d="M{x} {yy+110} V{yy} H{x+100} V{yy+110}" fill="none" stroke="{c}" stroke-width="12"/>'
    return s


def head(spec):
    return (f'<text x="80" y="330" font-family="Inter" font-weight="700" font-size="52" fill="{CREAM}">Eurogrid</text>'
            f'<text x="80" y="395" font-family="{JP}" font-size="36" fill="{YEL}">{e(spec["event"])}｜{e(spec["session"])}</text>')


def wrap(t, n):
    out = []
    for para in t.split("\n"):
        out += textwrap.wrap(para, n) or [""]
    return out


def frame(spec, f):
    b = f'<rect width="{W}" height="{H}" fill="{NAVY}"/>' + head(spec)
    k = f["kind"]
    if k == "spoiler":
        b += (f'<path d="M540 600 L640 780 H440 Z" fill="{YEL}"/><rect x="532" y="650" width="16" height="70" fill="{NAVY}"/><rect x="532" y="735" width="16" height="18" fill="{NAVY}"/>'
              f'<text x="540" y="920" text-anchor="middle" font-family="{JP}" font-weight="700" font-size="76" fill="{CREAM}">ネタバレ注意</text>'
              f'<text x="540" y="1020" text-anchor="middle" font-family="{JP}" font-size="44" fill="{CREAM}">{e(spec["session"])}の結果が出ます</text>'
              f'<text x="540" y="1180" text-anchor="middle" font-family="{JP}" font-size="40" fill="{YEL}">見たい人だけ、タップして次へ →</text>')
    elif k == "result":
        b += f'<text x="80" y="540" font-family="{JP}" font-weight="700" font-size="72" fill="{CREAM}">{e(f.get("heading","結果"))}</text>'
        y = 680
        for r in f["rows"]:
            b += (f'<text x="80" y="{y}" font-family="Inter" font-weight="700" font-size="72" fill="{YEL}">{e(r[0])}</text>'
                  f'<text x="200" y="{y}" font-family="{JP}" font-weight="700" font-size="56" fill="{CREAM}">{e(r[1])}</text>')
            if len(r) > 2:
                b += f'<text x="200" y="{y+52}" font-family="{JP}" font-size="34" fill="#AEB6C4">{e(r[2])}</text>'
            y += 150
        for i, ln in enumerate(wrap(f.get("note", ""), 22)):
            b += f'<text x="80" y="{y+40+i*58}" font-family="{JP}" font-size="40" fill="{CREAM}">{e(ln)}</text>'
    elif k == "quote":
        b += (f'<text x="80" y="540" font-family="Inter" font-weight="700" font-size="64" fill="{YEL}">{e(f["pos"])}</text>'
              f'<text x="80" y="630" font-family="{JP}" font-weight="700" font-size="64" fill="{CREAM}">{e(f["name"])}</text>'
              f'<rect x="80" y="680" width="10" height="440" fill="{YEL}"/>')
        for i, ln in enumerate(wrap(f["quote"], 16)):
            b += f'<text x="120" y="{740+i*80}" font-family="{JP}" font-size="54" fill="{CREAM}">{e(ln)}</text>'
        b += f'<text x="80" y="1300" font-family="{JP}" font-size="32" fill="#AEB6C4">出典：{e(f["source"])}</text>'
    elif k == "end":
        for i, ln in enumerate(wrap(f.get("text", ""), 15)):
            b += f'<text x="540" y="{820+i*80}" text-anchor="middle" font-family="{JP}" font-size="54" fill="{CREAM}">{e(ln)}</text>'
        b += f'<text x="540" y="1100" text-anchor="middle" font-family="{JP}" font-size="40" fill="{YEL}">ふたつの視点、ひとつのグリッド。</text>'
    b += grid() + f'<text x="540" y="1600" text-anchor="middle" font-family="Inter" font-size="34" fill="#AEB6C4">@eurogrid_jp</text>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">{b}</svg>'


def main():
    spec = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    names = []
    for i, f in enumerate(spec["frames"], 1):
        svg = out / f"s{i}.svg"; png = out / f"s{i}.png"; jpg = out / f"s{i}.jpg"
        svg.write_text(frame(spec, f), encoding="utf-8")
        subprocess.run(["rsvg-convert", "-o", str(png), str(svg)], check=True)
        Image.open(png).convert("RGB").save(jpg, quality=92)
        svg.unlink(); png.unlink(); names.append(jpg.name)
    print(json.dumps(names))


if __name__ == "__main__":
    main()
