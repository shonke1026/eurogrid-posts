"""Machine checks for the auditor (CLAUDE.md / .claude/agents/auditor.md).

Usage:
  python3 scripts/check_post.py x "本文"            X の数え方での長さ（280以内か）
  python3 scripts/check_post.py threads "本文"      Threads：「#」なし、500字以内
  python3 scripts/check_post.py instagram "本文"    Instagram：Amazonリンクなし、ハッシュタグ数
  python3 scripts/check_post.py note-title "タイトル"   note：国旗の絵文字なし
  python3 scripts/check_post.py note-body <body.html>  note：tag=eurogridnote-22、PR表記、アソシエイト表示
  python3 scripts/check_post.py folder posts/<フォルダ>  post.json をまとめて確かめる
Exit code 1 when a check fails. Text checks only; the auditor still reads everything.
"""
import json
import pathlib
import re
import sys

URL = re.compile(r"https?://\S+|\b[\w-]+\.(?:com|net|it|es|jp|org)\b(?:/\S*)?")
FLAG = re.compile(r"[\U0001F1E6-\U0001F1FF]{2}")
AMAZON = re.compile(r"amazon\.co\.jp|amzn\.(?:to|asia)|amazon\.com", re.I)
BANNED_NAME = re.compile(r"MotoGP", re.I)
PR_HEAD = "※この記事にはアフィリエイトリンク（PR）が含まれます。"
ASSOC = "Amazonのアソシエイトとして、Eurogridは適格販売により収入を得ています。"


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


def check(kind, text):
    errs = []
    if kind == "x":
        w = x_weight(text)
        if w > 280:
            errs.append(f"X: {w}/280（超えている）")
        else:
            print(f"X: {w}/280")
    if kind in ("x", "threads", "instagram", "tiktok") and AMAZON.search(text):
        errs.append(f"{kind}: Amazonのリンクがある（投稿には貼らない）")
    if kind == "threads":
        if "#" in text or "＃" in text:
            errs.append("Threads: 本文や返信に「#」がある")
        if len(text) > 500:
            errs.append(f"Threads: {len(text)}/500字")
    if kind == "instagram":
        tags = re.findall(r"#\S+", text)
        if not 3 <= len(tags) <= 5:
            errs.append(f"Instagram: ハッシュタグが{len(tags)}個（3〜5個）")
    if kind == "note-title":
        if FLAG.search(text):
            errs.append("note: タイトル・見出しに国旗の絵文字がある")
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


def check_folder(folder):
    p = pathlib.Path(folder) / "post.json"
    post = json.loads(p.read_text())
    errs = []
    if post.get("platform") == "threads":
        for k in ("text", "reply"):
            if post.get(k):
                errs += check("threads", post[k])
        if post.get("topic_tag") and not post.get("reply_to_id") and post["topic_tag"] != "MotoGP":
            errs.append("Threads: topic_tag が MotoGP でない")
    elif "caption" in post:
        errs += check("instagram", post["caption"])
    m = re.search(r"T\d\d:(\d\d)", post.get("publish_at", ""))
    if m and m.group(1) in ("00", "15", "30", "45"):
        errs.append(f"予約がちょうどの分（:{m.group(1)}）")
    return errs


def main():
    kind, arg = sys.argv[1], sys.argv[2]
    if kind == "folder":
        errs = check_folder(arg)
    elif kind == "note-body":
        errs = check(kind, pathlib.Path(arg).read_text())
    else:
        errs = check(kind, arg)
    for e in errs:
        print("NG", e)
    if not errs:
        print("OK")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
