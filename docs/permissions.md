# Permissions contract

What each reusable workflow needs from its caller, and the rules that keep that list true.

## Why it matters

A called workflow cannot have more permissions than its caller grants. When a job of a reusable workflow asks for
more, GitHub refuses the whole run before any job starts (`startup_failure`), in every repository that calls it.
So a workflow here asks for the least it needs, per job, and the README and this page say exactly what that is.

## What each workflow needs

Grant at least the "Caller grants" column on the calling job, or at the top of the calling workflow. The table is
read from the workflow files.

<!-- generated: permissions-table -->
| Workflow | Caller grants | Job: permissions |
| --- | --- | --- |
| [`ru-ci-gate.yml`](ru-ci-gate.md) | `contents: read` | `gate`: `contents: read` |
| [`ru-cpp-analysis.yml`](ru-cpp-analysis.md) | `contents: read` | `cppcheck`: `contents: read` |
| [`ru-cpp-lint.yml`](ru-cpp-lint.md) | `contents: read`, `pull-requests: write` | `lint`: `contents: read`, `pull-requests: write` |
| [`ru-docs-linkcheck.yml`](ru-docs-linkcheck.md) | `contents: read` | `link-check`: `contents: read` |
| [`ru-docs-publish.yml`](ru-docs-publish.md) | `contents: write` | `input-validation`: none<br>`quality-checks`: `contents: read`<br>`version-detection`: `contents: read`<br>`build`: `contents: write` |
| [`ru-host-ci.yml`](ru-host-ci.md) | `contents: read` | `host`: `contents: read` |
| [`ru-markdown-lint.yml`](ru-markdown-lint.md) | `contents: read` | `markdownlint`: `contents: read` |
| [`ru-mkdocs-publish.yml`](ru-mkdocs-publish.md) | `contents: write` | `build`: `contents: read`<br>`quality`: `contents: read`<br>`deploy`: `contents: write` |
| [`ru-release.yml`](ru-release.md) | `contents: write` | `release`: `contents: write` |
| [`ru-yaml-lint.yml`](ru-yaml-lint.md) | `contents: read` | `yamllint`: `contents: read` |
<!-- /generated -->

## The rules

The self-CI (`check_permissions.py` in the `workflow contract checks` job) fails a pull request when:

| Rule | Why |
| --- | --- |
| A reusable workflow sets top-level `permissions:` | Permissions are per job, so a read-only job never holds a write token |
| A job of a reusable workflow has no `permissions:` mapping | It would inherit everything the caller granted |
| A workflow's job permissions differ from its row in the README table | More breaks callers; less means the table asks for too much |
| A reusable workflow has no row, or a row names no workflow | The table is the contract callers read |
| A caller in this repository grants less than the contract | The self-tests would hit `startup_failure` |

A new permission on an existing workflow is a breaking change: it needs a `### Breaking` entry in the changelog
and a new major ([Versioning](VERSIONING.md)).

## The "no bare `&&` tail" rule

GitHub runs `run:` blocks with `bash -e`, and a script's exit status is that of its last command. A last line such
as `[ -n "$X" ] && echo "..."` fails the step whenever the condition is false, although `-e` ignores the same line
anywhere else. `check_run_tails.py` fails any `run:` block that ends that way; write an `if ... fi` instead.

Next: [the workflow catalogue](workflows.md).
