"""リールを書き出す（templates/reel_1920.html の型）。
python3 templates/render_reel.py <reel.html> <出力.mp4>
- html と同じフォルダに brand.css と fonts/ が無ければ、templates/ からコピーする
- 1フレームずつ画面を作って JPEG にし、ffmpeg で H.264（30fps、veryfast、CRF 20）にまとめる。18秒で30秒ほど
- 音は入れない。書き出したら、場面ごとに数枚を目で見て確かめる（文字の重なり、安全な範囲）
"""
import pathlib, shutil, subprocess, sys, tempfile
from playwright.sync_api import sync_playwright

def main(src, out):
    src = pathlib.Path(src).resolve(); out = pathlib.Path(out).resolve()
    tpl = pathlib.Path(__file__).resolve().parent
    if not (src.parent / "brand.css").exists():
        shutil.copy(tpl / "brand.css", src.parent / "brand.css")
    if not (src.parent / "fonts").exists():
        shutil.copytree(tpl / "fonts", src.parent / "fonts")
    with tempfile.TemporaryDirectory() as d:
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
            pg.goto(src.as_uri()); pg.wait_for_timeout(800)
            dur = pg.evaluate("DUR")
            for f in range(dur):
                pg.evaluate("f=>setFrame(f)", f)
                pg.screenshot(path=f"{d}/{f:04d}.jpg", type="jpeg", quality=92)
            b.close()
        tmp = out.with_name(out.stem + ".tmp.mp4")
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-framerate", "30", "-i", f"{d}/%04d.jpg",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(tmp)], check=True)
        tmp.rename(out)
    print("ok", out, f"{dur} frames")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(2)
    main(sys.argv[1], sys.argv[2])
