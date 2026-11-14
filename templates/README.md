# 画像の型（2026-11-11 から新しいデザイン。決まりは CLAUDE.md の13）

| ファイル | サイズ | 使う場所 |
|---|---|---|
| brand.css | | 色・書体・キッカー・ロゴの土台。全部のテンプレートが読む |
| note_eyecatch.html | 1280×670（2倍で書き出し） | note のアイキャッチ |
| note_compare.html | 1280×960（2倍） | note の記事内の比較図 |
| ig_explainer.html | 1080×1350×5枚 | Instagram 解説型カルーセル（デザイン仕様 v1.1：表紙＝結論か対比の一文で色面は下半分以上、帯は全ページの上端、引用は独立した枠、2〜4枚目の末尾に差分の箱、数字帯は Anton。占有率70%以上を check_fill.py で測る） |
| ig_result.html | 1080×1350 | Instagram 結果型（1位だけ大きく、2〜10位は同じ行） |
| check_fill.py | | カルーセルの占有率（70%以上）・帯・表紙の色面を測る。`python3 templates/check_fill.py <html>` |
| reel_1920.html | 1080×1920、30fps、18秒 | リール・TikTok の動画の型（4場面＋字幕、写真・映像なし）。書き出しは `python3 templates/render_reel.py <html> <mp4>`（18秒で30秒ほど、音なし） |
| cover_1920.html | 1080×1920 | リール・TikTok のカバー（`?guide` で安全な範囲を表示） |
| x_image.html | 1600×900 | X・Threads の添付画像 |
| note_book_card.html | 1280×670（2倍） | note「この回の一冊」（旧デザインの色のまま） |
| old/ | | 旧デザイン（濃紺 #0B1220・黄 #F5B700）。note_header_v1.html、carousel_v1.py |

書き出し：
```
python3 templates/render.py templates/note_eyecatch.html out/eyecatch.png
python3 templates/render.py templates/ig_explainer.html posts/<フォルダ>     # c1.jpg〜c5.jpg
python3 templates/render.py templates/x_image.html out/x.jpg
```

- 書体の Dela Gothic One と Anton は、いまの作業環境に入っていない。入るまでは Noto Sans JP Black と Inter Display で代わりに表示される。フォントのファイル（どちらも OFL）を templates/fonts/ に置けば、brand.css に @font-face を足して使える
- 運営者が Canva で作るときも、色・左右・キッカー・サイズはこの表と CLAUDE.md の13に合わせる

## 育て方（2026-11-14 ユーロのデザイン仕様 v1）
- 同じ指摘が2回出たら、その投稿だけでなくテンプレート（この folder の html か brand.css）を直す。1回だけの指摘はその投稿の中で直す
- 色・書体・ロゴの色（brand.css）は、運営者が決めるまで変えない
