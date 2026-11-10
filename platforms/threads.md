# Threads（@eurogrid_jp）

共通ルールは CLAUDE.md。ここは Threads だけのこと。

## 役割
- 拡散の本命。新しい人への入口（日本人ライダー、けが・復帰の続報が強い）
- 速報は X と同じ素材から作る。X で削った補足を1文足してよい

## 文字数と形
- 本文 500 字以内、返信も500字以内
- 本文に「#」を書かない（トピックタグになり、後ろの文がタグ扱いで崩れる）。「#97」は「97番」と書く
- トピックは本文でなく topic_tag に「MotoGP」
- 出典は本文に入れず返信に（「出典\n媒体名 URL」）。結果にふれる24時間以内の投稿は、返信1つに「⚠️ネタバレ：〜」＋中身＋出典
- Eurogridの視点は1〜2文
- URL の末尾が「.html」だとリンクが途中で切れることがある。押して開けるか確かめる

## 固定投稿とプロフィール
- 固定：自己紹介＋論調比較の代表作のリンク＋note（11/11 8:52 に出したもの）。固定はアプリで運営者が手動（API ではできない）
- プロフィールのリンク：「X（速報）」と「note（深掘り）」
- 当たった投稿の返信の最後に、自己紹介＋note の案内を1回だけ入れる（同じ投稿に何度も入れない）

## 投稿のしかた（Claude用）
- posts/<日付-名前>/post.json を作り、OKのあと main に push
  - 通常：`{"platform":"threads","publish_at":"…+09:00","approved":true,"text":"本文","topic_tag":"MotoGP","reply":"出典\n媒体名 URL"}`
  - 画像：`"images":["1.jpg",…]` を足す。動画：`"video":"reel.mp4"`
  - 既存の投稿の下に返信だけ：`"reply_to_id":"<media id>"` と `"text"`（topic_tag は付かない）
- GitHub Actions が15分ごとに出す。遅れることがあるので、予約から20分たっても published.json がなければ手動で実行：
  `gh api -X POST repos/shonke1026/eurogrid-posts/actions/workflows/publish.yml/dispatches -f ref=main -f 'inputs[dry_run]=0'`
- dispatch する前に publish_at が過ぎているか確かめる（未来だと出ない）
- 返信先の media id は posts/<フォルダ>/published.json にある。投稿の URL（threads.com/@eurogrid_jp/post/…）はプロフィールのページから取る

## Amazon
- 投稿に Amazon のリンクを貼らない（CLAUDE.md の8）
