# Instagram（@eurogrid_jp）

共通ルールは CLAUDE.md。ここは Instagram だけのこと。

## 役割
- 図解と保管の場所。Threads・X で当たったネタだけをカルーセルにする。全部の転載先にしない
- 当面の目標：投稿を10件まで増やす
- レース週末はストーリーズで二択アンケート（スペイン紙 vs イタリア紙）
- 当たった対比ネタは45秒前後のリールにする（ルシア＝スペイン視点、マッテオ＝イタリア視点）。作り方は Project の 11_video_sound.md
- リールのカバーは 1080×1920：templates/cover_1920.html。大事な情報は真ん中の 1080×1350 の内側に入れ、下の3分の1と右下は空ける（`?guide` を付けて開くと範囲が見える）。CapCut を使うなら無料の範囲（自動字幕とカバー）

## カルーセル（1080×1350、JPEG。色・書体・キッカーは CLAUDE.md の13）
- 解説型（5枚）：templates/ig_explainer.html
  - 1枚目＝表紙に結論／2枚目＝スペイン／3枚目＝イタリア／4枚目＝ちがい／5枚目＝まとめ（Eurogridの見方、出典）と note への案内
- 結果型：templates/ig_result.html。1位だけ大きく、2〜10位は同じ高さの行。日本人選手の行には「日本」の印
- 結果にふれる24時間以内の投稿は、1枚目とキャプションの冒頭に結果を書かない（結果型は2枚目から）
- 右上に「n/全体」、下に @eurogrid_jp
- 書き出し：`python3 templates/render.py templates/ig_explainer.html posts/<フォルダ>`（c1.jpg〜c5.jpg ができる）
- 11/11 12:37 の小椋藍のカルーセルは旧デザイン（templates/old/carousel_v1.py）で作った最後の回

## キャプション
- 2〜4行の短文＋最後に Eurogrid の見方1〜2文
- 出典は媒体名を書く（キャプションの URL はリンクにならない）
- アフィリエイトなしの投稿は「PRではありません」
- ハッシュタグは基本セット4つ＋話題1つの計5個：`#MotoGP #モトGP #バイクレース #Eurogrid ＋ライダー名など`（2026-11-10 の案。表記ゆれを出さない）
- 「#01」のような番号はタグになるので「第1回」と書く
- 投稿時に「Threadsにもシェア」が出たらオフ

## 投稿のしかた（Claude用）
- posts/<日付-ig-名前>/ に画像と post.json、OKのあと main に push
  - カルーセル：`{"publish_at":"…+09:00","approved":true,"caption":"…","images":["c1.jpg","c2.jpg",…]}`（JPEGのみ）
  - リール：`"video":"reel.mp4"`（表紙は `"cover":"cover.jpg"`）。フィードにも出る
  - ストーリーズ：`{"story":true,"publish_at":…,"approved":true,"images":[…]}`（1080×1920、scripts/story_cards.py）
- 出し方・遅れたときの手動実行は platforms/threads.md と同じ（publish.yml）
- プロフィールのリンクの編集はスマホのアプリからだけ（運営者）。いまは note が1本目

## Amazon
- 投稿・ストーリーズに Amazon のリンクを貼らない（CLAUDE.md の8）
