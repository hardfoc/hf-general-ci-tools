---
layout: default
title: "🔗 Documentation Link Check (Reusable)"
description: "Reusable workflow for documentation link validation using Lychee"
nav_order: 4
parent: "🔄 Reusable Workflows"
---

# 🔗 Documentation Link Check (Reusable)

**Workflow:** `ru-docs-linkcheck.yml` → 🔗 **[RU] Documentation Link Check**

A comprehensive reusable workflow for automated documentation link validation using Lychee. Ensures all links in your documentation are valid, accessible, and properly formatted across multiple file types.

---

## 📋 Overview

This reusable workflow (`ru-docs-linkcheck.yml`) validates all documentation links in your repository using the powerful Lychee link checker. It supports extensive configuration options for different types of projects and documentation structures.

### ✨ **Live CI Example**
� See our comprehensive testing workflow: [`ci-docs-linkcheck.yml`](../.github/workflows/ci-docs-linkcheck.yml) which demonstrates **all features** of this reusable workflow by testing it against this repository's documentation with maximum configuration options enabled.
It ensures that all internal and external links are working correctly, preventing broken references in your documentation.

### **Key Features**

- 🔍 **Comprehensive Link Checking** - Validates all markdown files and documentation using Lychee
- 🌐 **External Link Validation** - Checks external URLs for accessibility with retry logic
- 📁 **Internal Link Validation** - Verifies internal file references and anchors
- ⚡ **Fast Processing** - Efficient scanning with configurable timeouts and parallel processing
- 🎯 **Flexible Path Patterns** - Customizable file and directory patterns
- 📊 **Detailed Reporting** - Clear error messages and link status with verbose output
- 🛡️ **Smart Filtering** - Excludes private links and mailto addresses by default
- 🔄 **Retry Logic** - Configurable retry attempts with customizable wait times

---

## 🚀 Quick Start

### **Basic Usage**

```yaml
name: Check Documentation Links

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  link-check:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-linkcheck.yml@v1
```

### **Advanced Configuration**

```yaml
name: Advanced Link Check

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  link-check:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-linkcheck.yml@v1
    with:
      paths: "docs/** *.md **/docs/**"
      fail_on_errors: true
      timeout: "15"
      max_retries: "5"
      retry_wait_time: "2"
      exclude_private: true
      exclude_mail: true
      verbose: true
```

### **Using TOML Configuration File**

For advanced configuration, you can use a `lychee.toml` file:

```yaml
name: Link Check with TOML Config

on:
  push:
    branches: [main]

jobs:
  link-check:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-linkcheck.yml@v1
    with:
      config_file: "lychee.toml"
      paths: "docs/** *.md"
      verbose: true
```

**Creating a TOML Config File:**

Create a custom configuration file:
```bash
# Create lychee.toml in your repository root
touch lychee.toml
```

Then customize it for your needs. The TOML file allows you to:
- Set default timeouts and retry counts
- Exclude specific domains or patterns
- Configure HTTP headers and redirects
- Enable caching for faster subsequent runs

---

## 📖 Input Parameters

### 📁 File Selection

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `checkout_recursive` | `boolean` | `false` | Checkout submodules recursively (for projects with docs in submodules) |
| `paths` | `string` | `"docs/** *.md **/docs/**"` | Space-separated paths to check for broken links |

### ⚙️ Link Checking Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `timeout` | `string` | `"10"` | Timeout in seconds for each link check |
| `max_retries` | `string` | `"3"` | Maximum number of retries per request |
| `retry_wait_time` | `string` | `"1"` | Minimum wait time in seconds between retries |
| `exclude_private` | `boolean` | `true` | Exclude private/internal links |
| `exclude_mail` | `boolean` | `true` | Exclude mailto links |
| `config_file` | `string` | `""` | Path to lychee.toml config file (optional) |

### 📊 Output Control

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fail_on_errors` | `boolean` | `true` | Fail the workflow if broken links are found |
| `verbose` | `boolean` | `false` | Enable verbose output |

### **Path Patterns**

The `paths` parameter supports glob patterns:

- `docs/**` - All files in docs directory and subdirectories
- `*.md` - All markdown files in repository root
- `**/docs/**` - All files in any docs directory
- `README.md` - Specific file
- `docs/** *.md` - Multiple patterns (space-separated)

**Important**: Paths must be **space-separated**, not comma-separated, as required by `lycheeverse/lychee-action@v2`.

---

## 🔧 Usage Examples

### **Basic Link Check**

```yaml
name: Basic Link Check

on:
  push:
    branches: [main]

jobs:
  link-check:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-linkcheck.yml@v1
```

### **Custom Paths**

```yaml
name: Custom Link Check

on:
  push:
    branches: [main]

jobs:
  link-check:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-linkcheck.yml@v1
    with:
      paths: "docs/** README.md CONTRIBUTING.md"
      fail_on_errors: false
```

### **Documentation Only**

```yaml
name: Documentation Link Check

on:
  push:
    branches: [main]

jobs:
  link-check:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-linkcheck.yml@v1
    with:
      paths: "docs/**"
```

### **All Markdown Files**

```yaml
name: All Markdown Link Check

on:
  push:
    branches: [main]

jobs:
  link-check:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-linkcheck.yml@v1
    with:
      paths: "**/*.md"
```

### **With Submodule Support**

```yaml
name: Link Check with Submodules

on:
  push:
    branches: [main]

jobs:
  link-check:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-linkcheck.yml@v1
    with:
      checkout_recursive: true  # Enable submodule checkout
      paths: "docs/** *.md **/docs/**"
      fail_on_errors: true
      timeout: "15"
```

---

## 🛠️ Integration with Other Workflows

### **Combined with Documentation Workflow**

```yaml
name: Documentation Pipeline

on:
  push:
    branches: [main]

jobs:
  docs:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-publish.yml@v1
    with:
      doxygen_config: _config/Doxyfile
      run_link_check: true

  link-check:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-linkcheck.yml@v1
    with:
      paths: "docs/**"
```

### **Part of Full CI Pipeline**

```yaml
name: Full CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-cpp-lint.yml@v1

  static:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-cpp-analysis.yml@v1

  link-check:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-linkcheck.yml@v1

  docs:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-publish.yml@v1
```

---

## 🔍 How It Works

### **Link Checking Process**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Scan Files      │───▶│ Extract Links   │───▶│ Validate Links  │───▶│ Report Results  │
│ (Lychee)        │    │ (Markdown       │    │ (HTTP requests  │    │ (Success/Error  │
│                 │    │ parsing)        │    │ + retry logic)  │    │ messages)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Link Types Checked**

1. **External Links** - HTTP/HTTPS URLs
2. **Internal File Links** - Relative file paths
3. **Anchor Links** - Links to sections within files
4. **Image Links** - Image file references

### **Validation Methods**

- **External Links**: HTTP HEAD requests with configurable timeout and retry logic
- **Internal Links**: File system existence checks
- **Anchor Links**: Section header validation
- **Image Links**: File existence and format validation
- **Private Links**: Automatically excluded (configurable)
- **Mailto Links**: Automatically excluded (configurable)

---

## ⚙️ Configuration Options

### **Lychee Parameters**

The workflow uses `lycheeverse/lychee-action@v2` with these default settings:

- **Timeout**: 10 seconds per link (configurable)
- **Retry**: 3 attempts for failed links (configurable)
- **External Links**: Enabled with retry logic
- **Private Links**: Excluded by default
- **Mailto Links**: Excluded by default
- **Anchor Checking**: Enabled
- **SSL Validation**: Enabled
- **Verbose Output**: Configurable

### **Custom Configuration**

For advanced configuration, you can use a `lychee.toml` file:

```toml
[input]
files = ["docs/**", "*.md"]  # Note: TOML config uses array format, workflow uses space-separated
exclude = ["CHANGELOG.md"]

[output]
format = "detailed"
verbose = true

[check]
timeout = 10
retry = 3
exclude_all_private = true
exclude_mail = true
exclude_github_issues = false

[http]
headers = { "User-Agent" = "lychee/0.14.0" }
```

---

## 🚨 Troubleshooting

### **Common Issues**

#### **Link Check Fails**
**Symptoms**: Workflow fails with "broken links found"
**Solutions**:
```bash
# Check specific links manually
curl -I https://example.com/broken-link

# Verify internal file paths
ls -la docs/broken-file.md

# Check anchor references
grep -n "## Target Section" docs/file.md
```

#### **Timeout Errors**
**Symptoms**: "Timeout" or "Connection timeout" errors
**Solutions**:
```bash
# Check if external site is accessible
ping example.com

# Verify network connectivity
curl -I https://example.com

# Check if site requires authentication
```

#### **False Positives**
**Symptoms**: Valid links reported as broken
**Solutions**:
```bash
# Check link format
echo "https://example.com/path"

# Verify file encoding
file -i docs/file.md

# Check for special characters
grep -n "\[.*\](.*)" docs/file.md
```

### **Debug Mode**

Enable verbose output for debugging:

```yaml
jobs:
  link-check:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-linkcheck.yml@v1
    with:
      paths: "docs/**"
      fail_on_errors: false  # Don't fail on errors for debugging
```

---

## 📊 Output and Reporting

### **Success Output**

```
✅ Link check completed successfully
📊 Checked 25 files
🔗 Validated 150 links
⏱️  Processing time: 45 seconds
```

### **Error Output**

```
❌ Link check failed
📊 Checked 25 files
🔗 Found 3 broken links
⏱️  Processing time: 45 seconds

Broken links:
- docs/guide.md:5 → https://example.com/broken
- docs/api.md:12 → ../missing-file.md
- README.md:8 → #non-existent-section
```

---

## 🔗 Related Documentation

- [Documentation Workflow](ru-docs-publish.md) - Build and deploy documentation
- [C/C++ Lint Workflow](ru-cpp-lint.md) - Code quality checks
- [Static Analysis Workflow](ru-cpp-analysis.md) - Security analysis
- [CI Workflows & Design](ci-workflows.md) - Our testing philosophy and live examples
- [Main Documentation Index](index.md) - All workflow guides

---

## 📚 External Resources

- [Lychee Documentation](https://github.com/lycheeverse/lychee)
- [Lychee Action](https://github.com/lycheeverse/lychee-action)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Markdown Link Syntax](https://www.markdownguide.org/basic-syntax/#links)

---

[← Previous: Documentation Workflow](ru-docs-publish.md) | [Next: YAML Lint Workflow →](ru-yaml-lint.md)

**📚 [All Documentation](index.md)** | **🏠 [Main README](../README.md)**
