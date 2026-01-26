from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
import shutil
import datetime as dt

import yaml
import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
OUT = ROOT / "docs"

FONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.S)

@dataclass
class Entry:
    kind: str
    slug: str
    title: str
    date: str
    tags: list[str]
    authors: list[str]
    html: str

def slugify(name: str) -> str:
    s = name.rsplit(".", 1)[0].lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "post"

def parse_md(path: Path, kind: str) -> Entry:
    raw = path.read_text(encoding="utf-8")

    fm = {}
    body = raw

    m = FONTMATTER_RE.match(raw)
    if m:
        fm_text, body = m.group(1), m.group(2)
        fm = yaml.safe_load(fm_text) or {}

    title = str(fm.get("title") or slugify(path.name))
    date = str(fm.get("date") or "")
    tags = fm.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    else:
        tags = [str(t).strip() for t in tags if str(t).strip()]

    authors = fm.get("authors", [])
    if isinstance(authors, str):
        authors = [authors]
    elif not isinstance(authors, list):
        authors = []
        authors = [str(a).strip() for a in authors if str(a).strip()]

    html = markdown.markdown(
        body,
        extensions=["fenced_code", "codehilite", "tables"],
        extension_configs={
            "codehilite": {
                "css_class": "codehilite",
                "guess_lang": False,
                "use_pygments": True,
            }
        },
        output_format="html5",
    )

    return Entry(
        kind=kind,
        slug=slugify(path.name),
        title=title,
        date=date,
        tags=tags,
        authors=authors,
        html=html,
    )

def load_entries(kind: str) -> list[Entry]:
    entries = []
    for p in sorted((CONTENT / kind).glob("*.md")):
        entries.append(parse_md(p, kind))

    # newest first if date is YYYY-MM-DD; blanks go last
    entries.sort(key=lambda e: (e.date == "", e.date), reverse=True)
    return entries

def write_html(rel: str, html: str) -> None:
    out_path = OUT / rel.lstrip("/")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

def main() -> None:
    # clean dist
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)

    # copy static assets
    if STATIC.exists():
        shutil.copytree(STATIC, OUT, dirs_exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html"]),
    )

    year = str(dt.datetime.now().year)

    posts = load_entries("posts")
    projects = load_entries("projects")

    home_tpl = env.get_template("home.html")
    write_html(
        "/index.html",
        home_tpl.render(title="Home", year=year, posts=posts[:5], projects=projects[:5]),
    )

    list_tpl = env.get_template("list.html")
    write_html(
        "/posts/index.html",
        list_tpl.render(title="Posts", year=year, heading="Posts", intro="Short writeups and notes.",
                        entries=posts, kind="posts"),
    )
    write_html(
        "projects/index.html",
        list_tpl.render(title="Projects", year=year, heading="Projects", intro="Projects and longer work.",
                        entries=projects, kind="projects"),
    )

    post_tpl = env.get_template("post.html")
    for e in posts + projects:
        write_html(
            f"/{e.kind}/{e.slug}/index.html",
            post_tpl.render(title=e.title, year=year, entry=e),
        )

    print("Built site -> docs/")

if __name__ == "__main__":
    main()
