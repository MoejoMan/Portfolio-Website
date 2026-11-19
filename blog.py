"""Markdown backed blog.

Posts live in posts/ as .md files. The filename is the URL slug. Each file
starts with a frontmatter block:

    ---
    title: Building a Cowrie honeypot that feeds an ELK SIEM
    date: 2026-11-30
    summary: One sentence that shows on the blog index.
    tags: Honeypot, ELK, Hetzner
    draft: false
    ---

Set draft: true to keep a post out of the index and off the site. Drafts are
visible locally when BLOG_SHOW_DRAFTS=1 is set, so you can preview one before
publishing it.
"""

import datetime
import os
import pathlib

import markdown

POSTS_DIR = pathlib.Path(__file__).parent / "posts"

MD_EXTENSIONS = ["fenced_code", "codehilite", "tables", "toc", "attr_list"]
MD_CONFIG = {"codehilite": {"css_class": "codehilite", "guess_lang": False}}

_TRUTHY = ("1", "true", "yes", "on")


def _show_drafts():
    return os.getenv("BLOG_SHOW_DRAFTS", "").strip().lower() in _TRUTHY


def _parse_frontmatter(text):
    """Split a leading '---' delimited key: value block off the top of a post."""
    meta = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    meta[key.strip().lower()] = value.strip()
            body = parts[2].lstrip("\n")
    return meta, body


def _build_post(meta, slug):
    raw_date = meta.get("date", "")
    try:
        date = datetime.date.fromisoformat(raw_date)
    except ValueError:
        date = None
    return {
        "slug": slug,
        "title": meta.get("title", slug.replace("-", " ").capitalize()),
        "date": date,
        "date_display": date.strftime("%d %B %Y").lstrip("0") if date else "",
        "summary": meta.get("summary", ""),
        "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
        "draft": meta.get("draft", "").strip().lower() in _TRUTHY,
    }


def load_posts(include_drafts=None):
    """Every post, newest first. Drafts are excluded unless asked for."""
    if include_drafts is None:
        include_drafts = _show_drafts()
    posts = []
    if not POSTS_DIR.is_dir():
        return posts
    for path in sorted(POSTS_DIR.glob("*.md")):
        meta, body = _parse_frontmatter(path.read_text(encoding="utf-8"))
        if not meta:
            continue
        post = _build_post(meta, path.stem)
        if post["draft"] and not include_drafts:
            continue
        post["body"] = body
        posts.append(post)
    posts.sort(key=lambda p: p["date"] or datetime.date.min, reverse=True)
    return posts


def get_post(slug, include_drafts=None):
    """One post by slug, or None.

    Slugs are compared against files already loaded from posts/, so a crafted
    slug cannot escape the directory.
    """
    for post in load_posts(include_drafts):
        if post["slug"] == slug:
            return post
    return None


def render_body(post):
    """Markdown to HTML. Returns the body and its table of contents."""
    md = markdown.Markdown(extensions=MD_EXTENSIONS, extension_configs=MD_CONFIG)
    html = md.convert(post["body"])
    return html, getattr(md, "toc", "")
