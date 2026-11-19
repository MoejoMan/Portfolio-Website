Blog posts live here as `.md` files. The filename becomes the URL, so
`jigsaw-static-analysis.md` is served at `/blog/jigsaw-static-analysis`.

Start every post with a frontmatter block:

    ---
    title: The post title
    date: 2026-11-30
    summary: One sentence, shown on the blog index.
    tags: Forensics, Malware
    draft: false
    ---

`draft: true` keeps a post off the site entirely. To preview drafts locally,
set `BLOG_SHOW_DRAFTS=1` before starting the app.

Images for a post go in `static/blog/<slug>/` and are referenced as
`/static/blog/<slug>/figure-1.png`.

This file has no frontmatter block, so it is skipped rather than listed.
