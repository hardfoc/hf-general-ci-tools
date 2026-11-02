"""The ``hardfoc`` MkDocs plugin: the shared configuration and the page checks of every HardFOC documentation site.

A site's ``mkdocs.yml`` only names the site and the repository; this plugin fills in the rest, so every site has the
same Markdown dialect, the same validation and the same versioning without copying configuration around:

* **Defaults** (a value the site sets wins): ``site_url`` (``https://<org>.github.io/<repo>/latest/``, the canonical
  address of every page), ``repo_name``, ``edit_uri`` (``edit/main/docs/``), ``copyright``, ``extra.version``
  (mike, default ``latest``), ``extra.social`` and ``extra.generator: false``.
* **Markdown extensions**: snippets (``--8<-- "tests/docs/x.cpp:section"`` includes code the repository compiles,
  paths from the repository root), admonitions, details, tabs, tables, footnotes, attribute lists, Markdown in HTML, task
  lists, keys, emoji, highlighting with line anchors, Mermaid fences and GitHub-style heading anchors (so ``#links``
  work on GitHub and on the site). The site may add more.
* **Validation**: a link MkDocs cannot resolve, a missing anchor or a page left out of the navigation is a warning,
  which ``mkdocs build --strict`` turns into a failure.
* **Build inputs stay out of the site**: figure modules and their data, ``*.py``, Doxygen output under
  ``docs/_doxygen/`` and PDFs (a link to a PDF goes to the file on GitHub, which renders it).
* **Page transforms** (``hooks.py``): links to repository files become GitHub links at the commit being built,
  links into the API reference become plain links, figure markers become light / dark image pairs, raw-HTML paths
  are re-based, ``\\|`` in table code spans is unescaped.
* **Page checks** (each one fails a strict build): a page left with Jekyll front matter or Liquid tags, a page
  without a level-one heading, an image without alt text or pointing at no file.
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path

from mkdocs.config import config_options as c
from mkdocs.config.base import Config
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.files import InclusionLevel

from . import hooks

log = get_plugin_logger(__name__)

JEKYLL_KEYS = ("layout", "nav_order", "parent", "grand_parent", "has_children", "permalink", "nav_exclude")
LIQUID = re.compile(r"\{%-?\s*(raw|endraw|include|if|for|assign|capture|comment|highlight)\b|\{\{\s*(site|page)\.")
H1 = re.compile(r"^#\s+\S|^<h1\b|^[^\n]+\n=+\s*$", re.M)
EXCLUDE = (
    re.compile(r"^diagrams/(figures|data)/"),
    re.compile(r"^_doxygen/"),
    re.compile(r"\.(py|pyc|pdf)$"),
    re.compile(r"^diagrams/figures\.json$"),
)


def _slugify():
    from pymdownx.slugs import slugify

    return slugify(case="lower")


def _extensions() -> dict[str, dict]:
    from material.extensions import emoji
    from pymdownx.superfences import fence_code_format

    return {
        "abbr": {},
        "admonition": {},
        "attr_list": {},
        "def_list": {},
        "footnotes": {},
        "md_in_html": {},
        "tables": {},
        "toc": {"permalink": True, "slugify": _slugify(), "toc_depth": 3},
        "pymdownx.betterem": {},
        "pymdownx.caret": {},
        "pymdownx.details": {},
        "pymdownx.emoji": {"emoji_index": emoji.twemoji, "emoji_generator": emoji.to_svg},
        "pymdownx.highlight": {"anchor_linenums": True, "line_spans": "__span", "pygments_lang_class": True},
        "pymdownx.inlinehilite": {},
        "pymdownx.keys": {},
        "pymdownx.mark": {},
        "pymdownx.smartsymbols": {},
        "pymdownx.superfences": {
            "custom_fences": [{"name": "mermaid", "class": "mermaid", "format": fence_code_format}]
        },
        "pymdownx.tabbed": {"alternate_style": True, "slugify": _slugify()},
        "pymdownx.tasklist": {"custom_checkbox": True},
        "pymdownx.tilde": {},
    }


def versioned_setting(option: bool | None, org_site: bool) -> bool:
    """Whether the site is versioned: the environment wins, then the plugin option, then the kind of repository."""
    env = os.environ.get("HARDFOC_DOCS_VERSIONED", "").strip().lower()
    if env in ("true", "1", "yes"):
        return True
    if env in ("false", "0", "no"):
        return False
    if option is not None:
        return option
    return not org_site


class HardfocConfig(Config):
    org = c.Type(str, default="hardfoc")
    portal_url = c.Type(str, default="https://hardfoc.github.io/")
    api_dir = c.Type(str, default="api")
    default_branch = c.Type(str, default="main")
    #: Fail the build on Jekyll front matter and Liquid tags left over from a migration.
    forbid_jekyll = c.Type(bool, default=True)
    #: Fail the build on a page without a level-one heading.
    require_h1 = c.Type(bool, default=True)
    #: Versioned with mike (``/<version>/`` folders, version selector). Unset: versioned, except the organisation
    #: site ``<org>.github.io``, which is served from the root. ``HARDFOC_DOCS_VERSIONED=true|false`` overrides both
    #: (ru-mkdocs-publish.yml sets it from its ``versioning`` input).
    versioned = c.Optional(c.Type(bool))


class HardfocPlugin(BasePlugin[HardfocConfig]):
    def on_config(self, config):
        root = Path(config.config_file_path).resolve().parent
        org = self.config.org

        if config.theme.name != "hardfoc":
            log.warning("theme is %r: use `theme: {name: hardfoc}` for the HardFOC look", config.theme.name)

        m = re.search(r"github\.com/([^/]+)/([^/#?]+)", config.repo_url or "")
        org_site = bool(m) and m.group(2).removesuffix(".git").lower() == f"{org}.github.io"
        versioned = versioned_setting(self.config.versioned, org_site)
        self.versioned = versioned
        if m:
            owner, name = m.group(1), m.group(2).removesuffix(".git")
            pages = f"https://{org}.github.io/" if org_site else f"https://{org}.github.io/{name}/"
            if not config.site_url and owner.lower() == org.lower():
                # A versioned site serves every version under /<version>/; the canonical address of a page is its
                # `latest` copy. An unversioned site is served from its root.
                config.site_url = pages + "latest/" if versioned else pages
            if owner.lower() == org.lower():
                config.extra.setdefault("hardfoc", {}).setdefault("site_root", pages)
            if config.repo_name in (None, "", "GitHub"):  # MkDocs' default for a GitHub repo_url
                config.repo_name = f"{owner}/{name}"
        if config.repo_url and config.edit_uri in (None, "", "edit/master/docs/"):  # MkDocs' default
            config.edit_uri = f"edit/{self.config.default_branch}/docs/"
        if not config.copyright:
            config.copyright = "Copyright &copy; HardFOC contributors"

        extra = config.extra
        extra.setdefault("generator", False)
        extra.setdefault("api_dir", self.config.api_dir)
        if versioned:
            extra.setdefault("version", {"provider": "mike", "default": "latest", "alias": True})
        elif extra.get("version"):
            log.warning("extra.version is set on an unversioned site: remove it (no version selector without mike)")
        extra.setdefault(
            "social",
            [{"icon": "fontawesome/brands/github", "link": f"https://github.com/{org}", "name": "HardFOC on GitHub"}],
        )
        extra.setdefault("hardfoc", {})
        extra["hardfoc"].setdefault("portal_url", self.config.portal_url)
        extra["hardfoc"].setdefault("org_url", f"https://github.com/{org}")

        exts = list(config.markdown_extensions)
        defaults = _extensions()
        # Code on a page is included from files the repository compiles: --8<-- "tests/docs/x.cpp:section".
        defaults["pymdownx.snippets"] = {"base_path": [str(root)], "check_paths": True, "dedent_subsections": True}
        for name, opts in defaults.items():
            if name not in exts:
                exts.append(name)
            config.mdx_configs.setdefault(name, opts)
        config.markdown_extensions = exts

        v = config.validation
        v.nav.omitted_files = logging.WARNING
        v.nav.not_found = logging.WARNING
        v.links.not_found = logging.WARNING
        v.links.anchors = logging.WARNING
        v.links.unrecognized_links = logging.WARNING
        v.links.absolute_links = logging.WARNING

        hooks.configure(config, root, extra["api_dir"])
        return config

    def on_files(self, files, config):
        api = (config.extra.get("api_dir") or "api").strip("/") + "/"
        for f in files:
            if f.is_documentation_page() and f.dest_uri.startswith(api):
                log.warning("%s: builds to %s, where the API reference is merged: rename it (e.g. api-reference.md)",
                            f.src_uri, f.dest_uri)
            if any(rx.search(f.src_uri) for rx in EXCLUDE) and not f.src_uri.startswith("assets/hardfoc/"):
                if f.abs_src_path and Path(config.docs_dir) in Path(f.abs_src_path).parents:
                    f.inclusion = InclusionLevel.EXCLUDED
        return files

    def on_page_markdown(self, markdown, page, config, files):
        src = page.file.src_uri
        body = hooks.outside_fences(markdown, lambda t: re.sub(r"`[^`\n]+`", "", t))
        if self.config.forbid_jekyll:
            if any(k in page.meta for k in JEKYLL_KEYS):
                log.warning("%s: Jekyll front matter (layout/nav_order/parent/permalink): remove it", src)
            if LIQUID.search(body):
                log.warning("%s: Liquid tag ({%% raw %%}, {{ site.* }}, ...): remove it", src)
        if self.config.require_h1 and not (page.meta.get("title") or H1.search(body)):
            log.warning("%s: no level-one heading: start the page with '# Title'", src)
        return hooks.on_page_markdown(markdown, page, config, files)

    def on_post_build(self, config):
        hooks.on_post_build(config)
