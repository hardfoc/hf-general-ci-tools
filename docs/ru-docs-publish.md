---
layout: default
title: "📚 Documentation Publisher (Reusable)"
description: "Reusable workflow for documentation generation and GitHub Pages deployment"
nav_order: 3
parent: "🔄 Reusable Workflows"
---

# 📚 Documentation Publisher (Reusable)

**Workflow:** `ru-docs-publish.yml` → 📚 **[RU] Documentation Publisher**

A comprehensive reusable workflow for building and publishing documentation using multiple tools including Doxygen, Jekyll, and GitHub Pages. Supports complex documentation pipelines with link checking and artifact management.

---

## 📋 Overview

This reusable workflow (`ru-docs-publish.yml`) builds documentation using various tools (Doxygen, Jekyll, etc.) and optionally deploys it to GitHub Pages with comprehensive link checking and artifact management. It's designed for maximum flexibility to handle complex documentation workflows.

### ✨ **Live CI Example**
👀 See our comprehensive testing workflow: [`ci-docs-publish.yml`](../.github/workflows/ci-docs-publish.yml) which demonstrates **all features** of this reusable workflow by building and deploying this repository's documentation with full configuration options enabled.

## 📋 Table of Contents

- [Overview](#-overview)
- [Inputs](#-inputs)
- [Outputs](#-outputs)
- [Usage Examples](#-usage-examples)
- [Configuration](#-configuration)
- [GitHub Pages Setup](#-github-pages-setup)
- [Troubleshooting](#-troubleshooting)
- [Related Workflows](#-related-workflows)

## 🎯 Overview

**Purpose**: Generate and deploy versioned documentation with Doxygen and Jekyll integration

**Key Features**:
- **Versioned Documentation Architecture**: Automatic version detection and deployment
- **Doxygen + Graphviz integration** (optimized installation)
- **Jekyll static site generation** with enhanced presentation
- **Centralized Doxygen Management**: Single source of truth for all API versions
- **Smart Root Redirects**: Always redirects to latest/development version
- **Interactive Version Selector**: Beautiful UI for navigating between versions
- **Advanced link checking** with Lychee
- **Markdown linting** (markdownlint)
- **Spell checking** (cspell)
- **Modern GitHub Pages deployment** using peaceiris/actions-gh-pages
- **Concurrency control** and artifact storage
- **Fast dependency installation** using pre-built binaries

**Use Case**: Automated versioned documentation generation and deployment for C/C++ projects with
comprehensive versioning support

## 🏗️ Versioned Documentation Architecture

The workflow implements a sophisticated versioned documentation system that automatically manages
multiple versions of your documentation:

### **Directory Structure**
```
gh-pages branch:
├── .git/
├── README.md
├── index.html (redirect to latest/development)
├── version_selector.html (interactive version browser)
├── development/ (main branch docs from _site/)
│   ├── index.html          # From Jekyll _site/
│   ├── assets/             # From Jekyll _site/
│   ├── docs/               # From Jekyll _site/
│   ├── api/                # Copied from doxs/development/ (Jekyll-compatible)
│   └── version_info.json   # Created by workflow
├── v1.0.0/ (stable releases from _site/)
│   ├── index.html          # From Jekyll _site/
│   ├── assets/             # From Jekyll _site/
│   ├── docs/               # From Jekyll _site/
│   ├── api/                # Copied from doxs/v1.0.0/ (Jekyll-compatible)
│   └── version_info.json   # Created by workflow
└── doxs/ (centralized Doxygen artifacts)
    ├── v1.0.0/
    ├── development/
    ├── latest -> v1.0.0/
    ├── version_selector.js
    └── versions.json
```

### **Version Detection Strategy**
- **`main` branch** → `development` version
- **`release/v*` branches** → versioned releases (e.g., `v1.2.0`)
- **`v*` tags** → stable releases (e.g., `v1.2.0`)
- **Other branches** → `preview` version

### **Smart Root Redirects**
- **Stable releases**: Redirects to the specific version
- **Development**: Redirects to `development`
- **Preview**: Redirects to `development` as fallback

### **Interactive Version Selector**
- Beautiful, responsive UI for version navigation
- Shows version types (Development, Stable Release, Preview)
- Highlights current version
- Mobile-friendly design

### **Deployment Flow**

The deployment process follows this sequence:

1. **Build Phase**:
   - Jekyll generates static site in `_site/` directory
   - Doxygen generates API docs in centralized `/doxs/` directory
   - Quality checks run in parallel

2. **Deploy Phase**:
   - `peaceiris/actions-gh-pages` deploys `_site/` contents to `gh-pages/version/`
   - `peaceiris/actions-gh-pages` deploys `doxs/` contents to `gh-pages/doxs/`
   - Version metadata created in each deployed directory

3. **Update Phase**:
   - Root redirect updated to point to appropriate version
   - Version selector updated with all available versions
   - README updated with current deployment info

**Key Benefits**:
- ✅ **Direct Deployment**: Generated `_site` directory deployed directly to version folder
- ✅ **Preserved History**: All previous versions remain accessible
- ✅ **Centralized API**: Doxygen docs available at root level for all versions
- ✅ **Smart Navigation**: Root always redirects to appropriate version

## ⚙️ Inputs

### 📁 Repository Configuration

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `checkout_recursive` | boolean | ❌ | `false` | Checkout submodules recursively (for projects with docs in submodules) |

### 📚 Doxygen Configuration

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `doxygen_config` | string | ❌ | `Doxyfile` | Path to Doxyfile (relative to repo root) |
| `doxygen_working_directory` | string | ❌ | `.` | Directory to execute Doxygen from (relative to repo root). Relative paths in your Doxyfile are resolved from here. |
| `doxygen_fail_on_warnings` | boolean | ❌ | `false` | Treat Doxygen warnings as errors in CI |

> 💡 **Tip:** When your `Doxyfile` lives in a subdirectory (for example `docs/api/Doxyfile`) or assumes it will be executed from a specific folder, point `doxygen_config` to the file itself and set `doxygen_working_directory` to the directory you want Doxygen to run from. This keeps relative `INPUT` and `OUTPUT_DIRECTORY` values working exactly as they do locally.

### 🔗 Link Checking

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `run_link_check` | boolean | ❌ | `true` | Run documentation link checker |
| `link_check_paths` | string | ❌ | `**/*.md` | Space-separated paths to check for broken links |
| `link_check_config` | string | ❌ | `''` | Path to lychee.toml config file (optional) |
| `verbose` | boolean | ❌ | `false` | Enable verbose output for link checking |

### 📝 Documentation Quality

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `run_markdown_lint` | boolean | ❌ | `false` | Run markdown linting on documentation files |
| `markdown_lint_paths` | string | ❌ | `**/*.md` | Space-separated glob patterns for markdown files to lint |
| `yamllint_config` | string | ❌ | `_config/.yamllint` | Path to yamllint configuration file |
| `markdown_lint_config` | string | ❌ | `_config/.markdownlint.json` | Path to markdownlint configuration file |
| `run_spell_check` | boolean | ❌ | `false` | Run spell checking on documentation files |
| `spell_check_paths` | string | ❌ | `**/*.md` | Space-separated glob patterns for files to spell check |
| `spell_check_config` | string | ❌ | `.cspell.json` | Path to cspell configuration file |

> ℹ️ **Visibility:** The workflow lists every YAML and Markdown file that will be linted before running `yamllint` or `markdownlint`, making it easy to confirm what is being validated in CI logs.

### 🌐 Deployment

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `deploy_pages` | boolean | ❌ | `true` | Deploy to GitHub Pages |
| `deployment_branch` | string | ✅ | `gh-pages` | Branch name for deployment (required for versioned documentation) |

### 🎨 Jekyll Configuration

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `jekyll_enabled` | boolean | ❌ | `false` | Enable Jekyll static site generation |
| `jekyll_config` | string | ❌ | `_config.yml` | Comma-separated list of Jekyll configuration files |
| `jekyll_source` | string | ❌ | `docs` | Jekyll source directory containing your site files |
| `jekyll_destination` | string | ❌ | `_site` | Jekyll build destination directory for generated site |
| `jekyll_environment` | string | ❌ | `production` | Jekyll environment (development, production, staging) |

### ⚙️ Jekyll Advanced Options

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `jekyll_safe` | boolean | ❌ | `true` | Run in safe mode (disables custom plugins, used by GitHub Pages) |
| `jekyll_plugins_dir` | string | ❌ | `''` | Comma-separated list of plugin directories |
| `jekyll_layouts_dir` | string | ❌ | `''` | Layout directory |
| `jekyll_verbose` | boolean | ❌ | `false` | Enable verbose output during Jekyll build |
| `jekyll_strict_front_matter` | boolean | ❌ | `true` | Fail build on YAML syntax errors in front matter |
| `jekyll_drafts` | boolean | ❌ | `false` | Include draft posts in the build |
| `jekyll_future` | boolean | ❌ | `false` | Include future-dated posts in the build |
| `jekyll_unpublished` | boolean | ❌ | `false` | Include unpublished posts in the build |
| `jekyll_incremental` | boolean | ❌ | `false` | Enable incremental builds for faster development |
| `jekyll_lsi` | boolean | ❌ | `false` | Enable LSI (Latent Semantic Indexing) for related posts |
| `jekyll_limit_posts` | string | ❌ | `''` | Limit the number of posts to parse and publish |
| `jekyll_profile` | boolean | ❌ | `false` | Enable profiling output to show build performance |
| `jekyll_quiet` | boolean | ❌ | `false` | Suppress normal output during Jekyll build |
| `jekyll_trace` | boolean | ❌ | `false` | Show full backtrace when an error occurs |

## 📤 Outputs

| Output | Description |
|--------|-------------|
| Versioned Documentation | Deployed to `gh-pages/version/` directories |
| Centralized API Docs | Doxygen artifacts in `gh-pages/doxs/` directory |
| Root Navigation | Smart redirects and version selector |
| Version Metadata | `version_info.json` files in each deployed directory |
| GitHub Pages | Live documentation site (if enabled) |
| Artifacts | Uploaded documentation files for download |

## 🚀 Usage Examples

### Basic Usage

```yaml
jobs:
  docs:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-publish.yml@v1
    with:
      doxygen_config: _config/Doxyfile
      deployment_branch: gh-pages
```

### With Submodule Support

```yaml
jobs:
  docs:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-publish.yml@v1
    with:
      doxygen_config: _config/Doxyfile
      deployment_branch: gh-pages
      checkout_recursive: true  # Enable submodule checkout
```

### With Documentation Quality Checks

```yaml
jobs:
  docs:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-publish.yml@v1
    with:
      doxygen_config: _config/Doxyfile
      deployment_branch: gh-pages
      run_link_check: true
      link_check_paths: "docs/** *.md **/docs/**"
      run_markdown_lint: true
      markdown_lint_paths: "docs/** *.md"
      run_spell_check: true
      spell_check_paths: "docs/** *.md"
      spell_check_config: ".cspell.json"
      deploy_pages: true
```

### With Jekyll Integration

```yaml
jobs:
  docs:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-publish.yml@v1
    with:
      doxygen_config: _config/Doxyfile
      deployment_branch: gh-pages
      jekyll_enabled: true
      jekyll_config: "_config.yml"
      jekyll_source: "docs"
      jekyll_destination: "_site"
      run_link_check: true
      deploy_pages: true
```

### Advanced Jekyll Configuration

```yaml
jobs:
  docs:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-publish.yml@v1
    with:
      doxygen_config: _config/Doxyfile
      deployment_branch: gh-pages
      jekyll_enabled: true
      jekyll_config: "_config.yml,_config_prod.yml"
      jekyll_source: "docs"
      jekyll_destination: "_site"
      jekyll_environment: "production"
      jekyll_safe: true
      jekyll_verbose: true
      jekyll_strict_front_matter: true
      jekyll_drafts: false
      jekyll_future: false
      jekyll_unpublished: false
      run_link_check: true
      deploy_pages: true
```

### Custom Configuration

```yaml
jobs:
  docs:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-publish.yml@v1
    with:
      doxygen_config: docs/Doxyfile.custom
      deployment_branch: gh-pages
      run_link_check: false
      deploy_pages: false
```

### Submodule Documentation Projects

```yaml
jobs:
  docs:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-publish.yml@v1
    with:
      checkout_recursive: true  # Required for submodule-based docs
      doxygen_config: _config/Doxyfile
      deployment_branch: gh-pages
      jekyll_enabled: true
      jekyll_source: "docs"
      run_link_check: true
      link_check_paths: "docs/** *.md **/docs/**"
```

## ⚙️ Configuration

### Repository Setup

#### **Submodule Checkout**

The workflow supports optional recursive submodule checkout for projects that store documentation in submodules:

```yaml
checkout_recursive: true  # Enable submodule checkout
```

**When to use recursive checkout:**
- Documentation is stored in a separate submodule repository
- Doxygen source files are in submodules
- Jekyll themes or plugins are in submodules
- External documentation dependencies are in submodules

**When NOT to use recursive checkout:**
- All documentation is in the main repository
- No submodules are present
- Performance optimization (recursive checkout is slower)

**Default behavior:** `false` (no submodule checkout)

### Optimized Dependency Installation

The workflow uses optimized installation methods for maximum speed:

- **Doxygen**: `ssciwr/doxygen-install@v1` - Pre-built binaries with caching
- **Graphviz**: `tlylt/install-graphviz@v1` - Pre-built binaries with caching
- **Pre-installation Check**: Uses pre-installed Graphviz if available (instant)
- **Performance**: 75-90% faster than traditional `apt-get` installation

### Doxygen Configuration

This repository ships with a preconfigured Doxygen setup at `_config/Doxyfile`. Run it
from the repository root so the relative paths resolve correctly:

```bash
doxygen _config/Doxyfile
```

The configuration publishes HTML documentation to `docs/doxygen/html`, enabling GitHub
Pages to surface the generated API reference alongside the rest of the site. It also
discovers the sample sources in `cpp-ci-test/`, which you can reuse to validate C and
C++ focused workflows.

When invoking the reusable workflow, point to this configuration explicitly:

```yaml
with:
  doxygen_config: _config/Doxyfile
  doxygen_working_directory: .
```

> Need to customize the inputs? Copy `_config/Doxyfile` and adjust `INPUT`,
> `OUTPUT_DIRECTORY`, or any other settings to match your project's layout.

### Link Checking with Lychee

The workflow includes advanced link checking using Lychee, which provides comprehensive link validation
for both internal and external links.

```yaml
run_link_check: true  # Enable link checking (default: true)
link_check_paths: "docs/** *.md"  # Paths to check for broken links
```

The Lychee link checker:
- Scans all markdown files in the specified paths
- Uses **space-separated glob patterns** (not comma-separated)
- Validates both internal file references and external URLs
- Supports configurable timeouts and retry attempts
- Excludes private/internal links by default
- Provides detailed reporting with verbose output options

**Path Format Examples:**
- `**/*.md` - All .md files recursively (default)
- `docs/** *.md` - All files in docs/ and all .md files in root (space-separated)
- `README.md docs/**/*.md` - Specific file + all .md files in docs/ (space-separated)
- Uses the modern `lycheeverse/lychee-action@v2` action
- Offers better performance and reliability than traditional link checkers

**Important**: Paths must be **space-separated**, not comma-separated, as required by `lycheeverse/lychee-action@v2`.

### Markdown Linting

Optional markdown linting using `markdownlint-cli` to enforce consistent markdown formatting and catch common issues.

```yaml
run_markdown_lint: true  # Enable markdown linting (default: false)
markdown_lint_paths: "**/*.md"  # Glob patterns for files to lint
markdown_lint_config: "_config/.markdownlint.json"  # Path to markdownlint config
```

Features:
- Enforces consistent markdown formatting
- Catches common markdown issues
- Configurable via `_config/.markdownlint.json` (override with `markdown_lint_config`)
- Ignores `node_modules` by default

### Spell Checking

Optional spell checking using `cspell` to catch spelling errors in documentation.

```yaml
run_spell_check: true  # Enable spell checking (default: false)
spell_check_paths: "**/*.md"  # Glob patterns for files to check
spell_check_config: ".cspell.json"  # Path to cspell config file
```

Features:
- Catches spelling errors in documentation
- Configurable via `.cspell.json` file
- Supports custom dictionaries and ignore patterns
- Works with multiple file types

### Jekyll Integration

Optional Jekyll static site generation for enhanced documentation presentation and better GitHub Pages integration.

```yaml
jekyll_enabled: true  # Enable Jekyll (default: false)
jekyll_config: "_config.yml"  # Path to Jekyll config
jekyll_source: "docs"  # Source directory
jekyll_destination: "_site"  # Build destination
```

**Jekyll Configuration:**

The workflow automatically creates a minimal `_config.yml` file if one doesn't exist.
For comprehensive Jekyll configuration, see the [Jekyll Guide](jekyll-guide.md).

**Quick Setup:**
```yaml
# Basic Jekyll configuration
title: "My C++ Project Documentation"
description: "Comprehensive documentation for my C++ project"
baseurl: ""  # Set by workflow automatically
url: "https://yourusername.github.io"
theme: minima
markdown: kramdown
highlighter: rouge
```

**Features:**
- Static site generation with customizable themes
- Better GitHub Pages integration
- Enhanced navigation and presentation
- Support for custom layouts and includes
- Automatic baseurl configuration for GitHub Pages
- **Smart configuration validation** with directory-aware checking
- **Automatic API reference link injection** into Jekyll navigation

**Advanced Jekyll Configuration:**

The workflow supports extensive Jekyll configuration options for fine-tuned control:

```yaml
jekyll_enabled: true
jekyll_config: "_config.yml,_config_prod.yml"  # Multiple config files
jekyll_environment: "production"               # Environment-specific settings
jekyll_safe: true                              # Safe mode (GitHub Pages compatible)
jekyll_verbose: true                           # Verbose output for debugging
jekyll_strict_front_matter: true              # Fail on YAML syntax errors
jekyll_drafts: false                           # Exclude draft posts
jekyll_future: false                           # Exclude future-dated posts
jekyll_unpublished: false                      # Exclude unpublished posts
jekyll_incremental: false                      # Disable incremental builds (CI recommended)
jekyll_lsi: false                              # Disable LSI (resource-intensive)
jekyll_profile: false                          # Disable profiling (reduces build time)
jekyll_quiet: false                            # Enable normal output
jekyll_trace: false                            # Disable full backtrace
```

**CI-Optimized Defaults:**
The workflow automatically applies CI-optimized defaults for better reliability:
- Safe mode enabled (prevents custom plugin issues)
- Incremental builds disabled (prevents stale content)
- Profiling disabled (reduces build time)
- Drafts and future posts excluded (focus on published content)
- Strict front matter validation enabled (ensures content integrity)

### Standalone Link Check

For repositories that only need link checking without documentation generation, use the dedicated link check workflow:

```yaml
jobs:
  link-check:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-linkcheck.yml@v1
    with:
      paths: "docs/** *.md **/docs/**"  # Paths to check (default: **/*.md)
      fail_on_errors: true              # Fail on broken links
      timeout: "10"                     # Timeout per link (seconds)
      retry: "3"                        # Number of retries
      exclude_private: true             # Exclude private links
      exclude_mail: true                # Exclude mailto links
      verbose: false                    # Verbose output
      # Uses lycheeverse/lychee-action@v2 for advanced link checking
```

### 🔍 Jekyll Configuration Validation

The workflow includes intelligent Jekyll configuration validation that:

#### **Smart Directory Detection**
- Reads your `_config.yml` to determine custom directory locations
- Checks directories where they're actually configured (e.g., `_config/_layouts`)
- Falls back to standard locations if custom paths aren't specified
- Reports missing directories as "may be using theme defaults"

#### **File Location Validation**
- Checks common files (`index.md`, `404.html`, `robots.txt`) relative to your config file location
- If `_config.yml` is in `docs/`, files are checked in `docs/` directory
- Prevents false warnings about missing files in wrong locations

#### **Configuration Warnings**
- Detects trailing slashes in `baseurl` and `url` (should be avoided)
- Validates YAML syntax with specific error reporting
- Provides helpful guidance for common configuration issues

**Example Validation Output:**
```
🔍 Validating Jekyll configuration...
✅ Validating config file: _config/_config.yml
  ✅ YAML syntax is valid
✅ Found layouts directory: _config/_layouts
✅ Found includes directory: _config/_includes
⚠️  Directory not found: _config/_sass (may be using theme defaults)
✅ Found file: index.md
✅ Found file: 404.html
✅ Found file: robots.txt
⚠️  File not found: index.html (optional but recommended)
✅ Jekyll configuration validation completed
```

For detailed validation guidance, see the [Jekyll Configuration Guide](jekyll-guide.md#-configuration-validation).

### 🔗 Automatic API Reference Link Injection

The workflow automatically injects API reference links into your Jekyll configuration when Doxygen is
enabled. This provides seamless navigation from your documentation site to the API documentation.

#### **How It Works:**

1. **Detection**: When Doxygen is enabled (`doxygen_config` is specified), the workflow detects this
2. **URL Generation**: Creates the appropriate API reference URL based on version and repository
3. **Configuration Injection**: Automatically adds the link to Jekyll's `aux_links` section
4. **Navigation Integration**: The link appears in your Jekyll site's navigation menu

#### **Generated URL Format:**
```
https://username.github.io/repository/version/api/index.html
```

**Examples:**
- Development: `https://username.github.io/my-project/development/api/index.html`
- Stable Release: `https://username.github.io/my-project/v1.2.0/api/index.html`
- Preview: `https://username.github.io/my-project/preview/api/index.html`

#### **Configuration Behavior:**

**If `aux_links` section exists:**
```yaml
# Your existing config
aux_links:
  "🏠 Home": "/"
  "📚 Documentation": "/docs/"

# Workflow automatically adds:
aux_links:
  "🏠 Home": "/"
  "📚 Documentation": "/docs/"
  "📖 API Reference":
    - "/my-project/development/api/index.html"
```

**If `aux_links` section doesn't exist:**
```yaml
# Workflow creates new section:
aux_links:
  "📖 API Reference":
    - "/my-project/development/api/index.html"
```

#### **Smart Updates:**
- **Existing API Reference**: If an API reference already exists, it's updated with the new URL
- **Version-Aware**: The URL automatically reflects the current version being deployed
- **Repository-Aware**: The URL includes the correct repository name

#### **Benefits:**
- ✅ **Zero Configuration**: Works automatically when Doxygen is enabled
- ✅ **Version-Aware**: Always points to the correct version's API docs
- ✅ **Theme Compatible**: Works with any Jekyll theme that supports `aux_links`
- ✅ **Non-Destructive**: Preserves existing `aux_links` configuration
- ✅ **Smart Updates**: Updates existing API references instead of duplicating

### Versioned Deployment Process

The workflow uses a sophisticated deployment process that maintains versioned documentation:

1. **Jekyll Site Deployment**: Deploys the generated `_site` directory to a version folder using `peaceiris/actions-gh-pages@v3`
2. **Doxygen Artifacts Deployment**: Deploys Doxygen artifacts to the root `/doxs/` directory using `peaceiris/actions-gh-pages@v3`
3. **Root Files Update**: Clones the `gh-pages` branch to update root redirects and version selector
4. **Version Metadata**: Creates `version_info.json` files in each deployed version directory
5. **Preserve History**: Uses `keep_files: true` to maintain all previous versions

### GitHub Pages Setup

**Important**: GitHub Pages must be enabled in your repository settings before using this workflow.

1. **Enable GitHub Pages** in your repository settings:
   - Go to **Settings** → **Pages**
   - Set **Source** to "GitHub Actions"
   - Save the settings

2. **Grant permissions** to the workflow:

```yaml
permissions:
  contents: write
  pages: write
  id-token: write
```

3. **Workflow behavior**:
   - If Pages is not enabled, the workflow will continue but skip deployment
   - Documentation will still be built and artifacts uploaded
   - No errors will occur if Pages is not configured

### Access URLs

After deployment, your documentation will be available at:

- **Root**: `https://username.github.io/repository/` → Redirects to latest version
- **Version Selector**: `https://username.github.io/repository/version_selector.html`
- **Specific Version**: `https://username.github.io/repository/v1.2.0/`
- **Development**: `https://username.github.io/repository/development/`
- **API Documentation**: `https://username.github.io/repository/v1.2.0/api/`
- **Centralized API**: `https://username.github.io/repository/doxs/v1.2.0/`

### Versioned Deployment Details

The workflow creates a sophisticated versioned documentation system:

#### **What Gets Deployed Where:**
- **Jekyll `_site/` contents** → **`gh-pages/version/`** (e.g., `development/`, `v1.2.0/`) via `peaceiris/actions-gh-pages`
- **Doxygen `doxs/` contents** → **`gh-pages/doxs/`** (centralized API docs) via `peaceiris/actions-gh-pages`
- **Root navigation files** → **`gh-pages/`** (redirects, version selector, README) via manual git operations

#### **Version Detection:**
- **Main branch pushes** → `development/` version
- **Release branch pushes** → `v1.2.0/` version (extracted from branch name)
- **Tag creation** → `v1.2.0/` version (extracted from tag name)
- **Other branches** → `preview/` version

#### **Smart Root Redirects:**
- **Stable releases** → Redirects to specific version (e.g., `v1.2.0/`)
- **Development** → Redirects to `development/`
- **Preview** → Redirects to `development/` as fallback

#### **Version Metadata:**
Each deployed version includes a `version_info.json` file with:
```json
{
  "version": "v1.2.0",
  "type": "stable",
  "deployed_at": "2024-01-15T10:30:00Z",
  "commit": "abc123...",
  "ref": "refs/tags/v1.2.0",
  "doxygen_version": "v1.2.0"
}
```

## 🌐 GitHub Pages Setup

### Repository Settings

1. Go to **Settings** → **Pages**
2. Set **Source** to "GitHub Actions"
3. Ensure **GitHub Actions** has write permissions

### Workflow Permissions

The workflow requires these permissions:

```yaml
permissions:
  contents: write      # Upload artifacts
  pages: write         # Deploy to Pages
  id-token: write      # Authentication
```

### Custom Domain (Optional)

Add a `CNAME` file to your `docs/doxygen/html` directory:

```
docs.yourproject.com
```

## 🔧 Troubleshooting

### Common Issues

**Doxygen Build Fails**
- Verify `Doxyfile` exists and is valid
- Check source directories exist (`src/`, `include/`)
- Graphviz is automatically installed via optimized action (no manual setup needed)
- Verify `doxygen_config` path is correct (and set `doxygen_working_directory` if relative paths expect a different working folder)

**Jekyll Configuration Validation Issues**

- **False warnings about missing directories**: Check if your `_config.yml` specifies custom directory
  locations (e.g., `layouts_dir: _config/_layouts`)
- **Files not found warnings**: Ensure common files (`index.md`, `404.html`, `robots.txt`) are in the
  same directory as your `_config.yml`
- **Trailing slash warnings**: Remove trailing slashes from `baseurl` and `url` in your configuration
- **YAML syntax errors**: Use online YAML validators or `yq` to check syntax

**GitHub Pages Not Deploying**
- Check repository permissions
- Verify `deploy_pages: true`
- Ensure workflow runs on main branch (not PRs)
- **Enable GitHub Pages** in repository settings (Settings → Pages → Source: GitHub Actions)
- Check if Pages site exists and is configured properly

**Link Check Fails**
- Verify link paths are correct in `link_check_paths`
- Check that markdown files exist at specified paths
- Review link checker output for specific broken links

**Markdown Lint Fails**
- Check markdown syntax and formatting
- Review `_config/.markdownlint.json` (or your configured `markdown_lint_config`) if present
- Fix linting errors reported by markdownlint

**Spell Check Fails**
- Review spelling errors in documentation
- Add words to `.cspell.json` custom dictionary if needed
- Check `spell_check_config` path is correct

### Debug Mode

Enable debug output:

```yaml
env:
  ACTIONS_STEP_DEBUG: true
```

### Manual Testing

Test Doxygen locally:

```bash
# Install Doxygen and Graphviz
# Option 1: Using package manager (slower)
sudo apt-get install doxygen graphviz

# Option 2: Using optimized actions (faster, like in CI)
# For local development, you can use the same actions:
# - ssciwr/doxygen-install@v1 for Doxygen
# - tlylt/install-graphviz@v1 for Graphviz

# Generate docs
doxygen Doxyfile

# Check output
ls docs/doxygen/html/
```

## 🔧 Troubleshooting

### Common Configuration Issues

#### **Sed Syntax Errors**

**Problem**: Workflow fails with `sed: -e expression #1, char 44: unterminated 's' command`

**Cause**: Inline comments in configuration files can cause sed syntax errors during processing.

**Solution**: The workflow now automatically handles inline comments safely. If you encounter this error:

1. **Check your `_config.yml`** for inline comments:
   ```yaml
   # This is safe
   title: "My Project"  # This comment is handled automatically
   baseurl: "/my-project"  # GitHub Pages subpath
   ```

2. **The workflow automatically**:
   - Strips inline comments during processing
   - Generates clean configuration files
   - Prevents sed syntax errors

**Example Fix**:
```yaml
# Before (could cause errors in older versions)
baseurl: "/my-project"  # GitHub Pages subpath

# After (handled automatically by current workflow)
baseurl: "/my-project"  # GitHub Pages subpath
# ↑ This comment is now safely stripped during processing
```

#### **YAML Validation Issues**

**Problem**: YAML syntax errors in configuration files

**Solution**: The workflow includes built-in YAML validation:

1. **Automatic validation** - YAML syntax is checked during workflow execution
2. **Clear error messages** - Specific line numbers and error descriptions
3. **Prevention** - Validation runs before configuration processing

**Manual validation**:
```bash
# Install yamllint
pip install yamllint

# Validate your configuration
yamllint _config.yml
```

#### **Configuration Generation Failures**

**Problem**: Version-specific configuration generation fails

**Solution**: The workflow now includes robust configuration processing:

1. **Comment-safe extraction** - Handles inline comments automatically
2. **Clean generation** - Creates `_config_generated.yml` without syntax errors
3. **Error prevention** - Validates configuration before processing

**Check generated configuration**:
```bash
# After workflow runs, check the generated file
cat _config_generated.yml
```

#### **Missing Deployment Branch**

**Problem**: Workflow fails with `fatal: Remote branch gh-pages not found in upstream origin`

**Solution**: The workflow automatically creates the deployment branch if it doesn't exist:

1. **Auto-detection** - Checks if the deployment branch exists
2. **Auto-creation** - Creates the branch from main/master if missing
3. **Fallback handling** - Tries main branch first, then master
4. **Clear messaging** - Provides informative output about branch creation

**What happens automatically**:
- ✅ Checks if `gh-pages` branch exists
- ✅ Creates branch from main/master if missing
- ✅ Pushes the new branch to origin
- ✅ Continues with deployment normally

**Manual creation** (if needed):
```bash
# Create gh-pages branch manually
git checkout -b gh-pages
git push origin gh-pages
```

#### **Git Authentication Errors**

**Problem**: Workflow fails with `fatal: could not read Username for 'https://github.com': No such device or address`

**Solution**: The workflow now uses proper GitHub token authentication:

1. **Automatic authentication** - Uses GitHub Actions built-in `GITHUB_TOKEN` with proper permissions
2. **Secure URLs** - Uses standard HTTPS URLs without token exposure
3. **No manual setup** - Works automatically in GitHub Actions environment

**What happens automatically**:
- ✅ Uses GitHub Actions built-in authentication via `contents: write` permission
- ✅ Uses standard HTTPS URLs without token exposure
- ✅ Clones and pushes using secure authentication
- ✅ No manual token configuration needed
- ✅ Works with private repositories (with proper permissions)

**Technical Details**:
- Uses standard HTTPS URLs without embedded tokens
- Relies on `contents: write` permission for authentication
- GitHub Actions automatically provides `GITHUB_TOKEN` with proper permissions
- No token exposure in logs or URLs

## 📚 Related Workflows

- **[C/C++ Lint](ru-cpp-lint.md)** - Code quality checks
- **[Static Analysis](ru-cpp-analysis.md)** - Security analysis
- **[Link Check](ru-docs-linkcheck.md)** - Documentation link validation

## 🔗 Related Resources

- [Doxygen Documentation](https://www.doxygen.nl/)
- [GitHub Pages](https://docs.github.com/en/pages)
- [Markdown Link Checking](https://github.com/tcort/markdown-link-check)

---

[← Previous: Static Analysis Workflow](ru-cpp-analysis.md) | [Next: Link Check Workflow →](ru-docs-linkcheck.md)

**📚 [All Documentation](index.md)** | **🏠 [Main README](../README.md)**

