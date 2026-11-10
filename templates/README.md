# 画像の型

- note_header.html：note の見出し画像（1280×670、deviceScaleFactor 2 で撮る）。差し替えるのは h1・.sub・.race の3か所
- note_book_card.html：note の「この回の一冊」カード（1280×670、2倍）。書名・著者・3点・値段と日付を差し替える。実物の表紙は使わない
- carousel.py：Instagram カルーセル（1080×1350、SVG → rsvg-convert → JPEG）。`python3 templates/carousel.py posts/<フォルダ>`。中身はスクリプトの中の文を書き換える

撮り方（Playwright）：
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1280,'height':670},device_scale_factor=2)
    pg.goto('file:///…/templates/note_header.html');pg.wait_for_timeout(500)
    pg.screenshot(path='out.png');b.close()
```
