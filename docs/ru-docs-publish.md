# ru-docs-publish (legacy)

Build a Jekyll site with Doxygen and publish it to `gh-pages` in version folders: the documentation pipeline that
[`ru-mkdocs-publish`](ru-mkdocs-publish.md) replaces.

!!! warning "Being replaced"
    New sites use [`ru-mkdocs-publish`](ru-mkdocs-publish.md). Repositories still on this workflow move with
    [Migrating to MkDocs](MIGRATING-TO-MKDOCS.md). This workflow keeps working for them under `@v1`.

## What it does

| Event | Path |
| --- | --- |
| `pull_request`, `pull_request_target`, `merge_group` | Build only: input validation, quality checks, Doxygen, the Jekyll build and the link check; the site is uploaded as the `docs-html` artifact (`artifact_name`). Never deploys, whatever `deploy_pages` says |
| Push to `main` | Builds and, with `deploy_pages: true`, publishes to `gh-pages/development/` |
| Push to `release/v*` or a `v*` tag | Builds and publishes to `gh-pages/vX.Y.Z/` |
| Other branches | Builds a `preview` version |

On `gh-pages`, each version folder holds the Jekyll site with the Doxygen HTML under `api/`; Doxygen output is
also kept under `doxs/<version>/`. The root `index.html` redirects to the newest release (or `development`), and
`version_selector.html` lists the versions. A single step, "Decide whether to deploy", decides whether anything is
published, and every deploy step reads it.

## Caller

```yaml
on:
  push:
    branches: [main]
  pull_request:

jobs:
  docs:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-publish.yml@v1
    permissions:
      contents: write   # required on pull requests too: GitHub checks every job's permissions before the run
    with:
      doxygen_config: _config/Doxyfile
      jekyll_enabled: true
      jekyll_source: "."
      jekyll_config: _config/_config.yml
      deploy_pages: true   # pull requests still never deploy
```

## Jobs and permissions

<!-- generated: jobs-ru-docs-publish -->
| Job | Permissions | Steps |
| --- | --- | --- |
| `input-validation` | none | Validate workflow inputs |
| `quality-checks` | `contents: read` | Checkout repository; Setup Node.js for quality tools; Cache pip dependencies; Install quality tools; Run YAML linting; Run markdown linting; Run spell checking |
| `version-detection` | `contents: read` | Checkout repository; Detect version and strategy |
| `build` | `contents: write` | Checkout repository; Check for Doxygen configuration; Install Doxygen (pinned version); Check for pre-installed Graphviz; Install Graphviz (Optimized); Setup Ruby (bundler cache); Setup Node.js; Resolve Doxygen HTML output directory; Cache pip dependencies; Cache Node.js dependencies; Cache Jekyll dependencies; Cache Doxygen build artifacts; Install Jekyll dependencies; Validate Jekyll configuration; Install Node.js tools; Install YAML linting tools; Generate Doxygen documentation with versioning; Stage Doxygen into Jekyll (if enabled); Manage Doxygen versioned artifacts; Quality checks summary; Caching status summary; Generate version-specific configuration; Build Jekyll site; Link check with Lychee; Prepare deployment artifacts; Upload documentation artifacts; Decide whether to deploy; Deploy Jekyll site to GitHub Pages; Deploy Doxygen artifacts to GitHub Pages; Update root redirect and version selector |
<!-- /generated -->

## Inputs

<!-- generated: inputs-ru-docs-publish -->
| Input | Type | Default | Description |
| --- | --- | --- | --- |
| `checkout_recursive` | boolean | `false` | Checkout submodules recursively (useful for projects with documentation in submodules) |
| `run_link_check` | boolean | `true` | Run documentation link checker |
| `link_check_paths` | string | `**/*.md` | Space-separated paths to check for broken links |
| `link_check_config` | string | empty | Path to lychee.toml config file (optional) |
| `verbose` | boolean | `false` | Enable verbose output for link checking |
| `yamllint_config` | string | `_config/.yamllint` | Path to yamllint configuration file |
| `run_markdown_lint` | boolean | `false` | Run markdown linting on documentation files |
| `markdown_lint_paths` | string | `**/*.md` | Glob patterns for markdown files to lint |
| `markdown_lint_config` | string | `_config/.markdownlint.json` | Path to markdownlint configuration file |
| `run_spell_check` | boolean | `false` | Run spell checking on documentation files |
| `spell_check_paths` | string | `**/*.md` | Glob patterns for files to spell check |
| `spell_check_config` | string | `.cspell.json` | Path to cspell configuration file |
| `deployment_branch` | string | `gh-pages` | Branch name for deployment (required for versioned documentation) |
| `deploy_pages` | boolean | `true` | Deploy to GitHub Pages. Ignored on pull_request, pull_request_target and merge_group events, which always take the PR build path (build and upload the docs-html artifact, no deploy). |
| `artifact_name` | string | `docs-html` | Name of the uploaded site artifact (set it when calling this workflow more than once in one run) |
| `doxygen_config` | string | `Doxyfile` | Path to Doxyfile (relative to repo root) - output directory auto-detected from OUTPUT_DIRECTORY and HTML_OUTPUT settings |
| `doxygen_working_directory` | string | `.` | Directory to execute Doxygen from (defaults to repository root). Relative paths in the Doxyfile are resolved against this directory. |
| `doxygen_fail_on_warnings` | boolean | `false` | Treat Doxygen warnings as errors in CI |
| `jekyll_enabled` | boolean | `false` | Enable Jekyll static site generation for enhanced documentation presentation |
| `jekyll_config` | string | `_config.yml` | Comma-separated list of Jekyll configuration files (e.g., "_config.yml,_config_prod.yml") |
| `jekyll_source` | string | `docs` | Jekyll source directory containing your site files |
| `jekyll_destination` | string | `_site` | Jekyll build destination directory for generated site |
| `jekyll_environment` | string | `production` | Jekyll environment (development, production, staging) - affects which config files are loaded |
| `jekyll_safe` | boolean | `true` | Run in safe mode (disables custom plugins, used by GitHub Pages) - CI Recommended |
| `jekyll_plugins_dir` | string | empty | Comma-separated list of plugin directories (--plugins option) |
| `jekyll_layouts_dir` | string | empty | Layout directory (--layouts option) |
| `jekyll_verbose` | boolean | `false` | Enable verbose output during Jekyll build - CI Recommended for debugging |
| `jekyll_strict_front_matter` | boolean | `true` | Cause build to fail if there is a YAML syntax error in front matter - CI Recommended |
| `jekyll_drafts` | boolean | `false` | Include draft posts in the build (useful for development) |
| `jekyll_future` | boolean | `false` | Include future-dated posts in the build |
| `jekyll_unpublished` | boolean | `false` | Include unpublished posts in the build |
| `jekyll_incremental` | boolean | `false` | Enable incremental builds for faster development (may cause issues in CI) |
| `jekyll_lsi` | boolean | `false` | Enable LSI (Latent Semantic Indexing) for related posts |
| `jekyll_limit_posts` | string | empty | Limit the number of posts to parse and publish |
| `jekyll_profile` | boolean | `false` | Enable profiling output to show build performance (reduces build time) |
| `jekyll_quiet` | boolean | `false` | Suppress normal output during Jekyll build (reduces debugging info) |
| `jekyll_trace` | boolean | `false` | Show full backtrace when an error occurs (debug only) |
<!-- /generated -->

## When it fails

| Symptom | Cause | Fix |
| --- | --- | --- |
| "Validate Jekyll configuration" fails | `jekyll_config` or `jekyll_source` points at nothing | Paths are relative to the repository root; the config may live in a subfolder of the source |
| The site has no styling | `baseurl` in `_config.yml` does not match `/<repo>` | Set `baseurl: "/<repo>"` without a trailing slash |
| Doxygen output folder missing | `OUTPUT_DIRECTORY`'s parent does not exist | The workflow creates it; check `doxygen_working_directory` |
| Nothing published from `main` | `deploy_pages` is false | Pass `deploy_pages: true` (or a repository-variable gate) |
