# Quickstart

Add CI to a HardFOC repository: one workflow file that calls the reusable workflows at `@v1` and ends with the gate.

## One workflow, one required check

Put every job in `.github/workflows/ci.yml`. Each job calls one reusable workflow and grants exactly the permissions
that workflow needs ([Permissions contract](permissions.md)). The last job is the gate.

```yaml title=".github/workflows/ci.yml"
name: CI

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  host:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-host-ci.yml@v1
    permissions:
      contents: read
    with:
      preset: host-debug
      build_dir: build/host-debug

  markdown:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-markdown-lint.yml@v1
    permissions:
      contents: read

  ci-gate:
    name: CI gate
    needs: [host, markdown]        # every other job in this workflow
    if: always()                   # a skipped required check counts as passing
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-ci-gate.yml@v1
    permissions:
      contents: read
    with:
      needs_json: ${{ toJSON(needs) }}
```

Then require only the check `CI gate / gate` in the repository ruleset. Adding, renaming or splitting jobs later
needs no change to the ruleset; the gate fails if a job is missing from its `needs`.

## Documentation

The documentation site has its own workflow, because it publishes on `main` and on tags:

```yaml title=".github/workflows/ci-docs-publish.yml"
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

jobs:
  docs:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-mkdocs-publish.yml@v1
    permissions:
      contents: write  # the publish job pushes gh-pages; pull requests never publish
    with:
      doxygen_config: Doxyfile
      deploy: true
```

[Migrating to MkDocs](MIGRATING-TO-MKDOCS.md) sets up `mkdocs.yml` and `docs/` for it.

## When a run fails

| Symptom | Cause | Fix |
| --- | --- | --- |
| `startup_failure`, no job started | The calling job grants less than the workflow needs | Grant the permissions in the [contract](permissions.md) |
| `startup_failure` after an upgrade to a new major | An input was removed or made required | Read the `### Breaking` notes in the [changelog](changelog.md) |
| The gate fails with "not in needs" | A job was added without adding it to the gate's `needs` | Add it to `needs` |
| A fix merged here does not reach a re-run | "Re-run failed jobs" reuses the revision of the first run | Start a new run (push, **Run workflow**, or reopen the pull request) |

Next: [Versioning](VERSIONING.md).
