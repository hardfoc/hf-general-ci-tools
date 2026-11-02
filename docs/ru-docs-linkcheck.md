# ru-docs-linkcheck

Check every link in a repository's Markdown, external ones included, with lychee.

`ru-docs-linkcheck.yml` runs [lychee](https://github.com/lycheeverse/lychee) over Markdown files in the
repository. It complements [`ru-mkdocs-publish`](ru-mkdocs-publish.md), whose link check runs offline on the built
site: this one also follows external links, and checks Markdown that is not part of a site (READMEs, examples).

## What it does

1. Checks out the repository, with submodules when `checkout_recursive` is set.
2. Works out the repository's own Pages site (`https://<owner>.github.io/<repo>/`) and leaves links to it out of
   the check on pull requests, where the pages a change links to are not published yet, and on other events while
   its `latest/` (the root, for `<owner>.github.io`) does not answer, as before a repository's first MkDocs
   publish. Turn this off with `exclude_own_site: false`.
3. Runs lychee over `paths` with the timeout, retries and exclusions set by the inputs, and a `lychee.toml` when
   `config_file` names one.

## Caller

```yaml
jobs:
  links:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-linkcheck.yml@v1
    permissions:
      contents: read
    with:
      paths: "docs/**/*.md *.md"
```

## Jobs and permissions

<!-- generated: jobs-ru-docs-linkcheck -->
| Job | Permissions | Steps |
| --- | --- | --- |
| `link-check` | `contents: read` | Checkout repository; Own documentation site; Link check with Lychee |
<!-- /generated -->

## Inputs

<!-- generated: inputs-ru-docs-linkcheck -->
| Input | Type | Default | Description |
| --- | --- | --- | --- |
| `checkout_recursive` | boolean | `false` | Checkout submodules recursively (useful for projects with documentation in submodules) |
| `paths` | string | `docs/** *.md **/docs/**` | Space-separated paths to check for broken links |
| `fail_on_errors` | boolean | `true` | Fail the workflow if broken links are found |
| `timeout` | string | `10` | Timeout in seconds for each link check |
| `max_retries` | string | `3` | Maximum number of retries per request |
| `retry_wait_time` | string | `1` | Minimum wait time in seconds between retries |
| `exclude_private` | boolean | `true` | Exclude private/internal links |
| `exclude_mail` | boolean | `true` | Exclude mailto links |
| `verbose` | boolean | `false` | Enable verbose output |
| `config_file` | string | empty | Path to lychee.toml config file (optional) |
| `exclude_own_site` | boolean | `true` | Skip links to this repository's own GitHub Pages site (https://<owner>.github.io/<repo>/) on pull requests, where the pages a change links to are not published yet, and on other events while the site's latest/ version (the root, for <owner>.github.io) does not answer yet, as before a repository's first MkDocs publish. |
<!-- /generated -->

## When it fails

| Symptom | Cause | Fix |
| --- | --- | --- |
| A link to the repository's own site under `/latest/` fails on `main` | The site answers, but the page is new and not published yet | It passes after the publish; or exclude that path in `lychee.toml` |
| A site that blocks bots answers 403 or 429 | Rate limits or bot protection | Exclude the host in `lychee.toml` |
| Links into a submodule fail | The submodule was not checked out | Set `checkout_recursive: true` |
| Intermittent timeouts | A slow host | Raise `timeout` or `max_retries` |
