"""Tests for check_post.py.  Run: python3 -m unittest scripts/test_check_post.py"""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).with_name("check_post.py")


def run(*args):
    r = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


class Usage(unittest.TestCase):
    def test_no_args(self):
        self.assertEqual(run()[0], 2)

    def test_one_arg(self):
        self.assertEqual(run("x")[0], 2)

    def test_too_many_args(self):
        self.assertEqual(run("x", "a", "b")[0], 2)

    def test_unknown_kind(self):
        code, out = run("tiktokk", "本文")
        self.assertEqual(code, 2)
        self.assertIn("知らない種類", out)

    def test_empty_text(self):
        self.assertEqual(run("threads", "  ")[0], 2)

    def test_missing_note_body_file(self):
        self.assertEqual(run("note-body", "/nonexistent/body.html")[0], 2)

    def test_missing_folder(self):
        self.assertEqual(run("folder", "/nonexistent/folder")[0], 2)

    def test_empty_folder(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(run("folder", d)[0], 2)

    def test_json_list(self):
        with tempfile.TemporaryDirectory() as d:
            pathlib.Path(d, "post.json").write_text("[]")
            self.assertEqual(run("folder", d)[0], 2)

    def test_not_utf8(self):
        with tempfile.TemporaryDirectory() as d:
            pathlib.Path(d, "post.json").write_bytes(b"\xff\xfe{")
            self.assertEqual(run("folder", d)[0], 2)

    def test_broken_json(self):
        with tempfile.TemporaryDirectory() as d:
            pathlib.Path(d, "post.json").write_text("{")
            self.assertEqual(run("folder", d)[0], 2)


class Text(unittest.TestCase):
    def test_x_ok(self):
        self.assertEqual(run("x", "小椋藍選手" * 10)[0], 0)

    def test_x_too_long(self):
        self.assertEqual(run("x", "あ" * 141)[0], 1)

    def test_x_source_names_only_ok(self):
        self.assertEqual(run("x-source", "出典：Motorsport スペイン版（11/12）。URLはThreadsの同じ投稿の返信に")[0], 0)

    def test_x_source_url(self):
        self.assertEqual(run("x-source", "出典：https://example.com/a")[0], 1)

    def test_x_source_domain(self):
        self.assertEqual(run("x-source", "出典：Crash.net")[0], 1)

    def test_x_source_domain_followed_by_japanese(self):
        self.assertEqual(run("x-source", "出典：Motorsport.com日本版")[0], 1)
        self.assertEqual(run("x-source", "出典：Crash.netの記事")[0], 1)

    def test_x_source_domain_upper_and_other_tld(self):
        for t in ("出典：CRASH.NET", "出典：youtu.be/abc", "出典：autosport.co.uk", "出典：motorsport.tv"):
            self.assertEqual(run("x-source", t)[0], 1, t)

    def test_x_weight_domain_counts_23(self):
        # 「Motorsport.com」はリンク扱いで23。全角136字＋リンクで 272+23 > 280
        self.assertEqual(run("x", "あ" * 136 + "Motorsport.com日本版")[0], 1)

    def test_tiktok_amazon(self):
        self.assertEqual(run("tiktok", "https://amzn.to/abc")[0], 1)
        self.assertEqual(run("tiktok", "本文")[0], 0)

    def test_instagram_fullwidth_tags(self):
        self.assertEqual(run("instagram", "本文 ＃a ＃b ＃c")[0], 0)

    def test_x_source_at(self):
        self.assertEqual(run("x-source", "出典：@motogp")[0], 1)

    def test_threads_hash(self):
        self.assertEqual(run("threads", "本文 #MotoGP")[0], 1)

    def test_threads_long(self):
        self.assertEqual(run("threads", "あ" * 501)[0], 1)

    def test_amazon_in_post(self):
        self.assertEqual(run("threads", "https://www.amazon.co.jp/dp/4087211649")[0], 1)

    def test_instagram_tags(self):
        self.assertEqual(run("instagram", "本文 #a #b #c")[0], 0)
        self.assertEqual(run("instagram", "本文 #a")[0], 1)

    def test_note_title_flag(self):
        self.assertEqual(run("note-title", "🇪🇸🇮🇹 論調比較")[0], 1)
        self.assertEqual(run("note-title", "スペイン×イタリア 論調比較")[0], 0)

    def test_note_body(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d, "b.html")
            p.write_text('<p>https://www.amazon.co.jp/dp/4087211649?tag=eurogridjp-22</p>')
            self.assertEqual(run("note-body", str(p))[0], 1)
            p.write_text('※この記事にはアフィリエイトリンク（PR）が含まれます。'
                         '<p>https://www.amazon.co.jp/dp/4087211649?tag=eurogridnote-22</p>'
                         'Amazonのアソシエイトとして、Eurogridは適格販売により収入を得ています。')
            self.assertEqual(run("note-body", str(p))[0], 0)


def folder(post=None, x=None):
    d = tempfile.TemporaryDirectory()
    if post is not None:
        pathlib.Path(d.name, "post.json").write_text(json.dumps(post, ensure_ascii=False))
    if x is not None:
        pathlib.Path(d.name, "x.json").write_text(json.dumps(x, ensure_ascii=False))
    return d


TH = {"platform": "threads", "publish_at": "2026-11-13T12:08:00+09:00", "text": "本文",
      "topic_tag": "MotoGP", "reply": "出典\nMotosan https://www.motosan.es/a"}
XJ = {"text": "本文", "reply": "出典：Motosan（11/9）。URLはThreadsの同じ投稿の返信に"}


class Folder(unittest.TestCase):
    def check(self, post=None, x=None):
        d = folder(post, x)
        try:
            return run("folder", d.name)
        finally:
            d.cleanup()

    def test_ok(self):
        code, out = self.check(TH, XJ)
        self.assertEqual(code, 0, out)
        self.assertIn("x.json reply", out)

    def test_x_json_only(self):
        self.assertEqual(self.check(x=XJ)[0], 0)

    def test_replies_chain_checked(self):
        post = dict(TH, replies=["ひとつ目", "#だめ"])
        code, out = self.check(post)
        self.assertEqual(code, 1)
        self.assertIn("replies[2]", out)

    def test_round_minute(self):
        self.assertEqual(self.check(dict(TH, publish_at="2026-11-13T12:15:00+09:00"))[0], 1)

    def test_topic_tag(self):
        self.assertEqual(self.check(dict(TH, topic_tag="F1"))[0], 1)

    def test_x_json_url_in_reply(self):
        self.assertEqual(self.check(x=dict(XJ, reply="出典 https://www.motosan.es/a"))[0], 1)

    def test_x_json_extra_key(self):
        self.assertEqual(self.check(x=dict(XJ, image="a.png"))[0], 1)

    def test_x_json_after_posting(self):
        ok = dict(XJ, status_ids=["1", "2"], posted_at="2026-11-13T12:20:00+09:00")
        self.assertEqual(self.check(x=ok)[0], 0)
        self.assertEqual(self.check(x=dict(XJ, status_ids=["1"]))[0], 1)

    def test_x_json_without_reply(self):
        self.assertEqual(self.check(x={"text": "本文"})[0], 1)

    def test_publish_at_null(self):
        self.assertEqual(self.check(dict(TH, publish_at=None))[0], 0)

    def test_empty_reply_in_chain_is_ng(self):
        self.assertEqual(self.check(dict(TH, replies=[""]))[0], 1)

    def test_topic_tag_missing_ok(self):
        post = dict(TH); post.pop("topic_tag")
        self.assertEqual(self.check(post)[0], 0)

    def test_story(self):
        self.assertEqual(self.check({"publish_at": "2026-11-13T19:22:00+09:00", "story": True})[0], 0)

    def test_x_json_too_long(self):
        self.assertEqual(self.check(x=dict(XJ, text="あ" * 141))[0], 1)

    def test_instagram(self):
        ig = {"publish_at": "2026-11-13T19:22:00+09:00", "caption": "本文 #a #b #c"}
        self.assertEqual(self.check(ig)[0], 0)

    def test_unknown_post_kind(self):
        self.assertEqual(self.check({"publish_at": "2026-11-13T19:22:00+09:00"})[0], 1)


class RealPosts(unittest.TestCase):
    """11/12 以降（X の出典は媒体名だけ）に出した投稿が通ること。"""

    def test_published_after_rule(self):
        root = SCRIPT.parent.parent / "posts"
        for name in ("2026-11-13-th-marquez", "2026-11-13-th-dovizioso", "2026-11-13-ig-ogura"):
            if (root / name).exists():
                code, out = run("folder", str(root / name))
                self.assertEqual(code, 0, f"{name}\n{out}")


if __name__ == "__main__":
    unittest.main()
