"""カルーセルの占有率を測る（デザイン仕様 v1.1、2026-11-14 運営者）。
python3 templates/check_fill.py <カルーセルの html>
- 各 section.slide で「使える高さ」（キッカーの上端から、下のロゴ行の上端まで）のうち、空いている部分を除いた割合を出す。70%未満は NG
  - 下に固定した箱（.diff、.end）は、その箱の高さだけを数える。箱があるだけで合格にならないよう、本文の下端と箱の上端のあいだの空きは空白として数える
- 表紙（1枚目）は、色面ブロック（.duo）の高さがページの半分（675px）以上かも見る
- 帯（.band）が全ページの上端にあるかも見る
終了コード：0＝全部OK、1＝NG あり
"""
import pathlib, sys
from playwright.sync_api import sync_playwright

JS = """() => [...document.querySelectorAll('section.slide')].map((s, i) => {
  const r = s.getBoundingClientRect();
  const rel = el => { const b = el.getBoundingClientRect(); return {top: b.top - r.top, bottom: b.bottom - r.top, h: b.height}; };
  const skip = el => el.matches('.band,.kicker,.n,.foot,.diff,.end') || el.closest('.foot,.diff,.end');
  let top = 1e9, bottom = 0;
  s.querySelectorAll('*').forEach(el => { if (skip(el)) return; if (el.children.length && !el.matches('.body')) {} const b = rel(el); if (b.h > 0 && getComputedStyle(el).visibility !== 'hidden') { top = Math.min(top, b.top); bottom = Math.max(bottom, b.bottom); } });
  const k = s.querySelector('.kicker'), f = s.querySelector('.foot'), band = s.querySelector('.band'), duo = s.querySelector('.duo');
  const areaTop = k ? rel(k).top : 72, areaBottom = f ? rel(f).top : r.height - 64;
  const boxH = [...s.querySelectorAll('.diff,.end')].reduce((a, el) => a + rel(el).h, 0);
  return {i: i + 1, fill: (bottom - areaTop + boxH) / (areaBottom - areaTop), band: !!band && rel(band).top <= 0.5, duo: duo ? rel(duo).h : null};
})"""


def main(path):
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        pg.goto(pathlib.Path(path).resolve().as_uri())
        pg.wait_for_timeout(600)
        rows = pg.evaluate(JS)
        b.close()
    ng = 0
    for r in rows:
        msgs = []
        if r["fill"] < 0.70:
            msgs.append(f"占有率 {r['fill']:.0%}（70%未満）")
        if not r["band"]:
            msgs.append("上端に帯がない")
        if r["i"] == 1 and (r["duo"] or 0) < 675:
            msgs.append(f"表紙の色面が {r['duo'] or 0:.0f}px（675px＝半分未満）")
        ng += bool(msgs)
        print(f"{r['i']}枚目: 占有率 {r['fill']:.0%}" + (" NG " + "、".join(msgs) if msgs else " OK"))
    return 1 if ng else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__); sys.exit(2)
    sys.exit(main(sys.argv[1]))
