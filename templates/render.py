"""templates/*.html を画像にする。
python3 templates/render.py <html> <出力先> [--jpg]
- ig_explainer.html は section.slide ごとに <出力先>/c1.jpg… を作る
- それ以外は1枚。note は2倍（deviceScaleFactor 2）、ほかは等倍で指定サイズ
"""
import pathlib, sys
from playwright.sync_api import sync_playwright
src = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]); jpg = "--jpg" in sys.argv
size = {"note_eyecatch":(1280,670,2),"note_compare":(1280,960,2),"ig_explainer":(1080,1350,1),"ig_result":(1080,1350,1),"cover_1920":(1080,1920,1),"x_image":(1600,900,1)}
w,h,s = size.get(src.stem,(1280,670,2))
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":w,"height":h}, device_scale_factor=s)
    pg.goto(src.as_uri()); pg.wait_for_timeout(600)
    slides = pg.query_selector_all("section.slide")
    if slides:
        out.mkdir(parents=True, exist_ok=True)
        for i, el in enumerate(slides, 1):
            el.screenshot(path=str(out / f"c{i}.jpg"), type="jpeg", quality=92)
    else:
        out.parent.mkdir(parents=True, exist_ok=True)
        pg.screenshot(path=str(out), type="jpeg" if jpg or out.suffix==".jpg" else "png", **({"quality":92} if jpg or out.suffix==".jpg" else {}))
    b.close()
print("ok", out)
