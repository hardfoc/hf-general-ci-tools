# hardfoc-mkdocs-theme

The HardFOC documentation theme for MkDocs, as one package: the `hardfoc` theme, the `hardfoc` plugin, figkit, the
`hardfoc-docs` command and the pinned toolchain (mkdocs, mkdocs-material, mkdocs-awesome-nav, pymdown-extensions,
mike). Every HardFOC documentation site builds with it; no site carries CSS, templates or hooks of its own.

```bash
pip install "git+https://github.com/hardfoc/hf-general-ci-tools@v1#subdirectory=packages/hardfoc-mkdocs-theme"
```

`ru-mkdocs-publish.yml` installs it from the same commit as the workflow, so `@v1` callers get the matching theme.

## A site

```yaml
site_name: TMC9660 Driver
site_description: One sentence.
repo_url: https://github.com/hardfoc/hf-tmc9660-driver

theme:
  name: hardfoc

plugins:
  - hardfoc
  - search
  - awesome-nav
```

The plugin fills in `site_url` (`https://hardfoc.github.io/<repo>/latest/`; the root for an unversioned site), `repo_name`, `edit_uri`, copyright,
mike versioning, the Markdown extensions (admonitions, tabs, snippets from the repository root, Mermaid,
GitHub-style anchors, ...) and strict validation.

A site is versioned with mike unless it is the organisation site (`hardfoc.github.io`), or sets
`plugins: [{hardfoc: {versioned: false}}]`; `HARDFOC_DOCS_VERSIONED=true|false` overrides both (the publish
workflow sets it from its `versioning` input). An unversioned site has no version selector and its `site_url` is
the Pages root.

### Configuration outside the root

A repository that keeps tool configuration in `_config/` puts the site there with `docs_dir: ../docs`
(and `site_dir: ../site`, so a local build lands where it would with a root `mkdocs.yml`):

```yaml
# _config/mkdocs.yml
site_name: TMC9660 Driver
repo_url: https://github.com/hardfoc/hf-tmc9660-driver
docs_dir: ../docs
site_dir: ../site
theme:
  name: hardfoc
plugins:
  - hardfoc
  - search
  - awesome-nav
```

The repository root is then the folder that holds `docs_dir`, not the folder of the configuration, so snippets,
repository links, figures and generated regions resolve as they would with a root `mkdocs.yml`. Build with
`mkdocs build -f _config/mkdocs.yml`; `hardfoc-docs` finds `_config/mkdocs.yml` from anywhere in the repository
(or takes `-f _config/mkdocs.yml`), and the publish workflow takes `mkdocs_config: _config/mkdocs.yml`.

## What is in it

| Path | What |
| --- | --- |
| `hardfoc_mkdocs_theme/theme/` | Theme (`extends: material`): `main.html`, header with the org crumb, footer, inline mark, `assets/hardfoc/hardfoc.css` (tokens for light and dark, typography, admonitions, code, tables, hero, cards, chip card, figures, Mermaid, focus), the Doxygen stylesheet, the root `404.html` |
| `hardfoc_mkdocs_theme/plugin.py` | Defaults, Markdown extensions, validation, build-input exclusion, page checks |
| `hardfoc_mkdocs_theme/hooks.py` | Repository links to GitHub, API links, figure embeds, raw-HTML rebase, image and alt-text gate |
| `hardfoc_mkdocs_theme/figkit/` | Code-sourced SVG figures, light and dark from one layout, contrast-checked |
| `hardfoc_mkdocs_theme/gen.py`, `generators/` | `<!-- generated: name -->` regions; built in: `examples` (from `examples/*/app_config.yml`) |
| `hardfoc_mkdocs_theme/screenshots.py` | Phone / desktop, light / dark screenshots of a built site |
| `hardfoc_mkdocs_theme/publish.py` | `publish-root`: an unversioned site as the whole deployment branch |
| `tests/` | Unit tests (`python -m unittest discover -s tests`), run by the self-CI |

## Commands

```text
hardfoc-docs [-f CONFIG] COMMAND        CONFIG: the site configuration (default: nearest mkdocs.yml or _config/mkdocs.yml)
hardfoc-docs figures [--check] [ids]   build (or check) docs/diagrams/figures/*.py
hardfoc-docs gen [--check|--list]      fill (or check) generated regions (built-in + tools/docs/generators/)
hardfoc-docs check                     both checks, as CI runs them
hardfoc-docs screenshots SITE OUT      needs the [screenshots] extra and `playwright install chromium`
hardfoc-docs pages SITE                the pages CI audits
hardfoc-docs publish-root SITE         commit SITE as the whole deployment branch (unversioned sites)
```

## Brand

Indigo `#3B38C4` (primary), teal `#5EEAD4` / `#0B7A72` (accent), ink `#17202C`; dark surface `#0D1220`. Inter for
text and JetBrains Mono for code, from Google Fonts, loaded without blocking the first paint. The mark is a stator
ring of three phase arcs with a field vector (`theme/assets/hardfoc/mark.svg`, `wordmark.svg`, `favicon.svg`).
Every text colour is at least 4.5:1 on its background in both schemes; the ratios are noted in `hardfoc.css`.
