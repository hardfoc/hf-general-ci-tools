---
hide:
  - navigation
  - toc
---

<div class="hf-hero" markdown>
<span class="hf-kicker">HardFOC CI and documentation platform</span>

# General CI Tools

<p>Reusable GitHub Actions workflows that every HardFOC repository calls: C/C++ lint and analysis, host builds and
tests, the documentation platform, link and lint checks, releases, and one required CI gate. Callers pin
<code>@v1</code> and get fixes without breaking changes.</p>

[Quickstart](quickstart.md){ .md-button .md-button--primary }
[Workflow catalogue](workflows.md){ .md-button }
[Source on GitHub](https://github.com/hardfoc/hf-general-ci-tools){ .md-button }
</div>

A repository keeps a few short caller workflows; the jobs, the pinned tools and the checks live here. Every
third-party action is pinned to a commit SHA, so `@v1` pins everything a caller runs.

## What you get

- **One required check.** [`ru-ci-gate`](ru-ci-gate.md) turns every job of a workflow into `CI gate / gate`.
- **C++ checks that agree with the compiler.** [`ru-host-ci`](ru-host-ci.md) builds, runs ctest, then
  clang-tidy 18 and cppcheck over the same compile database.
- **The documentation platform.** [`ru-mkdocs-publish`](ru-mkdocs-publish.md) builds a site with the shared theme
  in [`packages/hardfoc-mkdocs-theme`](https://github.com/hardfoc/hf-general-ci-tools/tree/main/packages/hardfoc-mkdocs-theme),
  checks it, audits it and publishes it, versioned or not ([platform guide](docs-platform.md)).
- **Releases without breaking callers.** Semver tags, a moving `v1`, an automatic patch release on every merge,
  and a check that stops a breaking change from landing without a major ([Versioning](VERSIONING.md)).
- **A permissions contract.** Each workflow asks for the least it needs, per job, and the self-CI holds it to
  the [documented table](permissions.md).

## Workflows

<!-- generated: workflow-catalogue -->
| Workflow | Purpose | Permissions |
| --- | --- | --- |
| [`ru-ci-gate.yml`](ru-ci-gate.md) | One required status check per repository: it passes only when every other CI job passed. | `contents: read` |
| [`ru-cpp-analysis.yml`](ru-cpp-analysis.md) | Run cppcheck over source folders, without a build, and keep the report as an artifact. | `contents: read` |
| [`ru-cpp-lint.yml`](ru-cpp-lint.md) | Check C and C++ formatting with clang-format and lint with clang-tidy, with results as annotations on the pull request. | `contents: read`, `pull-requests: write` |
| [`ru-docs-linkcheck.yml`](ru-docs-linkcheck.md) | Check every link in a repository's Markdown, external ones included, with lychee. | `contents: read` |
| [`ru-docs-publish.yml`](ru-docs-publish.md) | Build a Jekyll site with Doxygen and publish it to `gh-pages` in version folders: the documentation pipeline that [`ru-mkdocs-publish`](ru-mkdocs-publish.md) replaces. | `contents: write` |
| [`ru-host-ci.yml`](ru-host-ci.md) | Build, test and analyse a CMake project on the host, with clang-tidy 18 and cppcheck over the compiler's own compile database. | `contents: read` |
| [`ru-markdown-lint.yml`](ru-markdown-lint.md) | Lint Markdown with markdownlint-cli2 against the repository's own rules. | `contents: read` |
| [`ru-mkdocs-publish.yml`](ru-mkdocs-publish.md) | Build, check, audit and publish a HardFOC documentation site with the shared theme, versioned or not. | `contents: write` |
| [`ru-release.yml`](ru-release.md) | Create a GitHub Release with generated notes for a tag. | `contents: write` |
| [`ru-yaml-lint.yml`](ru-yaml-lint.md) | Lint YAML files with yamllint against the repository's own rules. | `contents: read` |
<!-- /generated -->

<div class="grid cards" markdown>

-   **[Quickstart](quickstart.md)**

    The smallest CI for a repository: one workflow, the gate, pinned to `@v1`.

-   **[Versioning](VERSIONING.md)**

    Tags, the moving major, what counts as breaking, automatic patch releases.

-   **[Permissions contract](permissions.md)**

    What each workflow needs from its caller, and why a missing grant fails before any job runs.

-   **[Docs platform](docs-platform.md)**

    The theme package, the publish workflow, the migration tool and the style guide.

-   **[Workflow catalogue](workflows.md)**

    One page per workflow: what it does, jobs, permissions, inputs and failure modes.

-   **[How this repository tests itself](self-ci.md)**

    Self-CI, contract checks and the fixtures every change runs against.

</div>
