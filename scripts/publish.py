"""Publish approved Eurogrid posts to Instagram (Instagram Graph API, system user token).

Each post lives in posts/<folder>/ with post.json:
  {"publish_at": "2026-11-11T20:00:00+09:00", "approved": true,
   "caption": "...", "images": ["1.jpg", "2.jpg"]}
For Threads add "platform": "threads" with "text" (and optional "topic_tag", "reply",
"images": ["1.jpg", ...] for an image or carousel post)
instead of caption/images.
For Instagram Stories add "story": true with "images" (1080x1920 JPEG, one frame each).
For a reel/video add "video": "reel.mp4" instead of "images" (Instagram REELS,
Threads VIDEO). Optional for Instagram: "cover": "cover.jpg".
`python3 scripts/publish.py --check <folder>` only creates the media containers and
waits until Meta has processed them (nothing is published; containers expire in 24h).
A post is published when approved is true, publish_at has passed and
published.json does not exist yet. published.json is written afterwards.
"""
import datetime as dt
import json
import os
import pathlib
import sys
import time
import urllib.parse
import urllib.request

API = "https://graph.facebook.com/v23.0"
IG_USER_ID = os.environ.get("IG_USER_ID", "17841466770737433")
REPO = os.environ.get("GITHUB_REPOSITORY", "shonke1026/eurogrid-posts")
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
TOKEN = os.environ.get("IG_ACCESS_TOKEN", "")
TH_TOKEN = os.environ.get("THREADS_ACCESS_TOKEN", "")
TH_API = "https://graph.threads.net/v1.0"
DRY = os.environ.get("DRY_RUN") == "1"
ROOT = pathlib.Path(__file__).resolve().parent.parent / "posts"


def call(method, path, base=None, token=None, **params):
    token = token or TOKEN
    params["access_token"] = token
    data = urllib.parse.urlencode(params).encode()
    url = f"{base or API}/{path}"
    if method == "GET":
        req = urllib.request.Request(url + "?" + data.decode())
    else:
        req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace").replace(token, "***")
        raise SystemExit(f"API error {e.code} on {path}: {body}")


def wait_ready(cid, tries=30):
    for _ in range(tries):
        st = call("GET", cid, fields="status_code").get("status_code")
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            raise SystemExit(f"container {cid} status {st}")
        time.sleep(5)
    raise SystemExit(f"container {cid} not ready in time")


def raw_url(folder, name):
    return f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/posts/{folder}/{urllib.parse.quote(name)}"


def th(method, path, **params):
    return call(method, path, base=TH_API, token=TH_TOKEN, **params)


def th_wait(cid, tries=60):
    for _ in range(tries):
        r = th("GET", cid, fields="status,error_message")
        if r.get("status") == "FINISHED":
            return
        if r.get("status") in ("ERROR", "EXPIRED"):
            raise SystemExit(f"Threads container {cid}: {r}")
        time.sleep(5)
    raise SystemExit(f"Threads container {cid} not ready in time")


CHECK = False


def publish_threads(folder, post):
    """Text post on Threads. Optional: topic_tag, reply (posted as a reply, e.g. sources)."""
    if DRY:
        print(f"[dry-run] would post to Threads {folder}: {post['text'][:40]}...")
        return None
    if not TH_TOKEN:
        raise SystemExit("THREADS_ACCESS_TOKEN is not set")
    extra = {"topic_tag": post["topic_tag"]} if post.get("topic_tag") else {}
    imgs = post.get("images", [])
    if post.get("video"):
        cid = th("POST", "me/threads", media_type="VIDEO", video_url=raw_url(folder, post["video"]), text=post["text"], **extra)["id"]
        th_wait(cid)
        if CHECK:
            print(f"[check] Threads video container {cid} is ready (not published)")
            return None
    elif not imgs:
        cid = th("POST", "me/threads", media_type="TEXT", text=post["text"], **extra)["id"]
    elif len(imgs) == 1:
        cid = th("POST", "me/threads", media_type="IMAGE", image_url=raw_url(folder, imgs[0]), text=post["text"], **extra)["id"]
    else:
        kids = [th("POST", "me/threads", media_type="IMAGE", image_url=raw_url(folder, n), is_carousel_item="true")["id"] for n in imgs]
        time.sleep(15)
        cid = th("POST", "me/threads", media_type="CAROUSEL", children=",".join(kids), text=post["text"], **extra)["id"]
    if not post.get("video"):
        time.sleep(30 if imgs else 10)
    mid = th("POST", "me/threads_publish", creation_id=cid)["id"]
    if post.get("reply"):
        time.sleep(5)
        rid = th("POST", "me/threads", media_type="TEXT", text=post["reply"], reply_to_id=mid)["id"]
        time.sleep(10)
        th("POST", "me/threads_publish", creation_id=rid)
    return mid


def publish_reel(folder, post):
    v = post["video"]
    if not v.lower().endswith(".mp4"):
        raise SystemExit(f"{folder}/{v}: use an MP4 file")
    if DRY:
        print(f"[dry-run] would publish reel {folder}: {raw_url(folder, v)}")
        return None
    extra = {"cover_url": raw_url(folder, post["cover"])} if post.get("cover") else {}
    cid = call("POST", f"{IG_USER_ID}/media", media_type="REELS", video_url=raw_url(folder, v),
               caption=post["caption"], share_to_feed="true", **extra)["id"]
    wait_ready(cid, tries=72)
    if CHECK:
        print(f"[check] Instagram reel container {cid} is ready (not published)")
        return None
    return call("POST", f"{IG_USER_ID}/media_publish", creation_id=cid)["id"]


def publish_story(folder, post):
    """Instagram Stories: "story": true with "images" (JPEG, 1080x1920) and/or "video".
    Each file becomes one story frame, published in the listed order."""
    files = list(post.get("images", []))
    if post.get("video"):
        files.append(post["video"])
    if DRY:
        print(f"[dry-run] would publish {len(files)} story frame(s) from {folder}")
        return None
    ids = []
    for n in files:
        if n.lower().endswith(".mp4"):
            cid = call("POST", f"{IG_USER_ID}/media", media_type="STORIES", video_url=raw_url(folder, n))["id"]
            wait_ready(cid, tries=72)
        else:
            if not n.lower().endswith((".jpg", ".jpeg")):
                raise SystemExit(f"{folder}/{n}: Instagram accepts JPEG only")
            cid = call("POST", f"{IG_USER_ID}/media", media_type="STORIES", image_url=raw_url(folder, n))["id"]
            wait_ready(cid)
        if CHECK:
            print(f"[check] story container {cid} for {n} is ready (not published)")
            continue
        ids.append(call("POST", f"{IG_USER_ID}/media_publish", creation_id=cid)["id"])
        time.sleep(3)
    return ",".join(ids) if ids else None


def publish(folder, post):
    if post.get("story"):
        return publish_story(folder, post)
    if post.get("platform") == "threads":
        return publish_threads(folder, post)
    if post.get("video"):
        return publish_reel(folder, post)
    imgs = post["images"]
    for n in imgs:
        if not n.lower().endswith((".jpg", ".jpeg")):
            raise SystemExit(f"{folder}/{n}: Instagram accepts JPEG only")
    if DRY:
        print(f"[dry-run] would publish {folder}: {len(imgs)} image(s)")
        for n in imgs:
            print("   ", raw_url(folder, n))
        return None
    if len(imgs) == 1:
        cid = call("POST", f"{IG_USER_ID}/media", image_url=raw_url(folder, imgs[0]), caption=post["caption"])["id"]
    else:
        children = []
        for n in imgs:
            c = call("POST", f"{IG_USER_ID}/media", image_url=raw_url(folder, n), is_carousel_item="true")["id"]
            wait_ready(c)
            children.append(c)
        cid = call("POST", f"{IG_USER_ID}/media", media_type="CAROUSEL", children=",".join(children), caption=post["caption"])["id"]
    wait_ready(cid)
    return call("POST", f"{IG_USER_ID}/media_publish", creation_id=cid)["id"]


def main():
    global CHECK
    if len(sys.argv) == 3 and sys.argv[1] == "--check":
        CHECK = True
        d = ROOT / sys.argv[2]
        post = json.loads((d / "post.json").read_text(encoding="utf-8"))
        publish(d.name, post)
        print("check finished")
        return
    if not (TOKEN or TH_TOKEN) and not DRY:
        sys.exit("no access token is set")
    now = dt.datetime.now(dt.timezone.utc)
    done = 0
    for d in sorted(p for p in ROOT.iterdir() if p.is_dir()):
        meta, out = d / "post.json", d / "published.json"
        if not meta.exists() or out.exists():
            continue
        post = json.loads(meta.read_text(encoding="utf-8"))
        if not post.get("approved"):
            print(f"skip {d.name}: not approved")
            continue
        when = dt.datetime.fromisoformat(post["publish_at"])
        if when > now:
            print(f"wait {d.name}: scheduled {post['publish_at']}")
            continue
        media_id = publish(d.name, post)
        if media_id:
            out.write_text(json.dumps({"media_id": media_id, "published_at": now.isoformat()}, ensure_ascii=False, indent=2))
            print(f"published {d.name}: media {media_id}")
            done += 1
    print(f"done: {done} post(s) published")


if __name__ == "__main__":
    main()
