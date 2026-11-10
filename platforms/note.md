# note（https://note.com/eurogrid_jp）

共通ルールは CLAUDE.md。ここは note だけのこと。

## 役割
- 論調比較の本編を残す場所。レース週末ごとに1本。SNS はここへ流す入口
- 締切：レース後の月曜 10:00（ポルトガル 11/23、バレンシア 11/30）
- 表示名：Eurogrid｜スペイン×イタリア論調比較

## 記事の形
- タイトル：〈本文の一言〉【スペイン×イタリア 論調比較・○○GP】（国旗の絵文字は使わない）
- 見出し：「スペイン側：〜」「イタリア側：〜」「Eurogridの見方」「📚 この回の一冊」「出典」「Eurogridの各SNS」（見出しにも国旗なし）
- 冒頭：アフィリエイトがある回は「※この記事にはアフィリエイトリンク（PR）が含まれます。」、続けて各SNSへの案内1文
- 末尾：X・Threads・Instagram のリンク、「非公式の個人アカウントです。」、アフィリエイトがある回はアソシエイトの表示（CLAUDE.md の8）
- 海外記事の全文翻訳はしない

## 見出し画像（アイキャッチ）と記事内の図
- アイキャッチを毎回つける。1280×670 を2倍で書き出す：templates/note_eyecatch.html。キッカーは「比較」（論調比較の回）か「解説」
- 差し替えるのはキッカー・タイトル・サブタイトル・GP名
- 記事の中で両国を並べるところには比較図 1280×960（2倍）：templates/note_compare.html。左＝スペイン、右＝イタリア、下に「ちがい」の1行
- 画像を作る道具：Claude はテンプレートから。運営者は Canva（note と Canva の連携は 2025-12-01 に終わったので、書き出した画像を記事に入れる）
- 第1回（カタールGP）の見出し画像は旧デザイン（templates/old/note_header_v1.html）。作り直すかは運営者が決める

## この回の一冊
- 本は Project の 19_bookshelf.md から1冊。中身（章立て・人）は出版社のページなどで確かめてから書く
- 前後に区切り線
- 見出しのすぐ下に本の画像カード（1280×670、2倍。templates/note_book_card.html。旧デザインの色のまま。新しい色に合わせるのは次の回から）。実物の表紙は使わず、書名だけの本の絵。画像にタグ付きリンクを付ける（画像を選ぶ→リンクのアイコン→URL→「適用」）
- その下に「引用」で太字の『書名』＋改行＋著者（出版社、年）
- 紹介2段落：①どんな本か（確かめた事実だけ）②この回とのつながり、今読む理由（大事なところを太字）
- リンクは太字で「▶ Amazonで見る（新書 ○○円／M月D日時点）」。URL をそのまま見せない
- リンクの形：`https://www.amazon.co.jp/dp/<ASIN>?tag=eurogridnote-22`

## 編集のしかた（Claude用）
- 運営者が L5320-note の拡張入り Chrome で note にログインしておく（Claude は認証しない）
- 編集画面：https://editor.note.com/notes/<記事ID>/edit/ 。公開・更新は「公開に進む」→「投稿する」／「更新する」。公開は運営者のOKのあと
- 本文をまとめて入れる：ProseMirror の中身を全部選んで、HTML を paste イベント（DataTransfer の text/html）で流す。h2・hr・blockquote・strong・a はそのまま入る。本文に画像が入ったあとはこの方法を使わない（画像が消えるおそれ）。直したい文だけ JS で選んで Delete
- 画像を入れる：JS でカーソルを置いて Enter で空の行→左の「＋」→「画像」。ファイルは、画像を assets/ に push し、ページの中で raw.githubusercontent.com から fetch して File を作り、HTMLInputElement.prototype.click を差し替えて捕まえた input に DataTransfer で入れて change を送る（file_upload はこの環境で通らなかった）。終わったら click を元に戻す
- 更新したら https://note.com/api/v3/notes/<記事ID> の body で、tag・直した文・画像を確かめる
- プロフィール：https://note.com/settings/profile（ヘッダー画像は「この画像を使う」のあと数秒待ってから保存）

## 記事一覧
- 第1回 カタールGP（2026-11-10 公開）：https://note.com/eurogrid_jp/n/nbd86c7aa7de4
