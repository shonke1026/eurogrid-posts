"""Machine checks for the auditor (CLAUDE.md / .claude/agents/auditor.md).

Usage:
  python3 scripts/check_post.py x "本文"                X の数え方での長さ（280以内か）
  python3 scripts/check_post.py x-source "返信"         X の出典の返信：URL・@・ドメインに見える名前がないか
  python3 scripts/check_post.py threads "本文"          Threads：「#」なし、500字以内
  python3 scripts/check_post.py instagram "本文"        Instagram：Amazonリンクなし、ハッシュタグ3〜5個
  python3 scripts/check_post.py tiktok "本文"           TikTok：Amazonリンクなし
  python3 scripts/check_post.py note-title "タイトル"   note：国旗の絵文字なし
  python3 scripts/check_post.py note-body <body.html>  note：tag=eurogridnote-22、PR表記、アソシエイト表示
  python3 scripts/check_post.py folder posts/<フォルダ>  post.json と x.json（あれば）をまとめて確かめる

Exit code: 0 = OK, 1 = NG がある, 2 = 使い方のまちがい（種類・引数・ファイル）。
Text checks only; the auditor still reads everything.
"""
import json
import pathlib
import re
import sys

TLD = r"(?:com|net|org|it|es|jp|fr|de|uk|tv|be|io|co|me|info|eu|pt|at|ch|ly|gl|to|news)"
URL = re.compile(r"https?://\S+|(?<![A-Za-z0-9-])[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\." + TLD + r"(?![A-Za-z0-9])(?:/[^\s　、。）)]*)?", re.I)
FLAG = re.compile(r"[\U0001F1E6-\U0001F1FF]{2}")
AMAZON = re.compile(r"amazon\.co\.jp|amzn\.(?:to|asia)|amazon\.com", re.I)
AT = re.compile(r"[@＠]\w")
PR_HEAD = "※この記事にはアフィリエイトリンク（PR）が含まれます。"
ASSOC = "Amazonのアソシエイトとして、Eurogridは適格販売により収入を得ています。"
X_JSON_KEYS = {"text", "reply"}  # 出す前の正本はこの2つだけ
X_JSON_AFTER = {"status_ids", "posted_at"}  # 出したあとに足す
TEXT_KINDS = ("x", "x-source", "threads", "instagram", "tiktok", "note-title")
KINDS = TEXT_KINDS + ("note-body", "folder")


class UsageError(Exception):
    pass


def x_weight(text):
    """twitter-text v3 style: URLs count 23, chars in light ranges 1, others 2."""
    total = 0
    pos = 0
    for m in URL.finditer(text):
        total += _w(text[pos:m.start()]) + 23
        pos = m.end()
    return total + _w(text[pos:])


def _w(s):
    n = 0
    for ch in s:
        c = ord(ch)
        if 0xFE00 <= c <= 0xFE0F or c == 0x200D:  # variation selectors, ZWJ
            continue
        if c <= 0x10FF or 0x2000 <= c <= 0x200D or 0x2010 <= c <= 0x201F or 0x2032 <= c <= 0x2037:
            n += 1
        else:
            n += 2
    return n


def check(kind, text, label=None):
    """Return a list of NG messages. Prints passing measurements (X length)."""
    if kind not in TEXT_KINDS + ("note-body",):
        raise UsageError(f"知らない種類：{kind}")
    if not isinstance(text, str) or not text.strip():
        raise UsageError(f"{label or kind}：本文が空")
    where = f"{label}: " if label else ""
    errs = []
    if kind in ("x", "x-source"):
        w = x_weight(text)
        if w > 280:
            errs.append(f"{where}X: {w}/280（超えている）")
        else:
            print(f"{where}X: {w}/280")
    if kind == "x-source":
        if URL.search(text):
            errs.append(f"{where}X の出典: URL かドメインに見える名前がある（{URL.search(text).group(0)}）。媒体名だけにする")
        if AT.search(text):
            errs.append(f"{where}X の出典: 「@」がある（本人に通知が飛ぶ）")
    if kind in ("x", "x-source", "threads", "instagram", "tiktok") and AMAZON.search(text):
        errs.append(f"{where}{kind}: Amazonのリンクがある（投稿には貼らない）")
    if kind == "threads":
        if "#" in text or "＃" in text:
            errs.append(f"{where}Threads: 「#」がある")
        if len(text) > 500:
            errs.append(f"{where}Threads: {len(text)}/500字")
    if kind == "instagram":
        tags = re.findall(r"[#＃][^\s#＃]+", text)
        if not 3 <= len(tags) <= 5:
            errs.append(f"{where}Instagram: ハッシュタグが{len(tags)}個（3〜5個）")
    if kind == "note-title":
        if FLAG.search(text):
            errs.append(f"{where}note: タイトル・見出しに国旗の絵文字がある")
    if kind == "note-body":
        links = re.findall(r"amazon\.co\.jp/dp/\w+[^\s\"<]*", text)
        for l in links:
            if "tag=eurogridnote-22" not in l:
                errs.append(f"note: tag が eurogridnote-22 でないリンク {l}")
        if links:
            if PR_HEAD not in text:
                errs.append("note: 冒頭のPR表記がない")
            if ASSOC not in text:
                errs.append("note: アソシエイトの表示がない")
        for h in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", text, re.S):
            if FLAG.search(h):
                errs.append(f"note: 見出しに国旗の絵文字 {h}")
    return errs


def _load_json(p):
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise UsageError(f"{p} が UTF-8 の JSON として読めない（{e}）")
    if not isinstance(data, dict):
        raise UsageError(f"{p} の中身が {{...}} の形でない")
    return data


def _replies(post, errs, name):
    out = []
    if post.get("reply"):
        out.append(("reply", post["reply"]))
    replies = post.get("replies") or []
    if not isinstance(replies, list):
        errs.append(f"{name}: replies がリストでない")
        return out
    for i, r in enumerate(replies, 1):
        if not isinstance(r, str) or not r.strip():
            errs.append(f"{name}: replies[{i}] が空か文字でない")
        else:
            out.append((f"replies[{i}]", r))
    return out


def _text(kind, value, label):
    if not isinstance(value, str) or not value.strip():
        return [f"{label}: 空か文字でない"]
    return check(kind, value, label)


def check_folder(folder):
    d = pathlib.Path(folder)
    if not d.is_dir():
        raise UsageError(f"フォルダがない：{folder}")
    p = d / "post.json"
    xp = d / "x.json"
    if not p.exists() and not xp.exists():
        raise UsageError(f"{folder} に post.json も x.json もない")
    errs = []
    checked = []
    if p.exists():
        post = _load_json(p)
        if post.get("platform") == "threads":
            errs += _text("threads", post.get("text"), "post.json text")
            checked.append("post.json text")
            for label, r in _replies(post, errs, "post.json"):
                errs += check("threads", r, f"post.json {label}")
                checked.append(f"post.json {label}")
            if post.get("topic_tag") and not post.get("reply_to_id") and post["topic_tag"] != "MotoGP":
                errs.append("Threads: topic_tag が MotoGP でない")
        elif "caption" in post:
            errs += _text("instagram", post["caption"], "post.json caption")
            checked.append("post.json caption")
        elif not post.get("story"):
            errs.append("post.json: platform が threads でも caption・story でもない（種類が分からない）")
        m = re.search(r"T\d\d:(\d\d)", str(post.get("publish_at") or ""))
        if m and m.group(1) in ("00", "15", "30", "45"):
            errs.append(f"予約がちょうどの分（:{m.group(1)}）")
    if xp.exists():
        x = _load_json(xp)
        extra = set(x) - X_JSON_KEYS - X_JSON_AFTER
        if extra:
            errs.append(f"x.json: 決まりにない項目 {sorted(extra)}（text・reply、出したあとは status_ids・posted_at だけ）")
        errs += _text("x", x.get("text"), "x.json text")
        checked.append("x.json text")
        if not x.get("reply"):
            errs.append("x.json: reply（出典の返信）がない")
        for label, r in _replies(x, errs, "x.json"):
            errs += check("x-source", r, f"x.json {label}")
            checked.append(f"x.json {label}")
        if bool(x.get("status_ids")) != bool(x.get("posted_at")):
            errs.append("x.json: status_ids と posted_at は両方そろえて書く")
    print("見たもの:", "、".join(checked) if checked else "なし")
    return errs


def main(argv):
    if len(argv) != 3 or argv[1] in ("-h", "--help"):
        raise UsageError("引数は2つ（種類と本文／ファイル／フォルダ）")
    kind, arg = argv[1], argv[2]
    if kind not in KINDS:
        raise UsageError(f"知らない種類：{kind}（{'・'.join(KINDS)} のどれか）")
    if kind == "folder":
        return check_folder(arg)
    if kind == "note-body":
        p = pathlib.Path(arg)
        if not p.is_file():
            raise UsageError(f"ファイルがない：{arg}")
        return check(kind, p.read_text())
    return check(kind, arg)


def run(argv):
    try:
        errs = main(argv)
    except UsageError as e:
        print("使い方のまちがい:", e, file=sys.stderr)
        print(__doc__, file=sys.stderr)
        return 2
    except Exception as e:  # check_post.py 自体の不具合。NG（1）と区別する
        print(f"check_post.py の不具合: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    for e in errs:
        print("NG", e)
    if not errs:
        print("OK")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(run(sys.argv))
