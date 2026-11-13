# Facebook ページ（Eurogrid｜スペイン×イタリア論調比較）

共通ルールは CLAUDE.md。ここは Facebook だけのこと。2026-11-12 運営者が作成（運営者の決定：Instagram の投稿を流す形で始め、専用の投稿は作らない）。

- URL：https://www.facebook.com/eurogridjp （ユーザーネームにアンダーバーが使えないので eurogridjp）
- アイコン：templates/icon.html、カバー：templates/fb_cover.html（1640×624。スマホでは左右が切れるので中身は真ん中に）
- Instagram の @eurogrid_jp とリンク済み（2026-11-12）
- リンク：note（https://note.com/eurogrid_jp 、表示は「note」）を 2026-11-12 に追加。出口はほかの媒体と同じく note にそろえる（運営者）
- 自己紹介・表示名は今のまま（2026-11-12 運営者）
- 未確認：アカウントセンターでの連携と、Instagram のリールを Facebook に同時に出す設定。個人のアカウントへの切り替えが要るので運営者が確かめる（2026-11-12）
- 位置づけ（名前の確保だけか、リール転載のテストか）は運営者がこれから決める。決まったらこのファイルとグランドデザインを直す
- 確かめたこと（2026-11-12）：自動投稿（scripts/publish.py の API）で出した Instagram の投稿は、Facebook のページには流れなかった（19:09 公開のロッシ選手のカルーセル。20:2x にページを見て、投稿はカバー写真とプロフィール写真の変更だけだった）
- 2026-11-12 は運営者の指示で、同じ画像5枚とキャプションを Claude が Facebook のページに手で出した（20:30。出す前に最終版をメール）
- **Instagram の投稿は、毎回 Facebook のページにも手で出す（2026-11-13 決定。三者協議 grand-design-rebuild の Q3。11/30 に一次判断、12/30 に本決定）**
  - Instagram が出たのを確かめたら（published.json）、そのまま続けて出す。運営者に毎回聞かない
  - 画像とキャプションは Instagram と同じ（posts/<フォルダ>/ のもの）。最終版のメールは Instagram の分と1通にまとめてよい
  - 出したら、その投稿の post.json に `"facebook": {"posted_at": "出た時刻", "minutes": 分数}` を足して push する。分数は Facebook のページを開いてから、ページで投稿を確かめるまで
  - 出せなかったときは、post.json に `"facebook": {"error": "理由"}` を書き、運営者に知らせる
- 手で出すやり方：ページの「写真・動画」→ ページの中で raw.githubusercontent.com の画像を img で読み込んで canvas から File を作り、HTMLInputElement.prototype.click を差し替えて捕まえた input に DataTransfer で入れる（fetch は CSP で止まる。img は通る）。本文は入力欄に paste イベント（text/plain）で入れる →「次へ」→「投稿」→「後で」（「今すぐ電話」ボタンの案内）→「後で」（リール動画の案内）
- 調査：日本のファンのグループ「MotoGP ファン」（https://www.facebook.com/groups/393458810818731 、公開、約1.2万人）に、Eurogrid のページとして参加済み（2026-11-12）。Eurogrid 用の Chrome でフィードが読めることを確かめた。researcher.md の手順で毎朝読む。画面に「Eurogrid…としてコメント」の欄が出るが、いいね・コメント・投稿は Claude がしない（グループに書くかは運営者が決める）
- パスワードの再入力・ログインは運営者がする
