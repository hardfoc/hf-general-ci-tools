---
layout: default
title: "Adopting the MkDocs site"
description: "How a HardFOC repository moves to the MkDocs documentation platform"
nav_order: 5
parent: "🔄 Reusable Workflows"
---

# Adopting the MkDocs site

The HardFOC documentation platform is three pieces that live in this repository:

| Piece | Where | What it gives a repository |
| --- | --- | --- |
| Starter site | `templates/mkdocs-site/` | `mkdocs.yml`, a `docs/` skeleton, the HardFOC look (`overrides/`, `docs/stylesheets/hardfoc.css`, a logo slot), the hooks module and figkit |
| Reusable workflow | `.github/workflows/ru-mkdocs-publish.yml` | Strict build, drift checks, Doxygen under `api/`, offline link check, versioned publish with mike ([inputs](ru-mkdocs-publish.md)) |
| This guide | `docs/MKDOCS.md` | The steps below |

Driver repositories keep the Jekyll pipeline (`ru-docs-publish.yml`); the platform is meant for HAL and product
repositories whose documentation is a site a newcomer reads, not only an API reference.

## What the starter site contains

```text
templates/mkdocs-site/
├── mkdocs.yml                     Material, strict validation, awesome-nav, Mermaid, GitHub-style anchors, mike
├── requirements-docs.txt          the pinned toolchain the workflow installs
├── overrides/main.html            HardFOC overrides (older-version banner)
├── docs/
│   ├── .nav.yml                   top tabs, in order
│   ├── index.md                   landing page: hero, figure, cards
│   ├── getting-started.md
│   ├── learn/  architecture/  guides/  reference/  adr/
│   ├── reference/api.md           the link into the Doxygen reference
│   ├── assets/logo.svg            logo slot (replace with the repository's mark)
│   ├── stylesheets/hardfoc.css    palette tokens (contrast-checked, light and dark), typography, hero, cards
│   └── diagrams/                  figure modules, generated SVGs and the figure catalogue
└── tools/
    ├── docs/mkdocs_hooks.py       link rewriting, API links, figure embeds, raw-HTML rebase, image and alt-text gate
    ├── docs/gen.py                fills <!-- generated: name --> regions from tools/docs/generators/*.py
    └── figkit/                    figure library and build.py (--check is the drift gate)
```

### The hooks module

`tools/docs/mkdocs_hooks.py` lets a page link to anything in the repository the way GitHub resolves it:

- a link to a file outside `docs/` (or to a non-page file inside it) becomes a link to that file on GitHub at the
  commit being built, so a link MkDocs still cannot resolve is a real broken link and fails `--strict`;
- a link into `docs/api/` becomes a plain link the offline link check verifies once the API reference is merged;
- `<!-- figure: id -->` markers become a light / dark image pair that follows the theme toggle, with a caption
  and a long description listing the files the figure is drawn from;
- relative paths in raw HTML are re-based to the page MkDocs writes;
- after the build, every image must exist and have non-empty alt text.

### figkit

A figure is a Python module in `docs/diagrams/figures/`. `data()` extracts the facts from the code and names the
file each fact came from; `build(data)` lays the figure out with figkit cards, regions and arrows; colours are
tokens with a light and a dark value. `python3 tools/figkit/build.py` writes `<id>.svg`, `<id>.dark.svg`, the
extracted data and the figure catalogue, and fills every embed. It refuses a figure with text below 4.5:1 contrast
in either theme, content that does not fit its card, overlapping cards, an arrow that runs under a card, or no alt
text. `--check` regenerates everything in memory and fails if anything committed differs, so a code change that
moves a figure fails CI until the figure is rebuilt.

## Adopt it in a repository

1. **Copy the starter site** into the repository root:

    ```bash
    cp -R path/to/hf-general-ci-tools/templates/mkdocs-site/. .
    ```

2. **Edit `mkdocs.yml`**: the five lines marked `EDIT` (name, description, site URL, repository). Replace
   `docs/assets/logo.svg` if the repository has its own mark.
3. **Keep build inputs out of the site**: if Doxygen writes under `docs/`, keep its folder in `exclude_docs`
   (`/_doxygen/` is already there). Remove the old Jekyll files (`_config.yml`, `_layouts/`, `_includes/`) once
   nothing uses them.
4. **Write the pages.** Replace the example figure (`docs/diagrams/figures/docs-pipeline.py`) with figures drawn
   from the repository's code; put generators for tables in `tools/docs/generators/`.
5. **Build locally**:

    ```bash
    python3 -m pip install -r requirements-docs.txt
    python3 tools/figkit/build.py && python3 tools/docs/gen.py
    mkdocs build --strict
    ```

6. **Call the workflow** from `.github/workflows/`, with the submodules the checks need and the Doxyfile if there
   is an API reference (full example in [the workflow page](ru-mkdocs-publish.md#example)):

    ```yaml
    jobs:
      docs:
        uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-mkdocs-publish.yml@main
        permissions:
          contents: write
        with:
          submodule_paths: lib/core/hf-core-drivers/internal/hf-pincfg
          doxygen_config: _config/Doxyfile
          deploy: ${{ vars.ENABLE_GITHUB_PAGES_DEPLOY == 'true' }}
    ```

7. **Markdown lint**: the site uses Material syntax (admonitions, tabs, attribute lists, a little HTML). If the
   repository runs markdownlint, allow the HTML elements the site uses (`MD033` `allowed_elements`) and turn off
   `MD046` (admonition bodies are indented).

## After the first publish

The repository owner checks, once, that GitHub Pages serves the `gh-pages` branch from `/` (**Settings, Pages**). If
the branch held an older site, its files stay next to the version folders until someone removes them; the root
`index.html` is replaced by mike's redirect to the default version.

## Keeping the template and the sites in step

The sites copy the template; they do not import it. When the template's hooks, figkit or stylesheet change, copy
the changed files into each site and run its checks. Keep product names out of the template.
