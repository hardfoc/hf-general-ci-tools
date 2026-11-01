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

Everything below becomes **v1.0.0**, the first tagged release. Until callers
move from `@main` to `@v1`, `@main` stays compatible with them: no input has
been removed and no workflow needs more permissions than before.

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
