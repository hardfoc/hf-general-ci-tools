# Changelog

All notable changes to the reusable workflows in this repository are
documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and releases follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
as described in [docs/VERSIONING.md](docs/VERSIONING.md).

A change that breaks callers pinned to the current major goes under a
`### Breaking` heading in **Unreleased**, and the next release must then be a
major bump. Breaking means: a workflow or input removed, an input's type
changed, an input or secret made required, an output removed, or a job
needing a permission it did not need before. The self-CI
(`check_contract.py`) fails a pull request that makes such a change without
that heading.

## [Unreleased]

### Added (unversioned sites, link check)

- `ru-mkdocs-publish.yml`: `versioning` input (default `true`). `false` builds an unversioned site (the
  organisation portal) and publishes it from the default branch as the whole content of the deployment branch, at
  its root, in one ordinary commit; tags publish nothing. The custom domain comes from a `CNAME` file in the
  site (`docs/CNAME`), never from what the branch held before, so a stale `CNAME` cannot take the site over.
- Theme plugin: `versioned` option (unset: versioned, except `<org>.github.io`), overridden by
  `HARDFOC_DOCS_VERSIONED`; an unversioned site gets the Pages root as `site_url` and no version selector.
- `hardfoc-docs publish-root`: the publish step for unversioned sites, with unit tests against a scratch remote.
- `ru-docs-linkcheck.yml`: `exclude_own_site` (default `true`) skips links to the repository's own Pages site on
  pull requests and until its `latest/` answers, so a repository's first MkDocs pull request no longer fails on
  its own `/latest/` links.
- `ru-mkdocs-publish.yml`: `check_commands` run with `GH_TOKEN` set to the job's read-only token, so a site can
  generate pages from the GitHub API at build time (the organisation portal's repository catalogue).
- Theme: a filterable catalogue component (`.hf-filter` search field, `.hf-chipbtn` topic buttons, `.hf-repo`
  cards), used by the organisation portal's repository list.
- Theme package unit tests (`packages/hardfoc-mkdocs-theme/tests/`), run by the self-CI.

### Changed (documentation platform)

- This repository's documentation site is built with the platform itself (`ru-mkdocs-publish` at the same
  commit, `theme: hardfoc`): a quickstart, the workflow catalogue, one page per workflow with jobs, permissions and
  inputs generated from the YAML, the permissions contract, versioning, the platform guide and the self-CI. The
  Jekyll site files (`_config/_config.yml`, `_includes`, `_layouts`, `assets`) and the Jekyll-era guides are gone.
- Root `404.html` of versioned sites: a branded page (HardFOC mark, theme colours and font, light and dark) that
  says "Redirecting to the latest documentation" while `versions.json` loads, and shows "Page not found" with links
  only when no redirect applies, after two seconds, or without JavaScript.
- Theme: from tablet width up, tables fit the column (cells and code wrap) instead of cutting off the last column;
  on a phone, figures keep a readable size and scroll sideways instead of shrinking.

### Fixed (documentation platform)

- `hardfoc-docs screenshots` without `--page` crashed (`UnboundLocalError`).
- Theme plugin: a link from `docs/` to a repository file that does not exist was turned into a GitHub link that
  404s; it is now a warning, so `mkdocs build --strict` fails (a folder that is empty, a submodule not checked
  out, is not reported).
- `tools/docs-migrate.py`: the Doxyfile's `INPUT` and `USE_MDFILE_AS_MAINPAGE` no longer point at the README
  (sources plus `docs/_doxygen/mainpage.md`, written when missing), `CASE_SENSE_NAMES = NO`, a final newline
  always; the caller workflow is named `📚 Docs`; Material's `hide:` front matter is kept.
- Theme plugin: a link or figure marker written as inline code (an example on a page, such as
  ``[`x.hpp`](../inc/x.hpp)``) is left as it is instead of being rewritten or embedded.
- `hardfoc-docs gen` no longer fills regions in a folder with its own `mkdocs.yml` (a template or fixture inside
  the repository), which belong to that site.
- `ru-mkdocs-publish.yml`: a Doxyfile without a final newline no longer swallows the stylesheet line the workflow
  appends.

### Added (documentation platform)

- `packages/hardfoc-mkdocs-theme`: the HardFOC documentation theme as one pip package: `theme: hardfoc`
  (brand, header with the organisation crumb, footer, admonition / code / table / figure styles, hero, cards,
  chip and board card, Mermaid theming, light and dark), `plugins: [hardfoc]` (shared configuration, Markdown
  dialect with snippets, strict validation, the link / figure hooks, page checks for Jekyll leftovers and
  missing headings), figkit, `hardfoc-docs` (figures, generated regions, screenshots) and the pinned toolchain.
- `ru-mkdocs-publish.yml`: installs the theme from the workflow's own commit (`theme_ref` to override); a
  `quality` job with a Lighthouse budget (`lighthouse`, `lighthouse_budgets`) and phone / desktop screenshots
  (`screenshots`) as artifacts; `release_version` (tags publish `vX.Y.Z` by default); `prune_legacy` removes the
  pre-MkDocs site from `gh-pages` in the first publish commit; a root `404.html` that redirects old addresses;
  the HardFOC Doxygen stylesheet when a Doxyfile has none; Doxygen's output folder is created first.
- `tools/docs-migrate.py`: mechanical Jekyll-to-MkDocs migration of a repository, with `--check`.
- `docs/MIGRATING-TO-MKDOCS.md` and `docs/DOCS-STYLE-GUIDE.md`.
- Automatic patch release on every push to `main` (`release.yml`), unless Unreleased has a `### Breaking` section.

### Changed (documentation platform)

- `templates/mkdocs-site` is a driver skeleton on the theme package; it no longer copies CSS, overrides, hooks or
  figkit into a repository.
- `ru-mkdocs-publish.yml`: a `vX.Y.Z` tag publishes version `vX.Y.Z` (was `X.Y`; `release_version: minor` keeps
  the old behaviour). `requirements` is optional.

### Fixed

- `ru-docs-publish`: copy static assets kept next to the Jekyll config (for
  example `_config/assets/css/custom.css`) into the site source before the
  build. Jekyll skips underscore folders, so driver sites never received
  their custom CSS and JavaScript.
- `ru-docs-publish`: set the generated config's `url` to the publishing
  repository's Pages host, so canonical links and the sitemap stop pointing
  at an old owner.
- `ru-mkdocs-publish`: call the `mike` command; `python3 -m mike` fails because
  mike has no `__main__`, so every deploy step failed.
- `ru-docs-publish`: stop appending the version name to the site title; it
  made the sidebar title wrap. The version stays available as `version`.

## [1.1.0] - 2026-11-02

First release callers pin as `@v1` (v1.0.0 was cut before the platform work
below had landed). No input has been removed and no workflow needs more
permissions than before.

### Added

- `ru-ci-gate.yml`: one required check (`CI gate / gate`) that passes only if
  every needed job succeeded or is an allowed skip. It also verifies that the
  calling workflow lists every job in `needs` and runs the gate with
  `if: always()`.
- `ru-host-ci.yml`: host CMake configure (preset or `-S/-B`), build, ctest,
  and clang-tidy 18 and cppcheck on one file set selected from
  `compile_commands.json`.
- `ru-docs-publish.yml`: optional input `artifact_name`.
- `ru-docs-publish.yml`: pre-flight checks. just-the-docs `callouts` must be
  mappings with a `color`, and a Pages source set to "GitHub Actions" fails
  the deploy instead of leaving the site at 404.
- Self-CI (`ci-self.yml`): pinned actionlint and shellcheck, a check for
  `run:` blocks ending in a bare `cond && cmd`, the permissions contract
  check, the breaking-change check, and unit tests for these checks.
- Self-tests: `ci-docs-publish.yml` builds a site whose Jekyll source is a
  subdirectory, and `ci-host-ci.yml` runs the host workflow on a fixture.
- README permissions table: exactly what each caller must grant.
- `release.yml`: on a `vX.Y.Z` tag, creates a GitHub Release with generated
  notes and moves the `vX` major tag.
- Dependabot for GitHub Actions (weekly).

### Changed

- Every third-party action is pinned to a full commit SHA with a version
  comment. `softprops/action-gh-release` moves from v1 to v3.0.3, since the
  node16 runtime of v1 is no longer supported.
- Every reusable workflow declares minimal permissions per job, with no
  top-level `permissions`. In `ru-docs-publish.yml`, only the `build` job
  keeps `contents: write`.

### Fixed

- `ru-docs-publish.yml`: sites whose `jekyll_source` is a subdirectory
  failed with "No such file or directory - _config_generated.yml".
- `ru-docs-publish.yml`: the root-redirect step pushed to `gh-pages` from
  pull requests when `deploy_pages` was true. Pull requests now always take
  the build-only path.
- `ru-docs-publish.yml`: Doxygen failed when `OUTPUT_DIRECTORY` had a
  missing parent. The directory is now created first.
- `ru-docs-publish.yml`: `PAGES_REPO_NWO` and `JEKYLL_GITHUB_TOKEN` are set
  for jekyll-github-metadata ("No repo name found").
- `ru-docs-linkcheck.yml`: `fail_on_errors: false` still failed on broken
  links, and `verbose` never took effect. Both inputs were compared with the
  string `'true'`.
- `ru-markdown-lint.yml` (Docker path): the docker command was built as a
  string with literal quotes.
