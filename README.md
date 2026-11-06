# eurogrid-posts

Instagram publishing queue for Eurogrid (@eurogrid_jp).

- `posts/<folder>/post.json` + JPEG images. A post is published by GitHub Actions
  when `approved` is `true` and `publish_at` has passed. `published.json` is written afterwards.
- Secret `IG_ACCESS_TOKEN`: Instagram User access token (Instagram API with Instagram Login,
  permissions `instagram_business_basic`, `instagram_business_content_publish`).
- `Refresh Instagram token` runs twice a month to keep the token alive.
- Run `Publish to Instagram` manually with dry_run=1 to check without posting.
