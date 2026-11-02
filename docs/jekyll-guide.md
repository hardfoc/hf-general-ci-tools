---
layout: default
title: "🔧 Jekyll Configuration Guide"
description: "Complete guide to Jekyll configuration, CI optimization, and workflow examples"
nav_order: 1
parent: "📖 Examples & Guides"
---

# 🔧 Jekyll Configuration Guide

Complete guide to configuring Jekyll with the enhanced documentation workflow, including CI
optimization and practical examples.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Configuration Validation](#-configuration-validation)
- [Configuration Files](#configuration-files)
- [Environment vs Configuration](#environment-vs-configuration)
- [CI Optimization](#ci-optimization)
- [Workflow Examples](#workflow-examples)
- [Troubleshooting](#troubleshooting)

## 🚀 Quick Start

### 1. Basic Setup

```yaml
name: Build Documentation
on:
  push:
    branches: [main]

jobs:
  build-docs:
    uses: ./.github/workflows/ru-docs-publish.yml
    with:
      jekyll_enabled: true
      jekyll_config: "_config.yml"
      jekyll_environment: "production"
```

### 2. Multiple Configuration Files

```yaml
# Production build
jekyll_config: "_config.yml,_config_prod.yml"
jekyll_environment: "production"

# Development build
jekyll_config: "_config.yml,_config_dev.yml"
jekyll_environment: "development"

# Staging build
jekyll_config: "_config.yml,_config_staging.yml"
jekyll_environment: "staging"
```

## 🔍 Configuration Validation

### Built-in Validation Features

The workflow includes comprehensive Jekyll configuration validation that automatically:

- **Validates YAML syntax** in all configuration files
- **Checks directory structure** based on your `_config.yml` settings
- **Verifies file locations** relative to configuration file location
- **Reports configuration issues** with helpful warnings
- **Handles inline comments** safely during configuration extraction
- **Generates clean configuration** for versioned deployments

### How Validation Works

#### 1. **Smart Directory Detection**
The validation reads your `_config.yml` to determine where directories should be located:

```yaml
# Your _config.yml specifies custom locations
layouts_dir: _config/_layouts
includes_dir: _config/_includes
sass:
  sass_dir: _config/_sass
```

**Validation Logic:**
- ✅ Checks `_config/_layouts` (from config) → Found!
- ✅ Checks `_config/_includes` (from config) → Found!
- ⚠️ Checks `_config/_sass` (from config) → Not found (using theme defaults)

#### 2. **File Location Validation**
Files are checked relative to where your `_config.yml` is located:

```yaml
# If _config.yml is in docs/ directory
# Files are checked in docs/ directory, not root
```

**Example Output:**
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

#### 3. **Configuration Warnings**
The validation catches common configuration issues:

- **Trailing slashes** in `baseurl` or `url` (should not end with `/`)
- **Missing required directories** (with fallback to theme defaults)
- **YAML syntax errors** (with specific line numbers)

### Validation Best Practices

#### ✅ **Do This:**
```yaml
# Correct baseurl (no trailing slash)
baseurl: "/my-project"

# Correct url (no trailing slash)
url: "https://username.github.io"

# Specify custom directory locations
layouts_dir: _config/_layouts
includes_dir: _config/_includes
```

#### ❌ **Avoid This:**
```yaml
# Incorrect - trailing slashes
baseurl: "/my-project/"
url: "https://username.github.io/"

# Don't worry about missing directories if using theme defaults
# The validation will correctly report this
```

### Troubleshooting Validation Issues

#### **False Warnings About Missing Directories**
If you see warnings about missing `_layouts`, `_includes`, or `_sass` directories:

1. **Check your `_config.yml`** - Are custom paths specified?
2. **Verify directory locations** - Do they exist where specified?
3. **Theme defaults** - Missing directories are fine if using theme defaults

#### **File Not Found Warnings**
Common files (`index.md`, `404.html`, `robots.txt`) are checked in the same directory as your `_config.yml`:

- If `_config.yml` is in `docs/`, files are checked in `docs/`
- If `_config.yml` is in root, files are checked in root

### 🔧 Configuration Generation and Comment Handling

#### **Robust Configuration Processing**

The workflow includes advanced configuration processing that safely handles inline comments and
generates clean, versioned configurations:

**Key Features:**
- **Comment-safe extraction** - Automatically strips inline comments during configuration processing
- **Version-specific generation** - Creates `_config_generated.yml` with version information
- **Error prevention** - Prevents `sed` syntax errors from malformed configuration lines

#### **How Comment Handling Works**

The workflow safely extracts configuration values even when they contain inline comments:

```yaml
# Your _config.yml with inline comments
title: "My Project"  # Project title
baseurl: "/my-project"  # GitHub Pages subpath
layouts_dir: _config/_layouts  # Custom layouts
```

**Processing Steps:**
1. **Extract value** - Gets the configuration value
2. **Strip comments** - Removes `# comment` portions safely
3. **Clean whitespace** - Trims leading/trailing spaces
4. **Generate versioned config** - Creates clean configuration for deployment

**Example Processing:**
```bash
# Input: baseurl: "/my-project"  # GitHub Pages subpath
# Output: /my-project (clean, no comments)
```

#### **Version-Specific Configuration Generation**

For versioned documentation, the workflow automatically:

1. **Copies your main config** - Uses `_config.yml` as the base
2. **Extracts clean values** - Safely processes title, baseurl, and directory settings
3. **Injects version info** - Adds version-specific metadata
4. **Generates clean config** - Creates `_config_generated.yml` without syntax errors

**Generated Configuration Example:**
```yaml
# _config_generated.yml (auto-generated)
title: "My Project - v1.2.3"
baseurl: "/my-project/v1.2.3"
version: "v1.2.3"
version_type: "stable"
# ... rest of your original configuration
```

#### **Error Prevention**

This robust processing prevents common configuration errors:

- ❌ **Before**: `sed: -e expression #1, char 44: unterminated 's' command`
- ✅ **After**: Clean configuration generation without syntax errors

## 📁 Configuration Files

### Navigation in Just the Docs

Just the Docs uses **front matter navigation**:

- **Front matter attributes** - `nav_order`, `parent`, `has_children` in page front matter
- **Folder structure** - Pages are organized in directories
- **Auto-detection** - Just the Docs automatically builds navigation from page structure

### Standard Naming Convention

Use these standard naming conventions for your Jekyll configuration files:

- `_config.yml` - Base configuration
- `_config_staging.yml` - Staging overrides (optional)
- `_config_theme.yml` - Theme-specific settings (optional)
- `_config_analytics.yml` - Analytics settings (optional)

### Base Configuration (`_config.yml`)

```yaml
# Site settings
title: "My Project Documentation"
description: "Comprehensive documentation for my project"
baseurl: ""  # Set automatically by workflow for GitHub Pages
url: "https://yourusername.github.io"

# Author information
author:
  name: "Your Name"
  email: "your.email@example.com"
  url: "https://github.com/yourusername"

# Build settings
markdown: kramdown
highlighter: rouge
permalink: pretty

# Theme settings
theme: minima
# OR for remote themes:
# remote_theme: just-the-docs/just-the-docs

# Plugins
plugins:
  - jekyll-feed
  - jekyll-sitemap
  - jekyll-seo-tag
  - jekyll-redirect-from
  - jekyll-optional-front-matter

# Collections
collections:
  docs:
    output: true
    permalink: /:collection/:path/

# Navigation
navigation:
  - title: "Home"
    url: "/"
  - title: "Getting Started"
    url: "/getting-started/"
  - title: "API Reference"
    url: "/api/"

# Exclude files
exclude:
  - Gemfile
  - Gemfile.lock
  - node_modules
  - vendor
  - .git
  - .github
  - README.md
  - LICENSE
```

### Environment-Specific Configurations

> **Note**: For versioned documentation, the main `_config.yml` is dynamically modified by default. See the
> [Versioning Guide](versioning-guide.md) for details.

#### Development Configuration

```yaml
# Development URL settings
url: "http://localhost:4000"
baseurl: ""

# Development-specific settings
incremental: true   # Enable incremental builds
future: true        # Show future-dated posts
drafts: true        # Show draft posts
unpublished: true   # Show unpublished posts
verbose: true       # Enable verbose output
profile: true       # Enable profiling
safe: false         # Allow custom plugins

# Development exclusions (less restrictive)
exclude:
  - Gemfile
  - Gemfile.lock
  - node_modules
  - vendor
  - .git
  - .github
  - README.md
  - LICENSE
```

#### Production Configuration

```yaml
# Production URL settings
url: "https://yourusername.github.io"
baseurl: "/your-repo-name"

# Production optimizations
compress_html:
  clippings: all
  comments: all
  endings: all
  startings: [html, head, body]

# Production-specific settings
incremental: false  # Disable incremental builds
future: false       # Don't publish future-dated posts
drafts: false       # Don't publish draft posts
unpublished: false  # Don't publish unpublished posts
safe: true          # Enable safe mode
verbose: true       # Enable verbose output
profile: false      # Disable profiling
strict_front_matter: true  # Fail on front matter errors
lsi: false          # Disable LSI

# Production exclusions
exclude:
  - Gemfile
  - Gemfile.lock
  - node_modules
  - vendor
  - .git
  - .github
  - README.md
  - LICENSE
  - "*.gem"
  - "*.gemspec"
  - .sass-cache
  - .jekyll-cache
  - .jekyll-metadata
  - _config_dev.yml
  - _config_staging.yml
  - .env*
```

## 🌍 Environment vs Configuration

### Two Independent Concepts

Jekyll has **two separate mechanisms** that work together:

#### 1. `JEKYLL_ENV` - Runtime Environment Variable
- **Purpose**: Controls logic inside Liquid templates
- **Access**: `jekyll.environment` in templates
- **Usage**: Set as environment variable before Jekyll commands

```bash
# Set environment variable
JEKYLL_ENV=production bundle exec jekyll build
JEKYLL_ENV=development bundle exec jekyll build
```

**In Liquid templates:**
```liquid
{% if jekyll.environment == "production" %}
  <script src="analytics.js"></script>
{% endif %}

{% if jekyll.environment == "development" %}
  <div class="debug-banner">Development Mode</div>
{% endif %}
```

#### 2. `--config` - Configuration File Selection
- **Purpose**: Controls which YAML files Jekyll loads
- **Usage**: Comma-separated list of config files
- **Precedence**: Later files override earlier ones

```bash
# Multiple config files
jekyll build --config _config.yml,_config_prod.yml
```

### How They Work Together

**You associate them by convention** in your workflow:

```yaml
# Production build
jekyll_environment: "production"        # Sets JEKYLL_ENV=production
jekyll_config: "_config.yml,_config_prod.yml"  # Loads these configs

# Development build
jekyll_environment: "development"      # Sets JEKYLL_ENV=development
jekyll_config: "_config.yml,_config_dev.yml"  # Loads these configs
```

**Result:**
- **Configs** set structural things (URLs, excludes, plugins, etc.)
- **Environment** lets you branch on behaviors in Liquid templates
- **Association** is your choice - you decide which config goes with which environment

## ⚡ CI Optimization

### Automatic CI Defaults

The workflow automatically applies CI-optimized defaults for Jekyll command-line options:

| Setting | CI Default | Reason |
|---------|------------|--------|
| `incremental` | `false` | Prevents stale content issues |
| `watch` | `false` | Unnecessary in CI environments |
| `serve` | `false` | Not applicable for CI builds |
| `livereload` | `false` | Not applicable for CI builds |
| `safe` | `true` | More secure and predictable |
| `verbose` | `true` | Better debugging in CI |
| `profile` | `false` | Reduces build time |
| `drafts` | `false` | Focus on finalized content |
| `future` | `false` | Prevent future content publishing |
| `unpublished` | `false` | Focus on published content |
| `lsi` | `false` | Resource-intensive, not needed for CI |
| `strict_front_matter` | `true` | Ensure content integrity |

### Override CI Defaults

Users can override CI defaults when needed:

```yaml
# Override CI defaults for development
jekyll_environment: "development"
jekyll_drafts: true      # Override CI default
jekyll_future: true      # Override CI default
jekyll_safe: false       # Override CI default
```

## 🚀 Workflow Examples

### Basic Production Build

```yaml
name: Production Documentation Build
on:
  push:
    branches: [main]

jobs:
  build-docs:
    uses: ./.github/workflows/ru-docs-publish.yml
    with:
      jekyll_enabled: true
      jekyll_config: "_config.yml,_config_prod.yml"
      jekyll_environment: "production"
      # CI defaults automatically applied
```

### Development Build with Overrides

```yaml
name: Development Documentation Build
on:
  push:
    branches: [develop]

jobs:
  build-docs:
    uses: ./.github/workflows/ru-docs-publish.yml
    with:
      jekyll_enabled: true
      jekyll_config: "_config.yml,_config_dev.yml"
      jekyll_environment: "development"
      # Override CI defaults for development
      jekyll_drafts: true
      jekyll_future: true
      jekyll_safe: false
```

### Multi-Environment Build

```yaml
name: Multi-Environment Build
on:
  push:
    branches: [main, develop, staging]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        default: 'production'
        type: choice
        options:
          - production
          - staging
          - development

jobs:
  build-docs:
    uses: ./.github/workflows/ru-docs-publish.yml
    with:
      jekyll_enabled: true
      jekyll_environment: ${{ github.event.inputs.environment ||
        (github.ref == 'refs/heads/main' && 'production') ||
        (github.ref == 'refs/heads/staging' && 'staging') || 'development' }}
      jekyll_config: "_config.yml,_config_${{ github.event.inputs.environment ||
        (github.ref == 'refs/heads/main' && 'prod') ||
        (github.ref == 'refs/heads/staging' && 'staging') || 'dev' }}.yml"
```

### Custom Configuration Files

```yaml
name: Custom Config Build
on:
  push:
    branches: [main]

jobs:
  build-docs:
    uses: ./.github/workflows/ru-docs-publish.yml
    with:
      jekyll_enabled: true
      # Any combination of config files
      jekyll_config: "_config.yml,_config_theme.yml,_config_analytics.yml,_config_prod.yml"
      jekyll_environment: "production"
```

## 🔧 Troubleshooting

### Common Issues

#### Configuration Not Found
```
❌ Jekyll config not found, creating minimal _config.yml
```
**Solution**: Ensure your config file exists in the source directory or let the workflow create a minimal one.

#### YAML Syntax Errors
```
❌ YAML syntax error in _config.yml
```
**Solution**: Validate your YAML syntax using online tools or `yq` command.

#### Build Failures
```
❌ Jekyll build failed - no output directory or empty directory
```
**Solution**: Check your configuration, ensure all required files exist, and review build logs.

### Debug Build

```yaml
name: Debug Build
on:
  workflow_dispatch:

jobs:
  build-docs:
    uses: ./.github/workflows/ru-docs-publish.yml
    with:
      jekyll_enabled: true
      jekyll_config: "_config.yml"
      jekyll_environment: "development"
      # Debug options
      jekyll_verbose: true
      jekyll_trace: true
      jekyll_profile: true
      jekyll_strict_front_matter: true
```

### Getting Help

- Check the [Jekyll documentation](https://jekyllrb.com/docs/)
- Review the [GitHub Pages documentation](https://docs.github.com/en/pages)
- Use the workflow's built-in validation
- Enable verbose output for detailed debugging

---

[Next: CI Workflows & Design →](ci-workflows.md)

**📚 [All Documentation](index.md)** | **🏠 [Main README](../README.md)**

---

*This guide provides everything you need to configure Jekyll with the enhanced documentation
workflow. For more information, see the [main documentation](index.md).*
