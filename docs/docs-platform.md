# Documentation platform

The pieces every HardFOC documentation site is built from, where each one lives, and how a repository uses them.

## The pieces

| Piece | Where | What it gives a repository |
| --- | --- | --- |
| Theme package | [`packages/hardfoc-mkdocs-theme`](../packages/hardfoc-mkdocs-theme/README.md) | `theme: hardfoc` (brand, layout, components, light and dark), `plugins: [hardfoc]` (Markdown dialect, validation, repository links, figures, page checks), figkit, the `hardfoc-docs` command and the pinned toolchain |
| Publish workflow | [`ru-mkdocs-publish.yml`](ru-mkdocs-publish.md) | Strict build, drift checks, Doxygen under `api/`, offline link check, Lighthouse budget, screenshots, publish with mike or at the branch root |
| Template | [`templates/mkdocs-site`](../templates/mkdocs-site/mkdocs.yml) | The skeleton of a driver site; the self-CI builds it |
| Migration tool | [`tools/docs-migrate.py`](../tools/docs-migrate.py) | The mechanical move from Jekyll, with a `--check` dry run |
| Guides | [Migrating to MkDocs](MIGRATING-TO-MKDOCS.md), [Style guide](DOCS-STYLE-GUIDE.md) | The procedure, and what the pages contain |

A repository carries no CSS, templates, hooks or requirements file for its site. The workflow installs the theme
package from its own commit, so a caller pinned to `@v1` builds with the theme released in `v1`.

## A site in three files

```yaml title="mkdocs.yml"
site_name: TMC9660 Driver
site_description: One sentence on what this is.
repo_url: https://github.com/hardfoc/hf-tmc9660-driver

theme:
  name: hardfoc

plugins:
  - hardfoc
  - search
  - awesome-nav
```

`docs/.nav.yml` orders the pages; `.github/workflows/ci-docs-publish.yml` calls the workflow
([Quickstart](quickstart.md#documentation)). The plugin fills in the rest: `site_url`, `repo_name`, `edit_uri`, the
Markdown extensions, strict validation and the version selector.

## Versioned and unversioned sites

| | Versioned (every repository) | Unversioned (the portal, `hardfoc.github.io`) |
| --- | --- | --- |
| Addresses | `https://hardfoc.github.io/<repo>/<version>/`, root redirects to `latest/` | `https://hardfoc.github.io/` |
| Push to `main` | Publishes `dev` (also `latest` until the first release) | Replaces the site on `gh-pages` |
| Tag `vX.Y.Z` | Publishes `vX.Y.Z`, moves `latest` | Nothing |
| Selector | Version selector in the header, banner on old versions | None |
| Set by | Default | `versioning: false` on the workflow; the plugin knows `<org>.github.io` by itself |

## The `hardfoc-docs` command

| Command | Does |
| --- | --- |
| `hardfoc-docs figures [--check]` | Builds (or checks) the figkit figures under `docs/diagrams/figures/` |
| `hardfoc-docs gen [--check]` | Fills (or checks) `<!-- generated: name -->` regions; repository generators live in `tools/docs/generators/` |
| `hardfoc-docs check` | Both checks, as CI runs them |
| `hardfoc-docs screenshots SITE OUT` | Phone and desktop screenshots, light and dark (needs the `[screenshots]` extra) |
| `hardfoc-docs publish-root SITE` | Commits a built site as the whole deployment branch (unversioned sites) |

This site uses a generator itself: [`tools/docs/generators/workflows.py`](../tools/docs/generators/workflows.py)
writes the catalogue, the permissions table and every inputs and jobs table from the workflow files.

## Preview a site locally

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install "git+https://github.com/hardfoc/hf-general-ci-tools@v1#subdirectory=packages/hardfoc-mkdocs-theme"
mkdocs serve                       # http://127.0.0.1:8000
mkdocs build --strict -d /tmp/site # what CI runs
lychee --offline --include-fragments --index-files index.html --root-dir /tmp/site '/tmp/site/**/*.html'
```

## Sites that copied the earlier template

`hf-hal-flux-v1` and `hf-hal-vortex-v1` started from an earlier template that copied `overrides/`,
`docs/stylesheets/hardfoc.css`, `tools/docs/` and `tools/figkit/` into the repository. To move such a site onto
the package:

1. Set `theme: {name: hardfoc}` and `plugins: [hardfoc, search, awesome-nav]`.
2. Delete the copies and `requirements-docs.txt`.
3. Change figure modules to `from hardfoc_mkdocs_theme.figkit import Fig`.
4. Move repository-specific generators to `tools/docs/generators/`; they run under `hardfoc-docs gen`.

Next: [Migrating to MkDocs](MIGRATING-TO-MKDOCS.md).
