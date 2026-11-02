---
layout: default
title: "Migrating a repository to MkDocs"
description: "Step by step: move one HardFOC repository from the Jekyll docs site to the MkDocs platform"
nav_order: 6
parent: "🔄 Reusable Workflows"
---

# Migrating a repository to MkDocs

Move one repository's documentation from the Jekyll (just-the-docs) site to the HardFOC MkDocs platform, from a
clean checkout to a published, versioned site. Plan on half a day for a driver: the mechanical part takes minutes,
the rest is rewriting pages to the [style guide](DOCS-STYLE-GUIDE.md).

The pilot is `hardfoc/hf-tmc9660-driver`: when a step is unclear, look at what that repository does.

## What the platform gives a repository

| Piece | Where it lives | The repository keeps |
| --- | --- | --- |
| Theme: brand, layout, header, footer, version selector, components | `packages/hardfoc-mkdocs-theme` (`theme: hardfoc`) | nothing |
| Plugin: Markdown dialect, validation, link rewriting, figure embeds, page checks | same package (`plugins: [hardfoc]`) | nothing |
| figkit and generated regions (`hardfoc-docs figures`, `hardfoc-docs gen`) | same package | figure modules under `docs/diagrams/figures/`, optional generators under `tools/docs/generators/` |
| Toolchain (mkdocs, mkdocs-material, awesome-nav, pymdown, mike) | pinned by the package | nothing |
| Build, checks, Doxygen, link check, Lighthouse, screenshots, publish | `ru-mkdocs-publish.yml` | a 30-line caller |

The workflow installs the package from the **same commit** as itself, so a caller pinned to `@v1` always gets the
theme released with `v1`. A repository never carries CSS, templates, hooks or a requirements file for the site.

## The repository contract

After migration a repository has exactly these documentation files:

```text
mkdocs.yml                          site name, description, repo_url, theme: hardfoc, three plugins
Doxyfile                            moved from _config/, OUTPUT_DIRECTORY = build/doxygen, no custom CSS
docs/.nav.yml                       the navigation
docs/*.md                           pages: plain Markdown, no Jekyll front matter, no Liquid
docs/diagrams/figures/*.py          figkit figure modules (optional) and their generated SVGs
docs/datasheet/*.pdf                linked, never rendered (the site links them on GitHub)
docs/_doxygen/mainpage.md           Doxygen main page (optional)
tests/docs/*.cpp                    code shown on the pages, compiled by the host build (drivers)
tools/docs/generators/*.py          repository-specific generated regions (optional)
.github/workflows/ci-docs-publish.yml
```

Everything Jekyll is gone: `_config/_config.yml`, `_config/_includes/`, `_config/_layouts/`, `_config/assets/`,
`_config/404.html`, `Gemfile*`, `docs/version_selector*`, Liquid `raw` / `endraw` tags and the `doxygen-awesome-css` submodule.
`_config/` keeps the lint configurations (`.markdownlint.json`, `.yamllint`, `.clang-*`, `lychee.toml`).

## Steps

### 1. Branch and install

```bash
git clone https://github.com/hardfoc/<repo>.git && cd <repo>
git switch -c docs/mkdocs-platform
python3 -m venv .venv && . .venv/bin/activate
pip install "git+https://github.com/hardfoc/hf-general-ci-tools@v1#subdirectory=packages/hardfoc-mkdocs-theme"
```

Use `@main` (or the branch under review) instead of `@v1` until the platform release that contains the package is
out.

### 2. Run the mechanical migration

```bash
python3 path/to/hf-general-ci-tools/tools/docs-migrate.py . --check     # the plan; changes nothing
python3 path/to/hf-general-ci-tools/tools/docs-migrate.py . --name "TMC9660 Driver" \
    --description "One sentence on what this is."
git add -A && git commit -m "Docs: move the site files to the MkDocs platform"
```

The script strips front matter (adding `# Title` where a page had none), removes Liquid raw tags, drops emoji from
headings and rewrites the anchors that changed, writes `docs/.nav.yml` from `nav_order` / `parent`, moves and
cleans the Doxyfile, removes the doxygen-awesome submodule, writes `mkdocs.yml` and the caller workflow and deletes
the Jekyll files. It also strips front matter from README files elsewhere in the repository. Run `--check` again:
it must print `already migrated`.

### 3. Build

```bash
mkdocs build --strict
```

Fix every warning: strict mode turns them into failures, in CI too. The usual ones:

| Warning | Fix |
| --- | --- |
| `contains a link 'x.md', but the target is not found` | The page was renamed; fix the link |
| `unrecognized relative link 'folder/'` | Link a file, or the folder is fine once it exists outside `docs/` (the plugin links it on GitHub) |
| `no level-one heading` | Start the page with `# Title` |
| `Jekyll front matter` / `Liquid tag` | Remove it (the migration missed a file outside `docs/`?) |
| `builds to api/...` | A page named `api.md` collides with the Doxygen output: call it `api-reference.md` |
| `image(s) have no alt text` | Every image needs alt text |

### 4. Rewrite the pages to the style guide

Follow [DOCS-STYLE-GUIDE.md](DOCS-STYLE-GUIDE.md): the standard page set for the repository type, a purpose line
under every title, task-oriented API guide, verified code, a figure for the architecture, tables for registers.
For a driver:

1. Rename pages to the standard set (`hardware.md`, `porting.md`, `api-guide.md`, ...) and rewrite `.nav.yml`
   into the five tabs (Home, Get started, Concepts, Guides, Reference).
2. Put every C++ snippet in `tests/docs/*.cpp`, add them to an `OBJECT` library in `tests/CMakeLists.txt` (see the
   pilot), and include them with `--8<-- "tests/docs/file.cpp:section"`. Build it.
3. Draw the layer figure with figkit (`docs/diagrams/figures/driver-layers.py`, reading class names from the
   headers) and run `hardfoc-docs figures`.
4. Fill the example table with `<!-- generated: examples -->` and run `hardfoc-docs gen`.
5. Rewrite the README to the README standard.

### 5. Doxygen

The workflow runs Doxygen from the repository root with the `Doxyfile` and merges the HTML under `api/`.

- `OUTPUT_DIRECTORY = build/doxygen`, `HTML_OUTPUT = html` (the workflow creates the folder).
- No `HTML_EXTRA_STYLESHEET`: the workflow then adds the HardFOC API stylesheet and `HTML_COLORSTYLE = AUTO_LIGHT`.
- `CASE_SENSE_NAMES = NO`, so page names are the same on every OS (`classns_1_1_my_class.html`) and links from the
  site stay valid.
- `GENERATE_TAGFILE` empty; `INPUT` the headers (and `src/`), not the examples.
- A main page in `docs/_doxygen/mainpage.md` (`USE_MDFILE_AS_MAINPAGE`), not the README (badges and pictures
  break inside Doxygen).

Check it locally the way CI does, then run the link check on the merged result:

```bash
mkdir -p build/doxygen && doxygen Doxyfile
mkdocs build --strict -d /tmp/site && mkdir -p /tmp/site/api && cp -a build/doxygen/html/. /tmp/site/api/
lychee --offline --include-fragments --index-files index.html --root-dir /tmp/site '/tmp/site/**/*.html'
```

### 6. Lint and look

```bash
hardfoc-docs check                                   # figures and generated regions current
npx markdownlint-cli2 --config _config/.markdownlint.json "docs/**/*.md" "*.md"
pip install "hardfoc-mkdocs-theme[screenshots] @ git+https://github.com/hardfoc/hf-general-ci-tools@v1#subdirectory=packages/hardfoc-mkdocs-theme"
playwright install chromium
hardfoc-docs screenshots /tmp/site /tmp/shots         # 375 and 1280 px, light and dark
```

Add `"MD033": false` (or allow the theme's HTML elements), `"MD046": false` and `"MD041": false` to
`_config/.markdownlint.json`: pages use Material components and indented admonition bodies. Open the screenshots
and read every page on the phone size.

### 7. Pull request

Commit in small steps (site files; page rewrite; snippets and CMake; README) and open the pull request. CI must be
green: the docs job runs the strict build, the drift checks, Doxygen, the offline link check, the Lighthouse
budget, and uploads `docs-site`, `lighthouse-report` and `docs-screenshots` artifacts. Look at the screenshots
artifact before asking for review.

## gh-pages and GitHub Pages

### The first publish replaces the old site

The first push to `main` after the merge publishes version `dev` with mike. In the same run, before mike writes,
the workflow removes **every top-level entry of `gh-pages` that is not a mike version or alias** (the Jekyll site's
`development/`, `doxs/`, `html/`, `index.md`, `version_selector.html`, ...) in one ordinary commit, "Remove the
previous documentation site". Nothing is force-pushed. Kept: `versions.json`, mike's root `index.html`,
`.nojekyll`, `CNAME`, `robots.txt`. The root `index.html` then redirects to `latest/`, and a root `404.html` sends
old addresses (`/repo/docs/quickstart/`, `/repo/doxs/...`, `/repo/html/...`) to the same page under `latest/`
(and Doxygen pages under `latest/api/`).

A repository with no `gh-pages` branch at all gets one from mike on the first publish.

Turn the cleanup off with `prune_legacy: false` if a repository keeps hand-made files at the top of `gh-pages`.

### Versions

| Event | Version published | Aliases |
| --- | --- | --- |
| Push to `main` | `dev` | `latest`, until the first release |
| Tag `vX.Y.Z` | `vX.Y.Z` (`release_version: minor` publishes `X.Y`) | `latest` moves to it |
| Pull request | nothing | |

The header shows the version selector; older versions show a banner linking to the latest.

### Pages settings (owner, once per repository)

**Settings > Pages > Build and deployment**: Source **Deploy from a branch**, branch **gh-pages**, folder **/**.
Every HardFOC repository on the Jekyll pipeline already uses this, so usually nothing changes. A repository set
to **GitHub Actions** as the source would never show the mike site: switch it to the branch.

Check after the first publish:

```bash
gh api repos/hardfoc/<repo>/pages --jq '.build_type, .source'     # legacy, {branch: gh-pages, path: /}
curl -sI https://hardfoc.github.io/<repo>/ | head -1              # 200, redirect page to latest/
curl -s https://hardfoc.github.io/<repo>/versions.json            # [{"version": "dev", "aliases": ["latest"]...}]
```

## When something goes wrong

| Symptom | Cause |
| --- | --- |
| Docs job fails at "Install the theme" | The caller pins a ref of hf-general-ci-tools without the package (older than the platform release) |
| Old pages still served at the root | The first publish has not run yet, or `prune_legacy` is false |
| Site shows the README rendered by Jekyll | Pages source is a branch other than `gh-pages`, or **GitHub Actions** |
| API links 404 on the site | `CASE_SENSE_NAMES` differs from when the links were written; set it to `NO` |
| Lighthouse fails on performance only | A heavy image: export SVG, or compress; check the `lighthouse-report` artifact |
