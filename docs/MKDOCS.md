---
layout: default
title: "Adopting the MkDocs site"
description: "Where the HardFOC MkDocs documentation platform lives and how a repository adopts it"
nav_order: 5
parent: "🔄 Reusable Workflows"
---

# Adopting the MkDocs site

The HardFOC documentation platform is four pieces in this repository:

| Piece | Where | What it gives a repository |
| --- | --- | --- |
| Theme package | [`packages/hardfoc-mkdocs-theme`](../packages/hardfoc-mkdocs-theme/README.md) | `theme: hardfoc` (brand, layout, components), `plugins: [hardfoc]` (Markdown dialect, validation, link rewriting, figures, page checks), figkit, `hardfoc-docs`, the pinned toolchain |
| Reusable workflow | [`ru-mkdocs-publish.yml`](ru-mkdocs-publish.md) | Strict build, drift checks, Doxygen under `api/`, offline link check, Lighthouse budget, screenshots, versioned publish with mike |
| Migration tool | `tools/docs-migrate.py` | The mechanical move from Jekyll, with a `--check` dry run |
| Guides | [MIGRATING-TO-MKDOCS.md](MIGRATING-TO-MKDOCS.md), [DOCS-STYLE-GUIDE.md](DOCS-STYLE-GUIDE.md) | The procedure and the page rules |

`templates/mkdocs-site/` is the skeleton of a driver site on the platform (the self-CI builds it); copy it for a new
repository, or run `tools/docs-migrate.py` on an existing Jekyll one.

## Sites that copied the earlier template

`hf-hal-flux-v1` and `hf-hal-vortex-v1` started from the earlier template, which copied `overrides/`,
`docs/stylesheets/hardfoc.css`, `tools/docs/` and `tools/figkit/` into the repository. Move them onto the package:
set `theme: {name: hardfoc}` and `plugins: [hardfoc, search, awesome-nav]`, delete the copies and
`requirements-docs.txt`, change figure modules to `from hardfoc_mkdocs_theme.figkit import Fig`, and move
repository-specific generators to `tools/docs/generators/` (they run under `hardfoc-docs gen`).
