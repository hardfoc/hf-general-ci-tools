---
layout: default
title: "MkDocs Publisher (Reusable)"
description: "Reusable workflow: the HardFOC documentation platform: build, check, audit and publish a versioned MkDocs site"
nav_order: 4
parent: "🔄 Reusable Workflows"
---

# MkDocs Publisher (reusable)

**Workflow:** `ru-mkdocs-publish.yml` (**[RU] MkDocs Publish**)

Builds a HardFOC documentation site with the shared theme, checks it, audits it and publishes it to `gh-pages` as
a versioned site with [mike](https://github.com/jimporter/mike), with the Doxygen API reference under `api/`.
[MIGRATING-TO-MKDOCS.md](MIGRATING-TO-MKDOCS.md) moves a repository onto it; [DOCS-STYLE-GUIDE.md](DOCS-STYLE-GUIDE.md)
says what its pages contain.

## Where the theme comes from

The theme, the plugin, figkit and the pinned toolchain are the `hardfoc-mkdocs-theme` package in
[`packages/hardfoc-mkdocs-theme`](../packages/hardfoc-mkdocs-theme/README.md). Every job installs it with pip from
**the commit this workflow runs from** (the `job` context's `workflow_repository` and `workflow_sha`), so a caller
pinned to `@v1` builds with the theme released in `v1`, and a branch under review builds with that branch's theme.
`theme_ref` overrides the ref. A repository's own `requirements-docs.txt`, if it has one, is installed afterwards
for extra plugins.

## What runs when

| Event | Build + checks | Lighthouse + screenshots | Publish |
| --- | --- | --- | --- |
| Pull request | Yes | Yes | Never, whatever `deploy` says |
| Push to the default branch | Yes | Yes | Version `dev` (when `deploy` is true); `dev` also holds `latest` until the first release |
| Push of a `vX.Y.Z` tag | Yes | Yes | Version `vX.Y.Z` (`release_version: minor`: `X.Y`), and `latest` moves to it |

With `versioning: false` (the organisation portal) there are no versions: see
[Unversioned sites](#unversioned-sites).

The site root redirects to `latest`. Aliases are symlinks, so the API reference added to a version folder is
reachable through them too. Material's version selector in the header lists every version.

## Jobs and permissions

The caller must grant `contents: write` for the publish job; a caller that never publishes can grant `contents: read`.

| Job | Permissions | Steps |
| --- | --- | --- |
| `build` | `contents: read` | Check out (plus `submodule_paths`), install the theme, run `check_commands` (`hardfoc-docs check`), `mkdocs build --strict`, Doxygen into `api/` (with the HardFOC API stylesheet when the Doxyfile has none), lychee `--offline --include-fragments` on the merged site, upload `docs-site` |
| `quality` | `contents: read` | Lighthouse CI (median of 3 runs, mobile emulation) on the home page and the first navigation pages against `lighthouse_budgets`, upload `lighthouse-report`; Playwright screenshots at 375 and 1280 px, light and dark, upload `docs-screenshots` |
| `deploy` | `contents: write` | Versioned: prune the pre-MkDocs site from `gh-pages` (`prune_legacy`), `mike deploy`, add the API reference to the version folder, `mike set-default latest`, root `404.html`, push (never force). Unversioned: `hardfoc-docs publish-root` commits the built site as the whole branch, push (never force) |

Every action is pinned to a commit SHA with its version in a comment.

## The first publish

A repository with an older (Jekyll / Doxygen) site on `gh-pages`: everything at the top of the branch that is not
a mike version or alias is removed in one commit before mike writes (kept: `versions.json`, `index.html` once
mike owns it, `404.html`, `.nojekyll`, `CNAME`, `robots.txt`). A repository without `gh-pages`: mike creates the
branch. In both cases the root gets mike's redirect to `latest/` and a `404.html` that sends old addresses to the
same page under `latest/` (`/docs/x/`, `/development/x/` to `latest/x/`; `/doxs/`, `/html/` to `latest/api/`).

## Inputs

| Input | Type | Default | Description |
| --- | --- | --- | --- |
| `python_version` | string | `3.12` | Python used to build the site |
| `requirements` | string | `requirements-docs.txt` | Optional extra pip requirements, installed after the theme when the file exists |
| `theme_ref` | string | empty | Ref of this repository to install the theme from; empty: the workflow's own commit |
| `mkdocs_config` | string | `mkdocs.yml` | Path of `mkdocs.yml` |
| `submodules` | string | `false` | `false`, `true` or `recursive` |
| `submodule_paths` | string | empty | Space-separated submodule paths initialised (shallow) after checkout, nested ones included |
| `check_commands` | string | `hardfoc-docs check` | Shell lines run before the build (a repository's own `tools/figkit` / `tools/docs/gen.py` when present) |
| `doxygen_config` | string | empty | Doxyfile of the API reference; empty builds no API |
| `doxygen_working_directory` | string | `.` | Directory Doxygen runs in |
| `doxygen_html_dir` | string | empty | Generated HTML directory; empty reads `OUTPUT_DIRECTORY` / `HTML_OUTPUT` |
| `api_dir` | string | `api` | Site folder for the Doxygen HTML |
| `link_check` | boolean | `true` | lychee offline on the merged site |
| `link_check_args` | string | empty | Extra lychee arguments |
| `lighthouse` | boolean | `true` | Run the Lighthouse budget |
| `lighthouse_budgets` | string | `performance=0.8 accessibility=0.95 best-practices=0.9 seo=0.9` | Minimum category scores (median of 3 runs) |
| `screenshots` | boolean | `true` | Capture phone and desktop screenshots, light and dark |
| `versioning` | boolean | `true` | `true`: versioned with mike. `false`: one site, published from the default branch at the root of `deployment_branch` |
| `deploy` | boolean | `false` | Publish; ignored on pull requests |
| `deployment_branch` | string | `gh-pages` | Branch GitHub Pages serves |
| `dev_version` | string | `dev` | Version a push to the default branch publishes |
| `latest_alias` | string | `latest` | Alias moved to each release |
| `release_version` | string | `tag` | `tag` publishes `vX.Y.Z`; `minor` publishes `X.Y` |
| `prune_legacy` | boolean | `true` | Remove the pre-MkDocs site from the deployment branch on publish |

## Example

```yaml
name: 📚 Docs

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
  group: docs-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}

jobs:
  docs:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-mkdocs-publish.yml@v1
    permissions:
      contents: write
    with:
      doxygen_config: Doxyfile
      deploy: true
```

## Unversioned sites

The organisation portal (`hardfoc.github.io`) has one current site, not versions. With `versioning: false`:

| Piece | Versioned (default) | Unversioned |
| --- | --- | --- |
| `site_url` | `https://hardfoc.github.io/<repo>/latest/` | `https://hardfoc.github.io/` (or `/<repo>/`) |
| Version selector, older-version banner | Yes | No |
| Push to the default branch | Publishes `dev` | Replaces the whole deployment branch with the built site, in one ordinary commit (`.nojekyll` written; a `CNAME` only when the site has one, `docs/CNAME`; no commit when nothing changed) |
| Push of a `v*` tag | Publishes `vX.Y.Z` | Nothing (a notice) |
| Pull request | Build, checks, Lighthouse, screenshots | The same |

The build job tells the theme plugin through `HARDFOC_DOCS_VERSIONED`, so the input decides both the build and the
publish. A local build of the portal needs nothing: the plugin treats `<org>.github.io` as unversioned on its own,
and `plugins: [{hardfoc: {versioned: false}}]` does the same for any other site.

```yaml
jobs:
  site:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-mkdocs-publish.yml@v1
    permissions:
      contents: write
    with:
      versioning: false
      deploy: true
```

Pages must serve the `gh-pages` branch from `/` once the first publish has run; until then, leave the Pages source
as it is, so the current site stays up.

## After the first publish

GitHub Pages must serve the `gh-pages` branch from `/` (**Settings > Pages > Build and deployment**: source
*Deploy from a branch*, branch `gh-pages`, folder `/`). The workflow never changes repository settings.
