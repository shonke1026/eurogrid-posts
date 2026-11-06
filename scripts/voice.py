"""Make WAV files from voice/<job>/lines.json with a local VOICEVOX engine.

lines.json: [{"file": "lucia_01.wav", "speaker": "春日部つむぎ", "style": "ノーマル",
              "text": "...", "speed": 1.15}]
Existing WAVs are skipped (delete one to remake it). Writes credits.txt per job.
"""
import json, pathlib, sys, time, urllib.parse, urllib.request

ENGINE = "http://127.0.0.1:50021"


def get(path):
    with urllib.request.urlopen(ENGINE + path, timeout=30) as r:
        return json.load(r)


def post(path, body=None, raw=False):
    data = json.dumps(body).encode() if body is not None else b""
    req = urllib.request.Request(ENGINE + path, data=data, method="POST",
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read() if raw else json.load(r)


def wait_engine():
    for _ in range(90):
        try:
            print("VOICEVOX engine", get("/version"))
            return
        except Exception:
            time.sleep(2)
    sys.exit("VOICEVOX engine did not start")


def main():
    wait_engine()
    ids = {}
    for sp in get("/speakers"):
        for st in sp["styles"]:
            ids[(sp["name"], st["name"])] = st["id"]
    made = 0
    for lines_file in sorted(pathlib.Path("voice").glob("*/lines.json")):
        job = lines_file.parent
        credits = set()
        for item in json.loads(lines_file.read_text(encoding="utf-8")):
            key = (item["speaker"], item.get("style", "ノーマル"))
            if key not in ids:
                sys.exit(f"unknown voice {key}; available: {sorted(ids)}")
            credits.add(f"VOICEVOX:{item['speaker']}")
            out = job / item["file"]
            if out.exists():
                continue
            q = post("/audio_query?" + urllib.parse.urlencode(
                {"text": item["text"], "speaker": ids[key]}))
            q["speedScale"] = item.get("speed", 1.1)
            q["prePhonemeLength"] = 0.05
            q["postPhonemeLength"] = 0.1
            out.write_bytes(post(f"/synthesis?speaker={ids[key]}", q, raw=True))
            print("made", out)
            made += 1
        (job / "credits.txt").write_text("、".join(sorted(credits)) + "\n", encoding="utf-8")
    print(f"done, {made} new file(s)")


if __name__ == "__main__":
    main()
