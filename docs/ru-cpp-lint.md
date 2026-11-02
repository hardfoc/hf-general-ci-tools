# ru-cpp-lint

Check C and C++ formatting with clang-format and lint with clang-tidy, with results as annotations on the pull
request.

`ru-cpp-lint.yml` runs [cpp-linter-action](https://github.com/cpp-linter/cpp-linter-action) with the repository's
own `.clang-format` and `.clang-tidy`. It needs no build: clang-tidy runs without a compile database, so it sees
headers and defines only as far as it can guess them. A repository with a CMake host build gets more exact
results from [`ru-host-ci`](ru-host-ci.md).

## What it does

1. Checks out the repository.
2. Links `clang_format_config` and `clang_tidy_config` to `.clang-format` and `.clang-tidy` at the root when they
   live elsewhere (the HardFOC layout keeps them in `_config/`). A missing file is a warning, not an error.
3. Lists the files it will lint (`git ls-files` with `extensions`, without `ignore`), so the log shows the scope.
4. Runs clang-format (`style: file`) and clang-tidy at `clang_version`, on every file or only on changed files and
   lines, with annotations, a step summary and, optionally, one thread comment on the pull request.

## Caller

```yaml
jobs:
  lint:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-cpp-lint.yml@v1
    permissions:
      contents: read
      pull-requests: write
    with:
      clang_format_config: _config/.clang-format
      clang_tidy_config: _config/.clang-tidy
      files_changed_only: true
```

## Jobs and permissions

<!-- generated: jobs-ru-cpp-lint -->
| Job | Permissions | Steps |
| --- | --- | --- |
| `lint` | `contents: read`, `pull-requests: write` | `actions/checkout`; Prepare clang configuration; Report C/C++ files to lint; Run C/C++ Linter |
<!-- /generated -->

`pull-requests: write` is for annotations and the thread comment. The caller grants it even with both turned off.

## Inputs

<!-- generated: inputs-ru-cpp-lint -->
| Input | Type | Default | Description |
| --- | --- | --- | --- |
| `clang_version` | string | `20` | Clang major version |
| `clang_format_config` | string | `_config/.clang-format` | Path to clang-format configuration file |
| `clang_tidy_config` | string | `_config/.clang-tidy` | Path to clang-tidy configuration file |
| `tidy_checks` | string | empty | clang-tidy checks (comma-separated glob patterns, use - prefix to disable) |
| `extensions` | string | `c,cpp,cc,cxx,h,hpp` | File extensions to check (comma-separated) |
| `ignore` | string | `build\|.git` | Files or directories to exclude from linting (pipe-separated) |
| `files_changed_only` | boolean | `false` | Only lint files that have been changed in the pull request |
| `lines_changed_only` | boolean | `false` | Only inspect lines that have changed in the pull request |
| `step_summary` | boolean | `true` | Add a summary of linting results to the workflow step summary |
| `file_annotations` | boolean | `true` | Display linting errors and warnings as file annotations in the GitHub UI |
| `thread_comments` | boolean | `false` | Post a single, collapsible thread comment in a pull request detailing all linting issues |
<!-- /generated -->

## When it fails

| Symptom | Cause | Fix |
| --- | --- | --- |
| `startup_failure` | The caller does not grant `pull-requests: write` | Grant it on the calling job |
| Every line of a file is reported by clang-format | The config was not found, so the default style was used | Check the `clang_format_config` path; the log says which file was linked |
| clang-tidy reports missing headers | No compile database: include paths are guessed | Use [`ru-host-ci`](ru-host-ci.md) for clang-tidy, keep this for formatting |
| Findings in vendored code | The folder is not in `ignore` | Add it, pipe-separated: `build\|.git\|third_party` |
