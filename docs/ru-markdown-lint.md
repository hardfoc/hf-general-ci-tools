# ru-markdown-lint

Lint Markdown with markdownlint-cli2 against the repository's own rules.

`ru-markdown-lint.yml` runs [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) over `globs`
with `config_file`. The HardFOC layout keeps the rules in `_config/.markdownlint.json`; a site on the documentation
platform allows the theme's HTML and indented admonition bodies (`MD033`, `MD046` and `MD041` off).

## What it does

| Mode | How | Exclusions |
| --- | --- | --- |
| Default (`use_docker: false`) | The official markdownlint-cli2 action | Through the config file's `ignores` |
| `use_docker: true` | markdownlint-cli2 in a container, file list filtered first | `exclude_patterns` (substring match) as well |

With `fix: true` the linter rewrites what it can fix, in the job's checkout only; nothing is committed. Outputs:
`result`, `files_checked`, `issues_found`.

## Caller

```yaml
jobs:
  markdown:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-markdown-lint.yml@v1
    permissions:
      contents: read
    with:
      config_file: _config/.markdownlint.json
```

## Jobs and permissions

<!-- generated: jobs-ru-markdown-lint -->
| Job | Permissions | Steps |
| --- | --- | --- |
| `markdownlint` (Markdown Lint) | `contents: read` | Checkout code; Run markdownlint (Official Action - Simple); Process results (Official Action); Run markdownlint (Docker - Full Control with Excludes); Consolidate outputs |
<!-- /generated -->

## Inputs

<!-- generated: inputs-ru-markdown-lint -->
| Input | Type | Default | Description |
| --- | --- | --- | --- |
| `globs` | string | `**/*.md` | Space-separated list of glob patterns to check (default: all markdown files) |
| `config_file` | string | `_config/.markdownlint.json` | Path to markdownlint configuration file (default: _config/.markdownlint.json) |
| `exclude_patterns` | string | `.git/**,node_modules/**,venv/**,.venv/**,_site/**,**/hf-espidf-project-tools/**` | Comma-separated patterns to exclude from checking |
| `use_docker` | boolean | `false` | Use Docker container instead of official action (for more control) |
| `fix` | boolean | `false` | Automatically fix fixable issues (equivalent to --fix flag) |
| `separator` | string | empty | Separator to use between glob patterns (default: space) |
<!-- /generated -->

## When it fails

| Symptom | Cause | Fix |
| --- | --- | --- |
| `MD033` on every page of a documentation site | Material components are HTML | Turn `MD033` off, or allow the theme's elements |
| `MD046` on admonitions | Admonition bodies are indented | Turn `MD046` off |
| Files in a submodule or build folder are linted | The default glob is `**/*.md` | Add them to the config's `ignores`, or use `use_docker` with `exclude_patterns` |
