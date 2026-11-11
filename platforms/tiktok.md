# TikTok（@eurogrid_jp）

共通ルールは CLAUDE.md。ここは TikTok だけのこと。

## 役割（2026-11-10、運営者の指示）
- ポルトガルGP（11/20〜22）で、Instagram 用のリールをそのまま出して数字を見る。TikTok 専用の作り込みはまだしない
- 比べ方（2026-11-12 運営者が決定。11/30 の週次振り返りで YouTube を始めるか決める材料）
  - 対象：ポルトガルGPの期間に、Instagram と TikTok の両方に出したリール全部。片方にしか出していないリールは外す
  - 数字：各リールの、投稿から48時間の時点の再生数・平均視聴時間・フォロー数（48時間の時点で読んで、claude/daily/ に残す）
  - 読み取り：48時間になる時刻はリールごとにちがうので、1本ずつ、その時刻に読んで claude/daily/ に残す（媒体・リール・投稿時刻・読んだ時刻・数字）。リールを出したら、その場で投稿の48時間後に読むリマインダー（send_later）を媒体ごとに入れる
  - まとめ方：媒体ごとに、再生数とフォロー数は全本の合計と1本平均を並べる
  - 平均視聴時間：合計は出さず、再生数で重みをつけた平均を出す（計算：総視聴時間 ÷ 総再生数。総視聴時間＝各リールの平均視聴時間×再生数の合計）

## 投稿のしかた（Claude用）
- API はつないでいない。L5320-note の拡張入り Chrome で、運営者がログインしておく（11/10 に eurogrid_jp でログイン済み）
- https://www.tiktok.com/tiktokstudio/upload から上げる。公開ボタンは運営者のOKのあと
- 動画は10MB未満で書き出す（45秒なら映像1.5Mbps前後）
- ファイルの入れ方は note と同じ（assets/ か posts/ に push → raw.githubusercontent.com から fetch → input に DataTransfer）
- カバーは Instagram のリールと同じ 1080×1920（templates/cover_1920.html。真ん中 1080×1350 の内側に大事な情報、下の3分の1と右下は空ける）
- キャプション：Instagram と同じ本文から。ハッシュタグ3〜5個（#MotoGP #モトGP #バイクレース ＋話題の1つ）。「PRではありません」

## フォロー（2026-11-10、運営者の指示「あなたが毎日やって」）
- TikTok では、Claude が公式アカウントをフォローする。1日2〜3件、合計8件前後で止める。相互フォロー狙いはしない。スポンサー企業はまだ
- X と Instagram のフォローは Claude はしない。Threads は試しの期間だけ（platforms/threads.md）
- 認証バッジがないものは、チームや MotoGP の公式サイトからのリンクで公式と確かめてから
- 済み：@motogp、@ducaticorse（11/10）。予定と結果は Project の 23_portugal_reel_tiktok.md

## Amazon
- 投稿に Amazon のリンクを貼らない（CLAUDE.md の8）
