# How this repository tests itself

The checks every pull request to this repository runs, and what each one proves.

## Workflows

| Workflow | Job | What it checks |
| --- | --- | --- |
| [`ci-self.yml`](https://github.com/hardfoc/hf-general-ci-tools/blob/main/.github/workflows/ci-self.yml) | `actionlint` | actionlint with shellcheck, both pinned and verified by SHA-256; any finding fails |
| | `workflow-checks` | The [`&&` tail rule](permissions.md#the-no-bare--tail-rule), the [permissions contract](permissions.md), the README inputs tables, unit tests of these scripts, and, on pull requests, breaking changes against the base branch |
| | `docs-platform` | Unit tests of the theme package; the template site builds strictly with current figures; the migration tool turns a Jekyll fixture into a site that builds strictly |
| | `ci-gate` | This repository's own [CI gate](ru-ci-gate.md); the required check is `CI gate / gate` |
| [`ci-docs-publish.yml`](https://github.com/hardfoc/hf-general-ci-tools/blob/main/.github/workflows/ci-docs-publish.yml) | `docs` | This site, through [`ru-mkdocs-publish`](ru-mkdocs-publish.md) at the same commit, published on `main` |
| | `selftest-mkdocs-unversioned` | `ru-mkdocs-publish` with `versioning: false` on the organisation-site fixture |
| | `selftest-site-in-subdir` | The legacy [`ru-docs-publish`](ru-docs-publish.md) on a Jekyll site in a subdirectory |
| [`ci-host-ci.yml`](https://github.com/hardfoc/hf-general-ci-tools/blob/main/.github/workflows/ci-host-ci.yml) | | `ru-host-ci` on a fixture: the preset path on clean code passes; the `-S`/`-B` path with seeded defects reports findings |
| [`ci-docs-linkcheck.yml`](https://github.com/hardfoc/hf-general-ci-tools/blob/main/.github/workflows/ci-docs-linkcheck.yml) | `selftest-own-site` | `ru-docs-linkcheck` skips the repository's own unpublished Pages site |
| `ci-cpp-lint.yml`, `ci-cpp-analysis.yml`, `ci-markdown-lint.yml`, `ci-yaml-lint.yml` | | Each reusable lint workflow on this repository |

## Scripts

| Script | Run by | Fails when |
| --- | --- | --- |
| `.github/scripts/check_run_tails.py` | `workflow-checks` | A `run:` block ends in a bare `cond && cmd` |
| `.github/scripts/check_permissions.py` | `workflow-checks` | The permissions of a workflow differ from the README table |
| `.github/scripts/gen_readme_inputs.py --check` | `workflow-checks` | A README inputs table differs from its workflow |
| `.github/scripts/check_contract.py` | `workflow-checks` (pull requests) | A breaking change has no `### Breaking` entry |
| `hardfoc-docs check` | `docs` | A table on this site differs from the workflows it is read from |

## Actions and updates

Third-party actions are pinned to full commit SHAs with a `# vX.Y.Z` comment. Dependabot proposes updates to them
and to the theme package's pinned toolchain.

## Run the checks locally

```bash
python3 -m pip install PyYAML==6.0.2 ./packages/hardfoc-mkdocs-theme
python3 .github/scripts/check_run_tails.py .github/workflows/*.yml
python3 .github/scripts/check_permissions.py
python3 .github/scripts/gen_readme_inputs.py --check
python3 .github/scripts/test_checks.py
(cd packages/hardfoc-mkdocs-theme && python3 -m unittest discover -s tests)
hardfoc-docs check && mkdocs build --strict
```
