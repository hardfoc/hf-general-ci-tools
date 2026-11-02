#!/usr/bin/env python3
"""Move a HardFOC repository's documentation from Jekyll (just-the-docs) to the MkDocs platform: the mechanical part.

What it does, in order (docs/MIGRATING-TO-MKDOCS.md is the whole procedure, including the parts a person does):

1. **Pages.** Every Markdown file under ``docs/`` (and every README.md / Markdown file elsewhere in the repository,
   outside submodules and build folders) loses its Jekyll front matter. A page whose body has no level-one heading
   gets ``# <front-matter title>``. ``{% raw %}`` / ``{% endraw %}`` tags are removed. Decorative emoji are removed
   from headings and from the front-matter titles used for the navigation, and every ``#anchor`` link to a heading
   that changed is rewritten to the new anchor.
2. **Navigation.** ``nav_order`` / ``parent`` / ``title`` become ``docs/.nav.yml`` (mkdocs-awesome-nav), in the old
   order. Pages whose parent is the site itself sit at the top level; children follow their parent's position.
3. **Doxygen.** ``_config/Doxyfile`` moves to ``Doxyfile``; the doxygen-awesome stylesheet, header, footer and extra
   files are dropped (the publish workflow gives the API the HardFOC look) and ``OUTPUT_DIRECTORY`` becomes
   ``build/doxygen``. The ``doxygen-awesome-css`` submodule is removed.
4. **Site files.** ``mkdocs.yml`` and ``.github/workflows/ci-docs-publish.yml`` are written from the templates below.
5. **Jekyll goes.** ``_config/_config.yml``, ``_config/_includes``, ``_config/_layouts``, ``_config/assets``,
   ``_config/404.html``, ``Gemfile*``, ``_config.yml``, ``404.html``, ``docs/version_selector*`` and
   ``docs/_config.yml`` are deleted (with ``git rm`` when the repository is a git checkout).

Nothing is committed. ``--check`` changes nothing, prints the plan and exits 1 when there is something to migrate (0
when the repository is already on the platform), so it doubles as a CI guard.

Usage::

    python3 tools/docs-migrate.py PATH/TO/REPO [--check] [--name "TMC9660 Driver"] [--description "..."]
                                               [--workflow-ref v1]
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

FRONT = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*\n?", re.S)
RAW = re.compile(r"[ \t]*\{%-?\s*(?:end)?raw\s*-?%\}[ \t]*\n?")
H1 = re.compile(r"^#\s+\S", re.M)
HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$", re.M)
FENCE = re.compile(r"^(?P<indent>[ \t]*)(?P<fence>`{3,}|~{3,}).*?^(?P=indent)(?P=fence)[ \t]*$", re.M | re.S)
# Pictographs, dingbats, symbols, variation selectors, keycaps and ZWJ: what GitHub drops from anchors.
EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F900-\U0001F9FF\U00002B00-\U00002BFF"
    "\U00002190-\U000021FF\U00002300-\U000023FF\U0000FE0F\U0000200D\U000020E3]+"
)
SKIP_DIRS = {".git", "build", "site", "node_modules", ".venv", "venv", "third_party", "external", "_doxygen"}
JEKYLL_PATHS = [
    "_config/_config.yml",
    "_config/_includes",
    "_config/_layouts",
    "_config/assets",
    "_config/404.html",
    "_config.yml",
    "404.html",
    "Gemfile",
    "Gemfile.lock",
    "docs/_config.yml",
    "docs/Gemfile",
    "docs/404.html",
]
DOXY_DROP = re.compile(
    r"^(HTML_EXTRA_STYLESHEET|HTML_EXTRA_FILES|HTML_HEADER|HTML_FOOTER|HTML_STYLESHEET|HTML_COLORSTYLE|"
    r"HTML_COLORSTYLE_HUE|HTML_COLORSTYLE_SAT|HTML_COLORSTYLE_GAMMA|HTML_DYNAMIC_MENUS|GENERATE_TREEVIEW|"
    r"DISABLE_INDEX|FULL_SIDEBAR|HTML_COPY_CLIPBOARD|HTML_PROJECT_COOKIE|GENERATE_TAGFILE)\b"
)

MKDOCS_YML = """\
# Documentation site on the HardFOC MkDocs platform: theme, plugin and toolchain come from the hardfoc-mkdocs-theme
# package in hardfoc/hf-general-ci-tools. Preview locally:
#
#   pip install "git+https://github.com/hardfoc/hf-general-ci-tools@{ref}\\
#   #subdirectory=packages/hardfoc-mkdocs-theme"      (one line, without the backslash)
#   mkdocs serve                                     http://127.0.0.1:8000
#   mkdocs build --strict                            what CI runs
#   hardfoc-docs figures && hardfoc-docs gen         refresh figures and generated tables
#
# Pages: docs/, order: docs/.nav.yml, rules: docs/DOCS-STYLE-GUIDE.md in hf-general-ci-tools.
site_name: {name}
site_description: >-
  {description}
repo_url: https://github.com/{repo}

theme:
  name: hardfoc

plugins:
  - hardfoc
  - search
  - awesome-nav
"""

WORKFLOW_YML = """\
---
# Documentation: strict MkDocs build, figure / generated-region checks, Doxygen under /api/, offline link check,
# Lighthouse budget and screenshots on pull requests; publish to gh-pages with mike (main -> dev, vX.Y.Z tag ->
# that version + latest). Inputs: docs/ru-mkdocs-publish.md in hardfoc/hf-general-ci-tools.
name: Docs

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: docs-${{{{ github.ref }}}}
  cancel-in-progress: ${{{{ github.event_name == 'pull_request' }}}}

jobs:
  docs:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-mkdocs-publish.yml@{ref}
    permissions:
      contents: write  # the publish job pushes gh-pages; pull requests never publish
    with:
{with_block}      deploy: true
"""


class Plan:
    def __init__(self, root: Path, check: bool):
        self.root, self.check, self.actions = root, check, []
        self.git = (root / ".git").exists()

    def note(self, msg: str) -> None:
        self.actions.append(msg)
        print(("would " if self.check else "") + msg)

    def write(self, rel: str, text: str) -> None:
        p = self.root / rel
        if p.exists() and p.read_text() == text:
            return
        self.note(f"write {rel}")
        if not self.check:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)

    def remove(self, rel: str) -> None:
        p = self.root / rel
        if not (p.exists() or p.is_symlink()):
            return
        self.note(f"delete {rel}")
        if self.check:
            return
        if self.git and subprocess.run(["git", "-C", str(self.root), "rm", "-r", "-q", "-f", "--", rel],
                                       capture_output=True).returncode == 0:
            return
        shutil.rmtree(p) if p.is_dir() else p.unlink()

    def move(self, src: str, dst: str) -> None:
        if not (self.root / src).exists():
            return
        self.note(f"move {src} -> {dst}")
        if self.check:
            return
        if not (self.git and subprocess.run(["git", "-C", str(self.root), "mv", src, dst],
                                            capture_output=True).returncode == 0):
            (self.root / src).rename(self.root / dst)


def strip_emoji(s: str) -> str:
    return re.sub(r"\s{2,}", " ", EMOJI.sub("", s)).strip()


def gh_slug(text: str) -> str:
    """GitHub's heading anchor: lower case, punctuation and emoji dropped, spaces to hyphens."""
    t = re.sub(r"<[^>]+>", "", text)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = t.replace("`", "").lower()
    t = "".join(ch for ch in t if ch.isalnum() or ch in " -_")
    return t.replace(" ", "-")


def outside_fences(text: str, fn) -> str:
    out, pos = [], 0
    for m in FENCE.finditer(text):
        out.append(fn(text[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(fn(text[pos:]))
    return "".join(out)


def markdown_files(root: Path) -> list[Path]:
    subs = set()
    gm = root / ".gitmodules"
    if gm.exists():
        subs = {m.strip() for m in re.findall(r"^\s*path\s*=\s*(.+)$", gm.read_text(), re.M)}
    out = []
    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(root)
        if any(part in SKIP_DIRS or part.startswith(".") for part in rel.parts[:-1]):
            continue
        if any(rel.as_posix().startswith(s.rstrip("/") + "/") for s in subs):
            continue
        out.append(p)
    return out


def migrate_pages(plan: Plan) -> dict[str, dict]:
    """Strip front matter, add H1, drop raw tags and heading emoji. Returns the front matter of docs/ pages."""
    root = plan.root
    meta: dict[str, dict] = {}
    anchor_maps: dict[Path, dict[str, str]] = {}
    texts: dict[Path, str] = {}
    for p in markdown_files(root):
        text = p.read_text()
        fm = {}
        m = FRONT.match(text)
        if m:
            try:
                fm = yaml.safe_load(m.group(1)) or {}
            except yaml.YAMLError:
                fm = {}
            if not isinstance(fm, dict):
                fm = {}
            text = text[m.end():].lstrip("\n")
        text = RAW.sub("", text)
        amap: dict[str, str] = {}

        def heading(hm: re.Match) -> str:
            old = hm.group(2)
            new = strip_emoji(old)
            if new != old:
                o, n = gh_slug(old), gh_slug(new)
                if o != n:
                    amap[o] = n
            return f"{hm.group(1)} {new}"

        text = outside_fences(text, lambda t: HEADING.sub(heading, t))
        title = strip_emoji(str(fm.get("title", "")).strip())
        if title and not H1.search(FENCE.sub("", text)):
            text = f"# {title}\n\n{text}"
        rel = p.relative_to(root).as_posix()
        if rel.startswith("docs/"):
            meta[rel[len("docs/"):]] = {**fm, "title": title}
        anchor_maps[p] = amap
        texts[p] = text

    # Rewrite links to anchors that changed: same-page (#a) and cross-page (page.md#a).
    for p, text in texts.items():
        def fix(t: str) -> str:
            def link(m: re.Match) -> str:
                target = m.group(2)
                path, _, frag = target.partition("#")
                if not frag:
                    return m.group(0)
                dest = p if not path else (p.parent / path).resolve()
                amap = anchor_maps.get(dest) or anchor_maps.get(Path(str(dest)))
                if amap and frag in amap:
                    return f"{m.group(1)}({path}#{amap[frag]})"
                return m.group(0)

            return re.sub(r"(\[[^\]]*\])\(([^)\s]+)\)", link, t)

        new = outside_fences(text, fix)
        if new != p.read_text():
            plan.note(f"rewrite {p.relative_to(root).as_posix()} (front matter, H1, Liquid, heading emoji, anchors)")
            if not plan.check:
                p.write_text(new)
    return meta


def nav_yml(meta: dict[str, dict]) -> str:
    """docs/.nav.yml from nav_order / parent / title (top-level docs/ pages and their children)."""
    titles = {rel: m.get("title") or rel for rel, m in meta.items()}
    by_title = {}
    for rel, m in meta.items():
        by_title.setdefault(m.get("title", ""), rel)

    def order(rel: str):
        o = meta[rel].get("nav_order")
        return (o if isinstance(o, (int, float)) else 999, rel)

    def parent_of(rel: str):
        par = strip_emoji(str(meta[rel].get("parent", "") or ""))
        return by_title.get(par) if par and by_title.get(par) != rel else None

    roots = [r for r in meta if parent_of(r) is None and not meta[r].get("nav_exclude")]
    children: dict[str, list[str]] = {}
    for r in meta:
        par = parent_of(r)
        if par and not meta[r].get("nav_exclude"):
            children.setdefault(par, []).append(r)
    # A parent page that is only a hub (docs/index.md with has_children) sits first; its children join the top level.
    lines = ["---", "# Site navigation (mkdocs-awesome-nav): the tabs and sidebar, in this order.", "nav:"]
    flat: list[str] = []

    def emit(rel: str):
        flat.append(rel)
        for c in sorted(children.get(rel, []), key=order):
            emit(c)

    for r in sorted(roots, key=order):
        emit(r)
    seen = set()
    if "index.md" in meta:
        lines.append("  - Home: index.md")
        seen.add("index.md")
    for rel in flat:
        if rel in seen or rel.endswith("version_selector.md"):
            continue
        seen.add(rel)
        t = str(titles[rel]).replace('"', "'")
        lines.append(f'  - "{t}": {rel}')
    for rel in sorted(set(meta) - seen):
        if not rel.endswith("version_selector.md"):
            lines.append(f'  - "{titles[rel]}": {rel}')
    return "\n".join(lines) + "\n"


def migrate_doxyfile(plan: Plan) -> str | None:
    src = None
    for cand in ("_config/Doxyfile", "docs/Doxyfile", "Doxyfile"):
        if (plan.root / cand).exists():
            src = cand
            break
    if not src:
        return None
    text = (plan.root / src).read_text()
    # A dropped key's backslash-continued lines go with it.
    cleaned, skipping = [], False
    for line in text.splitlines():
        stripped = line.strip()
        if skipping:
            skipping = stripped.endswith("\\")
            continue
        if DOXY_DROP.match(stripped):
            skipping = stripped.endswith("\\")
            continue
        if re.match(r"^\s*OUTPUT_DIRECTORY\s*=", line):
            line = "OUTPUT_DIRECTORY       = build/doxygen"
        elif re.match(r"^\s*HTML_OUTPUT\s*=", line):
            line = "HTML_OUTPUT            = html"
        cleaned.append(line)
    new = "\n".join(cleaned).rstrip() + "\n"
    if src != "Doxyfile":
        plan.move(src, "Doxyfile")
    if text != new:
        if not plan.check:
            (plan.root / "Doxyfile").write_text(new)
        plan.note("clean Doxyfile (doxygen-awesome, header/footer dropped; OUTPUT_DIRECTORY build/doxygen)")
    return "Doxyfile"


def remove_submodule(plan: Plan, path_part: str) -> None:
    gm = plan.root / ".gitmodules"
    if not gm.exists():
        return
    for path in re.findall(r"^\s*path\s*=\s*(.+)$", gm.read_text(), re.M):
        path = path.strip()
        if path_part in path:
            plan.note(f"remove submodule {path}")
            if not plan.check:
                subprocess.run(["git", "-C", str(plan.root), "submodule", "deinit", "-f", "--", path],
                               capture_output=True)
                subprocess.run(["git", "-C", str(plan.root), "rm", "-q", "-f", "--", path], capture_output=True)
                shutil.rmtree(plan.root / ".git/modules" / path, ignore_errors=True)


def site_identity(root: Path, name: str | None, description: str | None) -> tuple[str, str, str]:
    cfg = {}
    for cand in ("_config/_config.yml", "_config.yml", "docs/_config.yml"):
        if (root / cand).exists():
            try:
                cfg = yaml.safe_load((root / cand).read_text()) or {}
            except yaml.YAMLError:
                cfg = {}
            break
    repo = ""
    try:
        url = subprocess.run(["git", "-C", str(root), "remote", "get-url", "origin"], capture_output=True,
                             text=True).stdout.strip()
        m = re.search(r"github\.com[:/]([^/]+/[^/]+?)(?:\.git)?$", url)
        repo = m.group(1) if m else ""
    except OSError:
        pass
    repo = repo or f"hardfoc/{root.name}"
    title = name or re.sub(r"^HardFOC\s+", "", str(cfg.get("title") or root.name)).strip()
    desc = description or " ".join(str(cfg.get("description") or "").split()) or "TODO: one sentence on what this is."
    return title, desc, repo


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo", type=Path)
    ap.add_argument("--check", action="store_true", help="change nothing; exit 1 if there is anything to migrate")
    ap.add_argument("--name", help="site name (default: _config.yml title without 'HardFOC ')")
    ap.add_argument("--description", help="one-sentence site description (default: _config.yml description)")
    ap.add_argument("--workflow-ref", default="v1", help="hf-general-ci-tools ref the caller workflow uses")
    args = ap.parse_args(argv)

    root = args.repo.resolve()
    if not (root / "docs").is_dir():
        print(f"{root}: no docs/ folder", file=sys.stderr)
        return 2
    plan = Plan(root, args.check)
    name, desc, repo = site_identity(root, args.name, args.description)

    meta = migrate_pages(plan)
    if not (root / "docs/.nav.yml").exists():
        plan.write("docs/.nav.yml", nav_yml(meta))
    for p in sorted((root / "docs").glob("version_selector*")):
        plan.remove(p.relative_to(root).as_posix())

    doxy = migrate_doxyfile(plan)
    remove_submodule(plan, "doxygen-awesome")
    if (root / "_config/doxygen-extensions").exists():
        plan.remove("_config/doxygen-extensions")

    if not (root / "mkdocs.yml").exists():
        plan.write("mkdocs.yml", MKDOCS_YML.format(name=name, description=desc, repo=repo, ref=args.workflow_ref))
    with_block = f"      doxygen_config: {doxy}\n" if doxy else ""
    plan.write(".github/workflows/ci-docs-publish.yml", WORKFLOW_YML.format(ref=args.workflow_ref,
                                                                             with_block=with_block))
    for rel in JEKYLL_PATHS:
        plan.remove(rel)

    gi = root / ".gitignore"
    lines = gi.read_text().splitlines() if gi.exists() else []
    missing = [x for x in ("site/", "build/") if x not in lines and x.rstrip("/") not in lines]
    if missing:
        plan.write(".gitignore", "\n".join(lines + missing) + "\n")

    if args.check:
        print(f"\n{len(plan.actions)} change(s) to make" if plan.actions else "already migrated")
        return 1 if plan.actions else 0
    print(f"\n{len(plan.actions)} change(s) made. Next: write the pages to docs/DOCS-STYLE-GUIDE.md, then "
          "`mkdocs build --strict`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
