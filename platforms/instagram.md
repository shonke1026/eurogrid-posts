# Instagram（@eurogrid_jp）

共通ルールは CLAUDE.md。ここは Instagram だけのこと。

## 役割
- 図解と保管の場所。Threads・X で当たったネタだけをカルーセルにする。全部の転載先にしない
- 当面の目標：投稿を10件まで増やす
- レース週末はストーリーズで二択アンケート（スペイン紙 vs イタリア紙）
- 当たった対比ネタは45秒前後のリールにする（ルシア＝スペイン視点、マッテオ＝イタリア視点）。作り方は Project の 11_video_sound.md

## カルーセル
- 1080×1350（縦4:5）、JPEG。濃紺 #0B1220・オフホワイト #F2EEE6・黄色 #F5B700。英字 Inter、日本語 Noto Sans CJK JP。グリッド枠と文字だけ（写真・ロゴなし）
- 構成：1枚目＝ひと言で引きつける見出し／2〜3枚目＝中身（スペイン側・イタリア側など）／最後＝Eurogridの見方、数字や事実、出典（媒体名）
- 結果にふれる24時間以内の投稿は、1枚目とキャプションの冒頭に結果を書かない
- 右上に「n/全体」、下に @eurogrid_jp

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
