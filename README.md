# eurogrid-posts

Instagram publishing queue for Eurogrid (@eurogrid_jp).

- `posts/<folder>/post.json` + JPEG images. A post is published by GitHub Actions
  when `approved` is `true` and `publish_at` has passed. `published.json` is written afterwards.
- Secret `IG_ACCESS_TOKEN`: Instagram User access token (system user token from Business settings,
  permissions `instagram_basic`, `instagram_content_publish`).
- `Check Instagram token` runs every Monday; it fails (and GitHub emails you) if the token stopped working. System user tokens last 60 days: regenerate in Business settings > System users > eurogrid-publisher.
- Run `Publish to Instagram` manually with dry_run=1 to check without posting.
