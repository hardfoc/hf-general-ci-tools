---
layout: default
title: "🔀 Documentation Versioning Guide"
description: "Complete guide to versioned documentation with Doxygen and Jekyll integration"
nav_order: 2
parent: "📖 Examples & Guides"
---

# 🔀 Documentation Versioning Guide

Complete guide to implementing versioned documentation with automatic Doxygen and Jekyll integration using the
enhanced `ru-docs-publish.yml` workflow.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Versioning Strategies](#versioning-strategies)
- [Configuration Options](#configuration-options)
- [Doxygen Integration](#doxygen-integration)
- [Jekyll Integration](#jekyll-integration)
- [Deployment Strategies](#deployment-strategies)
- [Workflow Examples](#workflow-examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## 🚀 Quick Start

### 1. Enable Versioning in Your Workflow

```yaml
name: '📚 Publish Versioned Documentation'

on:
  push:
    branches: ['main', 'release/*']
  pull_request:
    branches: ['main']
  workflow_dispatch:

permissions:
  contents: 'read'
  pages: 'write'
  id-token: 'write'

jobs:
  ci-docs-publish:
    uses: 'hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-publish.yml@main'
    with:
      # Versioning is now enabled by default
      deployment_branch: 'gh-pages'  # Required for versioned documentation

      # Doxygen versioning
      doxygen_version_strategy: 'auto'
      doxygen_config: '_config/Doxyfile'

      # Jekyll configuration
      jekyll_enabled: 'true'
      jekyll_source: 'docs'
      jekyll_destination: '_site'

      # Versioned deployment
      deployment_branch: 'gh-pages'

      # Quality checks
      run_link_check: 'true'
      run_markdown_lint: 'true'
      deploy_pages: 'true'
```

### 2. Version Configuration (Automatic)

**No separate config files needed!** The workflow automatically handles versioning by:

1. **Using your main `_config.yml` as the base**
2. **Dynamically injecting version information** during build
3. **Updating title and baseurl** for versioned documentation
4. **Adding version metadata** automatically

**Example: Your main `_config.yml`:**
```yaml
title: "My Project"
description: "Documentation for My Project"
baseurl: "/myproject"
url: "https://myusername.github.io"

# All your existing configuration...
markdown: kramdown
highlighter: rouge
theme: minima
```

**Automatically becomes for versioned docs:**
```yaml
title: "My Project - v1.2.3"
description: "Documentation for My Project"
baseurl: "/myproject/v1.2.3"
url: "https://myusername.github.io"

# All your existing configuration...
markdown: kramdown
highlighter: rouge
theme: minima

# Version information (auto-generated)
version: "v1.2.3"
version_type: "stable"
```

### 3. Dynamic Configuration (Automatic)

The workflow automatically modifies your main `_config.yml` to inject version-specific information:

- **Title**: Appends version name to the title
- **Base URL**: Updates to include version path
- **Version Info**: Adds `version` and `version_type` variables
- **Comment-safe processing**: Safely handles inline comments in configuration files
- **Clean generation**: Creates `_config_generated.yml` without syntax errors

No custom templates are needed - the workflow handles everything automatically with robust configuration processing.

**Navigation for Versioned Docs:**

Just the Docs uses **front matter navigation** (not `_data/navigation.yml`), so versioned navigation is handled
automatically through page front matter:

```yaml
---
nav_order: 1
parent: "Getting Started"
has_children: true
---
```

The workflow automatically generates the navigation menu based on the front matter in your markdown files.

- **Page front matter** - `nav_order`, `parent`, `has_children` work the same way
- **Folder structure** - Pages are organized in directories as usual
- **Version-specific content** - You can add version info to page titles in front matter
- **No separate navigation files needed** - Just the Docs handles this automatically

## 🎯 Versioning vs Deployment: Understanding the Difference

**Important**: Versioning and deployment are separate concerns that can be combined in different ways:

### **Architectural Design Decisions**

**The following features are automatically enabled with versioned documentation:**

- **Version preservation** - All existing version directories are preserved
- **Root redirect** - Creates redirect from root to latest stable version
- **Version selector** - Adds version selector component for navigation

**Why these are automatic:**
- **Root redirect is essential** - Without it, the root URL would be broken
- **Keeping existing versions is required** - Otherwise versions get deleted on each deployment
- **Version selector is necessary UX** - Users need a way to navigate between versions

**This architectural decision ensures:**
- ✅ **Consistent behavior** - Versioned deployment always works correctly
- ✅ **Simplified configuration** - Users don't need to understand internal dependencies
- ✅ **Professional results** - All versioned deployments have proper UX features

### **Automatic Base URL Extraction**

**The `version_base_url` input has been deprecated** in favor of automatic extraction from your Jekyll configuration:

```yaml
# In your _config.yml
baseurl: "/myproject"  # This is automatically used as the base URL

# In your workflow - no need to specify version_base_url
# The base URL "/myproject" is automatically extracted and used
```

**Benefits:**
- ✅ **Single source of truth** - Base URL defined once in `_config.yml`
- ✅ **No duplication** - Eliminates potential inconsistencies
- ✅ **Simpler configuration** - One less input to manage
- ✅ **Automatic consistency** - Versioned URLs always match your main site structure

### Versioning Without Deployment
**Purpose**: Generate versioned documentation artifacts for internal use, testing, or future deployment.

**What happens**:
- Doxygen gets versioned `PROJECT_NUMBER` (e.g., `v1.0.0`, `v1.1.0-dev`)
- Jekyll generates versioned configurations
- Documentation is built with version information
- **But NOT deployed to GitHub Pages**

**Use cases**:
- Development builds for testing
- Pre-release validation
- CI/CD artifact generation
- Internal documentation review

**Configuration**:
```yaml
deploy_pages: 'false'        # No deployment
# Versioning is always enabled by default
```

### Versioning With Deployment
**Purpose**: Publish versioned documentation to GitHub Pages for end users.

**What happens**:
- Everything from versioning without deployment, PLUS
- Deploy to versioned directories in `gh-pages` branch
- Create version selector and redirects
- Make documentation accessible to users

**Use cases**:
- Production releases
- Multi-version user access
- Release management

**Configuration**:
```yaml
deploy_pages: 'true'         # Deploy to GitHub Pages
# Versioning and versioned deployment are always enabled by default
```

### Versioning Strategies

#### Auto Detection (Recommended)

The workflow automatically detects versions from:

| Branch/Tag Pattern | Version Type | Deployment Path | Example |
|-------------------|--------------|-----------------|---------|
| `main` | Development | `development/` | Latest features |
| `release/v1.0.0` | Stable | `v1.0.0/` | Production release |
| `release/v1.1.0-rc1` | Pre-release | `v1.1.0-rc1/` | Release candidate |
| `release/v2.0.0-beta1` | Pre-release | `v2.0.0-beta1/` | Beta release |
| `v1.2.0` (tag) | Stable | `v1.2.0/` | Tagged release |

#### Disabled Versioning

**For versioned documentation (now the default):**

```yaml
deployment_branch: 'gh-pages'  # Required for versioned documentation
deploy_pages: 'true'          # Deploy to GitHub Pages
# Versioning is always enabled by default
# Automatically uses your main _config.yml as base
# No separate config files needed!
```

## ⚙️ Configuration Matrix

**Understanding how deployment settings work with versioning (always enabled):**

| `deploy_pages` | Result |
|----------------|---------|
| `false` | Versioned docs built as artifacts (no deployment) |
| `true` | Versioned docs deployed to versioned directories |

### Common Use Cases

**Development/Testing** (Build only):
```yaml
deploy_pages: 'false'
# Result: Versioned docs built as artifacts
```

**Production** (All versions):
```yaml
deploy_pages: 'true'
# Result: Versioned docs deployed to versioned directories
```

## ⚙️ Configuration Options

### Core Versioning Settings

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `deployment_branch` | string | `'gh-pages'` | Branch for versioned documentation deployment (required) |

### Doxygen Versioning

**Note**: Doxygen versioning is automatically synchronized with git-based versioning. No separate configuration needed.

#### **Automatic Version Generation:**

| Git Context | Version Type | Generated Doxygen Version | Example |
|-------------|--------------|---------------------------|---------|
| `main` branch | `development` | `{latest_tag}-dev` or `0.1.0-dev` | `v1.2.0-dev` |
| `release/v1.0.0` branch | `stable` | `{version_name}` | `v1.0.0` |
| `v1.1.0-rc1` tag | `prerelease` | `{version_name}` | `v1.1.0-rc1` |
| Other branches | `preview` | `{latest_tag}-preview` or `0.1.0-preview` | `v1.2.0-preview` |

**Benefits:**
- ✅ **Consistent formatting** - All projects follow the same pattern
- ✅ **No configuration errors** - Can't accidentally create malformed versions
- ✅ **Semantic versioning compliance** - Follows industry standards
- ✅ **Git context awareness** - Versions reflect actual git state

### **Centralized Doxygen Architecture**

**Doxygen artifacts are centrally managed for optimal access:**

#### **Root-Level Doxygen Organization:**
```
gh-pages branch:
├── doxs/                   # Centralized Doxygen artifacts
│   ├── v1.0.0/            # Doxygen docs for v1.0.0
│   ├── v1.1.0/            # Doxygen docs for v1.1.0
│   ├── v2.0.0-rc1/        # Doxygen docs for v2.0.0-rc1
│   ├── development/        # Doxygen docs for main branch
│   ├── latest -> v1.1.0/  # Symlink to latest stable
│   ├── version_selector.js # Centralized version selector
│   └── versions.json       # Centralized version metadata
├── v1.0.0/                 # Jekyll site for v1.0.0
│   ├── api -> ../../doxs/v1.0.0/  # Symlink to centralized API
│   ├── guides/             # Jekyll content
│   └── ...
└── development/            # Jekyll site for development
    ├── api -> ../../doxs/development/  # Symlink to centralized API
    ├── guides/
    └── ...
```

#### **Benefits of Centralized Architecture:**
- ✅ **Single source of truth** - All API versions in one location
- ✅ **Easy discovery** - Users know exactly where to find API docs
- ✅ **Efficient storage** - No duplication of Doxygen artifacts
- ✅ **Flexible access** - Works with or without Jekyll
- ✅ **Version selector** - Centralized navigation between API versions
- ✅ **Symlink integration** - Jekyll sites link to centralized API docs

### Deployment Settings

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `deployment_branch` | string | `gh-pages` | Branch for deployment |

## 🔧 Doxygen Integration

### Automatic Version Detection

The workflow automatically sets Doxygen's `PROJECT_NUMBER` based on:

1. **Git Tags**: Uses the latest tag for stable releases
2. **Branch Names**: Extracts version from `release/v*` branches
3. **Development**: Uses latest tag + "-dev" suffix

### Version Examples

| Source | Doxygen PROJECT_NUMBER | Description |
|--------|----------------------|-------------|
| `release/v1.0.0` | `v1.0.0` | Stable release |
| `release/v1.1.0-rc1` | `v1.1.0-rc1` | Release candidate |
| `main` (with v1.0.0 tag) | `v1.0.0-dev` | Development build |
| `main` (no tags) | `0.1.0-dev` | Initial development |


## 🎨 Jekyll Integration

### Template System

Use placeholders in your Jekyll templates:

| Placeholder | Replaced With | Example |
|-------------|---------------|---------|
| `{VERSION}` | Version name | `v1.0.0` |
| `{VERSION_TYPE}` | Version type | `stable` |
| `{BASE_URL}` | Full base URL | `/myproject/v1.0.0` |

### Generated Files

The workflow generates:

- `_config_generated.yml` - Versioned Jekyll configuration
- `version_info.json` - Version metadata

### Version Metadata

Each version includes metadata:

```json
{
  "version": "v1.0.0",
  "type": "stable",
  "deployed_at": "2024-01-15T10:30:00Z",
  "commit": "abc123...",
  "ref": "refs/heads/release/v1.0.0",
  "doxygen_version": "v1.0.0"
}
```

## 🚀 Deployment Strategies

### Versioned Deployment Structure

```
gh-pages branch:
├── index.html              # Redirects to latest stable
├── v1.0.0/                 # Stable release
│   ├── api/                # Doxygen docs
│   ├── guides/             # Jekyll content
│   ├── index.html
│   └── version_info.json
├── v1.1.0/                 # Another stable release
│   ├── api/
│   ├── guides/
│   └── ...
├── v2.0.0-rc1/             # Pre-release
│   ├── api/
│   ├── guides/
│   └── ...
└── development/            # Development (main branch)
    ├── api/
    ├── guides/
    └── ...
```

### URL Structure

| Version | URL | Description |
|---------|-----|-------------|
| Latest Stable | `/` | Redirects to latest stable |
| v1.0.0 | `/v1.0.0/` | Specific stable version |
| v2.0.0-rc1 | `/v2.0.0-rc1/` | Pre-release version |
| Development | `/development/` | Latest development |

### Custom Deployment Branch

```yaml
deployment_branch: 'docs-deploy'  # Use custom branch
```

## 📝 Workflow Examples

### Basic Versioning

```yaml
name: 'Documentation with Versioning'

on:
  push:
    branches: ['main', 'release/*']

jobs:
  docs:
    uses: 'hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-publish.yml@main'
    with:
      deployment_branch: 'gh-pages'
      doxygen_config: '_config/Doxyfile'
      jekyll_enabled: 'true'
      deploy_pages: 'true'
```

### Advanced Configuration

```yaml
name: 'Advanced Versioned Documentation'

on:
  push:
    branches: ['main', 'release/*', 'feature/*']
  pull_request:
    branches: ['main']

jobs:
  docs:
    uses: 'hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-publish.yml@main'
    with:
      # Versioning (always enabled)
      deployment_branch: 'gh-pages'

      # Doxygen (auto-synchronized with git versioning)
      doxygen_config: 'docs/Doxyfile'

      # Jekyll
      jekyll_enabled: 'true'
      jekyll_source: 'docs'
      jekyll_destination: '_site'

      # Deployment
      deployment_branch: 'gh-pages'  # Optional: defaults to 'gh-pages'

      # Quality
      run_link_check: 'true'
      run_markdown_lint: 'true'
      run_spell_check: 'true'
      verbose: 'true'

      # Standard deployment
      deploy_pages: 'true'
```

### Manual Versioning

```yaml
name: 'Manual Version Control'

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to deploy'
        required: true
        type: string

jobs:
  docs:
    uses: 'hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-publish.yml@main'
    with:
      deployment_branch: 'gh-pages'  # Required for versioned documentation
      deploy_pages: 'true'          # Deploy to GitHub Pages
```

## 🎯 Best Practices

### 1. Git-Based Versioning (Enforced)
**Always use git-based versioning for security and consistency:**
- ✅ **Tags**: `v1.0.0`, `v1.1.0-rc1`, `v2.0.0-beta1`
- ✅ **Release branches**: `release/v1.0.0`, `release/v1.1.0-rc1`
- ❌ **Manual input**: Never allow manual version names (security risk)

### 2. Branch Naming Convention

Follow semantic versioning for branches:

```bash
# Stable releases
release/v1.0.0
release/v1.1.0
release/v2.0.0

# Pre-releases
release/v1.1.0-rc1
release/v2.0.0-beta1
release/v1.2.0-alpha1

# Development
main
```

### 3. Configuration Management

The workflow automatically handles configuration without requiring templates:

- Uses your main `_config.yml` as the base
- Dynamically injects version information
- No template files needed

```

### 4. Version Selector Integration

The version selector is automatically included in your documentation:

```html
<!-- Version selector is automatically generated and injected -->
<!-- No manual inclusion needed - it's handled by the workflow -->
```

The workflow automatically creates version selector JavaScript for easy navigation between versions.

### 5. Quality Assurance

Enable all quality checks:

```yaml
run_link_check: 'true'
run_markdown_lint: 'true'
run_spell_check: 'true'
verbose: 'true'
```

### 6. Deployment Strategy

Choose the right deployment strategy:

- **Versioned Deployment**: For projects with multiple versions
- **Standard Deployment**: For simple single-version docs
- **Custom Branch**: For specialized deployment needs

## 🔧 Troubleshooting

### Common Issues

#### 1. Version Not Detected

**Problem**: Version detection fails or returns empty values.

**Solution**: Check branch naming convention and ensure deployment branch is specified:

```yaml
deployment_branch: 'gh-pages'  # Required for versioned documentation
```

#### 2. Doxygen Version Not Set

**Problem**: Doxygen `PROJECT_NUMBER` is not updated.

**Solution**: Ensure Doxygen versioning is enabled:

```yaml
doxygen_version_strategy: 'auto'  # or 'manual'
doxygen_config: '_config/Doxyfile'  # Ensure Doxyfile exists
```

#### 3. Jekyll Build Fails

**Problem**: Jekyll build fails with versioned configuration.

**Solution**: Check Jekyll configuration:

```bash
# Check if main config exists
ls _config.yml

# Verify Jekyll configuration
jekyll doctor
```

#### 4. Deployment Issues

**Problem**: Versioned deployment fails.

**Solution**: Check deployment branch and permissions:

```yaml
deployment_branch: 'gh-pages'  # Ensure branch exists
# Check repository permissions
permissions:
  contents: 'read'
  pages: 'write'
  id-token: 'write'
```

### Debug Commands

```bash
# Check version detection
echo "Version: ${{ needs.version-detection.outputs.version_name }}"
echo "Type: ${{ needs.version-detection.outputs.version_type }}"
echo "Doxygen: ${{ needs.version-detection.outputs.doxygen_version }}"

# Check generated files
ls -la docs/_config_generated.yml

# Check deployment structure
ls -la gh-pages-deploy/
```

### Getting Help

1. **Check Workflow Logs**: Review the GitHub Actions logs for detailed error messages
2. **Validate Configuration**: Ensure all required inputs are provided
3. **Test Locally**: Run Doxygen and Jekyll locally to verify configuration
4. **Check Permissions**: Ensure the workflow has necessary repository permissions

## 📚 Further Reading

- [HardFOC Versioning Policy](https://github.com/orgs/hardfoc/discussions/1) - Organization versioning strategy and guidelines
- [Jekyll Guide](jekyll-guide.md) - Jekyll configuration details
- [Doxygen Documentation](https://www.doxygen.nl/manual/) - Doxygen reference
- [Semantic Versioning](https://semver.org/) - Version numbering standard
- [GitHub Pages Documentation](https://docs.github.com/en/pages) - GitHub Pages reference

---

**Built for the HardFOC ecosystem - Enabling seamless multi-version documentation with proper Semantic Versioning**
