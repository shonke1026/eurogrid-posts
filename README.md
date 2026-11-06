# eurogrid-posts

Instagram publishing queue for Eurogrid (@eurogrid_jp).

- `posts/<folder>/post.json` + JPEG images. A post is published by GitHub Actions
  when `approved` is `true` and `publish_at` has passed. `published.json` is written afterwards.
- Secret `IG_ACCESS_TOKEN`: Instagram User access token (system user token from Business settings,
  permissions `instagram_basic`, `instagram_content_publish`).
- `Check Instagram token` runs every Monday; it fails (and GitHub emails you) if the token stopped working. System user tokens last 60 days: regenerate in Business settings > System users > eurogrid-publisher.
- Run `Publish to Instagram` manually with dry_run=1 to check without posting.

## Voice (VOICEVOX)
Put `voice/<job>/lines.json` (file, speaker, style, speed, text) and push.
The "Make voice" workflow runs the VOICEVOX engine, makes the WAV files and
`credits.txt`, and commits them back. Credit the voices in every post that
uses them, e.g. `VOICEVOX:春日部つむぎ、VOICEVOX:玄野武宏`.
