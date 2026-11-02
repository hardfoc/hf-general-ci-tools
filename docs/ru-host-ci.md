---
layout: default
title: "🖥️ Host CMake CI"
description: "Configure, build and test a CMake project on the host, then run clang-tidy and cppcheck on its compilation database"
nav_order: 10
parent: "🔄 Reusable Workflows"
permalink: /docs/ru-host-ci/
---

# 🖥️ Host CMake CI (Reusable)

`ru-host-ci.yml` runs the native (host) half of a C/C++ project's CI in one
job:

1. **Configure.** Uses `cmake --preset <preset>` when `preset` is set, otherwise
   `cmake -S <source_dir> -B <build_dir> -G Ninja`. Either way it passes
   `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`.
2. **Build.** Runs `cmake --build <build_dir> --parallel`.
3. **Test.** Runs `ctest --test-dir <build_dir> --output-on-failure`.
4. **Select files.** Picks translation units from `compile_commands.json`.
   A unit is analysed if its path relative to the repository root matches
   `tidy_paths`. Units that match `exclude_paths` and anything generated in
   the build tree are dropped. The selection is written as a filtered
   database, so both analysers see exactly the same files.
5. **Analyse.** Runs **clang-tidy 18** (`-p <build_dir>`) and **cppcheck**
   (`--project=<filtered database>`) on that set. Both see the include paths
   and defines the compiler sees, so no configuration is guessed.
6. **Report.** Findings appear as annotations. The reports, the file list and
   the database are uploaded as an artifact. With `fail_on_findings: true`
   (the default), any finding fails the job.

clang-tidy exits 0 even when it prints warnings, so the workflow counts
`file:line:col: warning|error: ... [check]` lines itself. It ignores compiler
warnings echoed as `clang-diagnostic-*`, except `clang-diagnostic-error`.
cppcheck findings are lines of severity error, warning, performance,
portability or style; `information` lines (analysis limits) do not count.

## Minimal caller

```yaml
jobs:
  host:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-host-ci.yml@v1
    permissions:
      contents: read
    with:
      preset: host-debug
      build_dir: build/host-debug           # the preset's binaryDir, from the repo root
      tidy_paths: "^(src|include|apps)/"
      cppcheck_suppressions: tools/lint/cppcheck-suppressions.txt
```

## Inputs

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `preset` | string | `""` | Configure preset from `<source_dir>/CMakePresets.json`; empty uses `-S/-B` |
| `source_dir` | string | `.` | CMake source directory |
| `build_dir` | string | `build/host` | Build directory; with a preset, the preset's `binaryDir` (relative to the repository root) |
| `cmake_args` | string | `""` | Extra configure arguments |
| `build_type` | string | `Debug` | `CMAKE_BUILD_TYPE` when no preset is used |
| `run_tests` | boolean | `true` | Run ctest |
| `ctest_args` | string | `""` | Extra ctest arguments |
| `tidy_paths` | string | `""` | Python regex (search) on repository-relative paths; empty selects every unit |
| `exclude_paths` | string | `(^\|/)(third_party\|external\|vendor\|_deps)/` | Python regex; matching units are not analysed and findings in matching files do not count |
| `run_clang_tidy` | boolean | `true` | Run clang-tidy 18 |
| `clang_tidy_config` | string | `""` | `--config-file` for clang-tidy; empty uses the usual `.clang-tidy` lookup |
| `run_cppcheck` | boolean | `true` | Run cppcheck |
| `cppcheck_suppressions` | string | `""` | `--suppressions-list` file |
| `cppcheck_enable` | string | `warning,performance,portability` | `--enable` value |
| `fail_on_findings` | boolean | `true` | Fail when either analyser reports a finding |
| `apt_packages` | string | `""` | Extra apt packages (for example a library the build needs) |
| `submodules` | string | `false` | `actions/checkout` submodules value |
| `runs_on` | string | `ubuntu-24.04` | Runner label |
| `artifact_name` | string | `host-ci-reports` | Report artifact name |

Outputs: `tidy_findings` and `cppcheck_findings`, the counts of findings
(empty when a tool did not run).

## Permissions

`contents: read`.

## Self-test

`ci-host-ci.yml` runs the workflow twice on `tests/fixtures/host-ci`:

- with the preset on clean code, where it must pass with `fail_on_findings: true`
  (the vendored file with a defect is excluded by the default `exclude_paths`);
- through `-S/-B` with seeded defects, where both analysers must report findings.
