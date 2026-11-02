# ru-yaml-lint

Lint YAML files with yamllint against the repository's own rules.

`ru-yaml-lint.yml` installs yamllint and runs it on every file matched by `paths` (comma-separated globs) that is
not excluded by `exclude_patterns`, with `config_file` when it exists (yamllint's defaults otherwise).

## What it does

1. Expands each glob in `paths` (with `**`), or finds matching files when the glob matches nothing.
2. Drops files whose path contains one of `exclude_patterns`.
3. Runs yamllint on each file, with `--strict` when `strict_mode` is set, so warnings fail too.
4. Fails when any file has errors (or warnings, in strict mode). Outputs: `result`, `files_checked`,
   `issues_found`.

## Caller

```yaml
jobs:
  yaml:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-yaml-lint.yml@v1
    permissions:
      contents: read
    with:
      config_file: _config/.yamllint
```

## Jobs and permissions

<!-- generated: jobs-ru-yaml-lint -->
| Job | Permissions | Steps |
| --- | --- | --- |
| `yamllint` (YAML Lint) | `contents: read` | Checkout code; Install yamllint; Run yamllint |
<!-- /generated -->

## Inputs

<!-- generated: inputs-ru-yaml-lint -->
| Input | Type | Default | Description |
| --- | --- | --- | --- |
| `paths` | string | `**/*.yml,**/*.yaml` | Comma-separated list of paths to check (default: all YAML files) |
| `config_file` | string | `_config/.yamllint` | Path to yamllint configuration file (default: _config/.yamllint) |
| `strict_mode` | boolean | `false` | Enable strict mode (fail on warnings) |
| `exclude_patterns` | string | `.git/**,node_modules/**,venv/**,.venv/**,**/hf-espidf-project-tools/**` | Comma-separated patterns to exclude from checking |
<!-- /generated -->

## When it fails

| Symptom | Cause | Fix |
| --- | --- | --- |
| `truthy` on `on:` in workflows | yamllint's default `truthy` rule | Allow `on` in the config (`truthy: {allowed-values: ['true', 'false', 'on']}`) |
| Line length on long descriptions | The default limit is 80 | Set `line-length` in the config |
| Files of a submodule are linted | The default glob is `**/*.yml,**/*.yaml` | Add the folder to `exclude_patterns` |
