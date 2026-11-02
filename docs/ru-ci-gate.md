---
layout: default
title: "✅ CI Gate"
description: "One required status check that passes only when every CI job passed"
nav_order: 9
parent: "🔄 Reusable Workflows"
permalink: /docs/ru-ci-gate/
---

# ✅ CI Gate (Reusable)

`ru-ci-gate.yml` turns the results of all jobs in a workflow into a single
check. A repository's ruleset then requires that one check instead of a list
of job names that has to be updated whenever jobs are added, renamed or split.

## Caller pattern

Add the gate as the **last** job of the CI workflow:

```yaml
jobs:
  build:
    # ...
  lint:
    # ...
  docs:
    # ...

  ci-gate:
    name: CI gate
    needs: [build, lint, docs]   # every other job in this workflow
    if: always()                 # required, see below
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-ci-gate.yml@v1
    permissions:
      contents: read
    with:
      needs_json: ${{ toJSON(needs) }}
      allow_skipped: docs        # optional: jobs that may be skipped
```

Then, in the repository ruleset (or branch protection), require **only** the
status check named:

```text
CI gate / gate
```

GitHub names checks from a called workflow `<calling job name> / <called job
name>`, so with `name: CI gate` on the calling job the check is always
`CI gate / gate`, in every repository.

## Rules

The gate passes if and only if every job in `needs` finished with `success`,
or with `skipped` and is listed in `allow_skipped`. `failure`, `cancelled`,
and an unlisted `skipped` all fail it.

- **`if: always()` is required.** Without it, a failing job causes the gate to
  be skipped, and a skipped required check counts as **passing**.
- **Every job must be in `needs`.** A job outside `needs` can fail without
  failing the gate.
- With `verify_needs: true` (the default) the gate reads the calling workflow
  file and fails if either rule above is broken. It also fails if
  `allow_skipped` names a job that is not in `needs`, which catches typos.

## Inputs

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `needs_json` | string | ✅ | | Pass `${{ toJSON(needs) }}` |
| `allow_skipped` | string | ❌ | `""` | Job ids that may be skipped (comma, space or newline separated) |
| `verify_needs` | boolean | ❌ | `true` | Check the calling workflow for missing `needs` and `if: always()` |

## Permissions

`contents: read`, used to read the calling workflow file.

## Jobs that run conditionally

A job that is skipped by design, for example a deploy job that runs only on
`main`, goes in `allow_skipped`. A job that is skipped because something it
needs failed is reported as `skipped` too. That case is still caught: the
failed upstream job is itself in `needs`, so the gate fails on it.
