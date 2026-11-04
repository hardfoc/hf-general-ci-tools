# ru-mkdocs-publish

Build, check, audit and publish a HardFOC documentation site with the shared theme, versioned or not.

`ru-mkdocs-publish.yml` builds a HardFOC documentation site with the shared theme, checks it, audits it and publishes it to `gh-pages` as
a versioned site with [mike](https://github.com/jimporter/mike), with the Doxygen API reference under `api/`.
[Migrating to MkDocs](MIGRATING-TO-MKDOCS.md) moves a repository onto it; the [style guide](DOCS-STYLE-GUIDE.md)
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

The caller grants `contents: write`, even one that never publishes (pull requests, `deploy: false`): GitHub checks
the permissions of every job of a called workflow before the run starts, whatever the job's `if`.

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

<!-- generated: inputs-ru-mkdocs-publish -->
| Input | Type | Default | Description |
| --- | --- | --- | --- |
| `python_version` | string | `3.12` | Python used to build the site. |
| `requirements` | string | `requirements-docs.txt` | Optional pip requirements file installed after the theme package (extra MkDocs plugins). Skipped when the file does not exist; the theme package already pins mkdocs, mkdocs-material, awesome-nav, pymdown and mike. |
| `theme_ref` | string | empty | Ref of hardfoc/hf-general-ci-tools to install the theme package from. Empty: the commit this workflow runs from, so the theme always matches the workflow. |
| `mkdocs_config` | string | `mkdocs.yml` | Path of the site configuration. A repository that keeps tool configuration out of its root passes _config/mkdocs.yml (with docs_dir: ../docs); the theme then takes the folder that holds docs_dir as the repository root (snippets, repository links, figures) and the check commands get it as HARDFOC_DOCS_CONFIG. |
| `submodules` | string | `false` | Submodules to check out with the repository: 'false', 'true' (top level) or 'recursive'. |
| `submodule_paths` | string | empty | Space-separated submodule paths to initialise (shallow) after checkout, nested ones included: each parent submodule on the way is initialised without recursion, e.g. 'lib/core/drivers/internal/pincfg'. Use it instead of 'recursive' when the checks need a few nested submodules. |
| `check_commands` | string | `if [ -f tools/figkit/build.py ]; then python3 tools/figkit/build.py --check; fi if [ -f tools/docs/gen.py ]; then python3 tools/docs/gen.py --check; fi if [ ! -f tools/figkit/build.py ] && [ ! -f tools/docs/gen.py ]; then hardfoc-docs check; fi` | Shell lines run before the build, with GH_TOKEN set to the job's read-only token (for commands that read the GitHub API); any failure fails the job. The default runs the figure drift check and the generated-region check (hardfoc-docs check), or a repository's own tools/figkit and tools/docs/gen.py when it still carries them. |
| `doxygen_config` | string | empty | Doxyfile for the API reference, relative to doxygen_working_directory. Empty: no API. |
| `doxygen_working_directory` | string | `.` | Directory Doxygen runs in; relative paths in the Doxyfile resolve against it. |
| `doxygen_html_dir` | string | empty | Directory of the generated HTML, relative to doxygen_working_directory. Empty: read OUTPUT_DIRECTORY and HTML_OUTPUT from the Doxyfile. |
| `api_dir` | string | `api` | Folder of the site that receives the Doxygen HTML (match extra.api_dir in mkdocs.yml). |
| `link_check` | boolean | `true` | Run lychee offline on the built site (internal links, anchors and images, API included). |
| `link_check_args` | string | empty | Extra lychee arguments, for example --exclude-path patterns. |
| `lighthouse` | boolean | `true` | Run Lighthouse on the built site (home page and the first navigation pages) against the budgets. |
| `lighthouse_budgets` | string | `performance=0.8 accessibility=0.95 best-practices=0.9 seo=0.9` | Minimum Lighthouse category scores (0-1, median of three runs, mobile emulation), space-separated category=score pairs. A score below its minimum fails the job. |
| `screenshots` | boolean | `true` | Capture the home page and the first navigation pages at 375 and 1280 px, light and dark (artifact). |
| `versioning` | boolean | `true` | true: a versioned site, published with mike (default branch -> dev_version, v* tag -> that version, with latest_alias moved to it). false: one unversioned site (the organisation portal), published from the default branch as the whole content of deployment_branch at its root (a custom domain only from a CNAME file in the site); tags publish nothing. The build tells the theme plugin which (HARDFOC_DOCS_VERSIONED), so site_url and the version selector match. |
| `deploy` | boolean | `false` | Publish to deployment_branch. Never happens on a pull_request event, whatever this says; callers usually pass a repository-variable gate here. |
| `deployment_branch` | string | `gh-pages` | Branch GitHub Pages serves from. |
| `dev_version` | string | `dev` | mike version name a push to the default branch publishes to. |
| `latest_alias` | string | `latest` | mike alias moved to each release (v* tag). |
| `release_version` | string | `tag` | Version name a v* tag publishes: 'tag' (the tag itself, vX.Y.Z) or 'minor' (X.Y, a patch release replaces the docs of its minor release). |
| `prune_legacy` | boolean | `true` | On publish, remove every top-level entry of the deployment branch that is not a mike version or alias (the old Jekyll / Doxygen site: development/, doxs/, html/, version_selector.html, ...), in the publish commit. Kept: versions.json, index.html, 404.html, .nojekyll, CNAME, robots.txt. |
<!-- /generated -->

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

### Configuration in `_config/`

A repository whose root holds only what GitHub and readers look for keeps the site configuration in `_config/`
with `docs_dir: ../docs` and passes its path:

```yaml
    with:
      mkdocs_config: _config/mkdocs.yml
      doxygen_config: _config/Doxyfile
```

The build, the drift checks (`HARDFOC_DOCS_CONFIG` is set from `mkdocs_config`), the pip cache key and mike all use
that path, and the theme takes the folder that holds `docs_dir` as the repository root, so snippets and repository
links are unchanged. Doxygen runs in `doxygen_working_directory` (default the root), so paths inside a
`_config/Doxyfile` stay relative to the root.

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

## When it fails

| Symptom | Cause |
| --- | --- |
| "Install the theme" fails | The caller pins a ref of hf-general-ci-tools without the theme package (older than `v1.1.0`) |
| The strict build fails | A warning: a broken link or anchor, a page missing from `.nav.yml`, Jekyll front matter, a page without `# Title`, an image without alt text, a link to a repository file that does not exist |
| Drift checks fail | A figure or generated table no longer matches the code: run `hardfoc-docs figures` / `hardfoc-docs gen` and commit |
| lychee fails | A broken link or anchor in the built site, the API reference included |
| Lighthouse fails | A score under budget; the `lighthouse-report` artifact names the audits |
| Old pages still served at the root | The first publish has not run yet, or `prune_legacy` is false |
| The site shows the README rendered by Jekyll | Pages serves a branch other than `gh-pages`, or **GitHub Actions** |
