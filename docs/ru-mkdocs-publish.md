---
layout: default
title: "MkDocs Publisher (Reusable)"
description: "Reusable workflow: strict MkDocs build, drift and link checks, versioned publish with mike and the Doxygen API"
nav_order: 4
parent: "🔄 Reusable Workflows"
---

# MkDocs Publisher (reusable)

**Workflow:** `ru-mkdocs-publish.yml` (**[RU] MkDocs Publish**)

Builds a MkDocs (Material) documentation site in strict mode, checks that generated figures and tables still match
the code, merges the Doxygen API reference under `api/`, checks every link of the result offline, and publishes it
to `gh-pages` as a versioned site with [mike](https://github.com/jimporter/mike).
A repository adopts it with the starter site in `templates/mkdocs-site/`; see [Adopting the MkDocs site](MKDOCS.md).

Driver repositories that publish a Jekyll site keep using [`ru-docs-publish.yml`](ru-docs-publish.md).

## What runs when

| Event | Build + checks | Publish |
| --- | --- | --- |
| Pull request | Yes | Never, whatever `deploy` says |
| Push to the default branch | Yes | As version `dev` (when `deploy` is true) |
| Push of a `vX.Y[.Z]` tag | Yes | As version `X.Y`, and the `latest` alias moves to it (when `deploy` is true) |

The site's root redirects to `latest` once a release has been published, and to `dev` until then. Material's
version selector lists every published version.

## Jobs and permissions

The workflow declares `permissions: {}` and grants each job only what it needs. A caller must grant at least
`contents: write` for the publish job to run; a caller that never publishes can grant `contents: read`.

| Job | Permissions | Steps |
| --- | --- | --- |
| `build` | `contents: read` | Check out (plus `submodule_paths`), install the pinned toolchain, run `check_commands`, `mkdocs build --strict`, Doxygen into `api/`, lychee `--offline` on the built site, upload the site as the `docs-site` artifact |
| `deploy` | `contents: write` | `mike deploy` to `deployment_branch`, add the API reference from the artifact to the version folder, `mike set-default`, push (never force) |

Every action is pinned to a commit SHA with its version in a comment.

## Inputs

| Input | Type | Default | Description |
| --- | --- | --- | --- |
| `python_version` | string | `3.12` | Python used to build the site |
| `requirements` | string | `requirements-docs.txt` | pip requirements with the pinned toolchain |
| `mkdocs_config` | string | `mkdocs.yml` | Path of `mkdocs.yml` |
| `submodules` | string | `false` | `false`, `true` or `recursive`: submodules checked out with the repository |
| `submodule_paths` | string | empty | Space-separated submodule paths initialised (shallow) after checkout, nested ones included; each parent on the way is initialised without recursion. Prefer it to `recursive` when the checks need a few nested submodules |
| `check_commands` | string | figkit and gen.py checks | Shell lines run before the build; the default runs `tools/figkit/build.py --check` and `tools/docs/gen.py --check` when they exist |
| `doxygen_config` | string | empty | Doxyfile of the API reference; empty builds no API |
| `doxygen_working_directory` | string | `.` | Directory Doxygen runs in |
| `doxygen_html_dir` | string | empty | Generated HTML directory; empty reads `OUTPUT_DIRECTORY` / `HTML_OUTPUT` from the Doxyfile |
| `api_dir` | string | `api` | Site folder for the Doxygen HTML (same as `extra.api_dir` in `mkdocs.yml`) |
| `link_check` | boolean | `true` | Run lychee offline on the built site, API included |
| `link_check_args` | string | empty | Extra lychee arguments (for example `--exclude-path`) |
| `deploy` | boolean | `false` | Publish; ignored on pull requests |
| `deployment_branch` | string | `gh-pages` | Branch GitHub Pages serves |
| `dev_version` | string | `dev` | Version a push to the default branch publishes |
| `latest_alias` | string | `latest` | Alias moved to each release |

## Example

```yaml
name: Docs

on:
  push:
    branches: [main]
    tags: ["v*"]
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
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-mkdocs-publish.yml@main
    permissions:
      contents: write
    with:
      submodule_paths: lib/core/hf-core-drivers/internal/hf-pincfg
      doxygen_config: _config/Doxyfile
      deploy: ${{ vars.ENABLE_GITHUB_PAGES_DEPLOY == 'true' }}
```

## After the first publish

GitHub Pages must serve the `gh-pages` branch from `/` (repository **Settings, Pages, Build and deployment**:
source *Deploy from a branch*, branch `gh-pages`, folder `/`). The workflow never changes repository settings.
