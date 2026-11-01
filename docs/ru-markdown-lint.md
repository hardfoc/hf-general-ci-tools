---
layout: default
title: "📄 Markdown Linting"
description: "Markdown file validation with ru-markdown-lint.yml reusable workflow"
nav_order: 7
---

# 📄 Markdown Linting

**Markdown file validation with `ru-markdown-lint.yml` reusable workflow**

---

## 🎯 Overview

The `ru-markdown-lint.yml` workflow provides comprehensive Markdown file validation:

- ✅ **Markdown syntax checking** with markdownlint
- ✅ **Style consistency** enforcement
- ✅ **Auto-fix capabilities** for common issues
- ✅ **Flexible configuration** with custom rules
- ✅ **Glob pattern matching** for targeted validation

---

## 🚀 Quick Start

### Basic Markdown Validation

```yaml
# .github/workflows/docs.yml
name: 📚 Documentation Quality

on: [push, pull_request]

jobs:
  markdown:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-markdown-lint.yml@v1
```

### Advanced Configuration

```yaml
name: 📚 Documentation Quality

on: [push, pull_request]

jobs:
  markdown:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-markdown-lint.yml@v1
    with:
      globs: "docs/**/*.md README.md"
      config_file: "_config/.markdownlint.json"
      exclude_patterns: "node_modules/**,_site/**"
      fix: false
```

---

## ⚙️ Configuration

### Inputs

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `globs` | string | `**/*.md` | Space-separated glob patterns for files to check |
| `config_file` | string | `_config/.markdownlint.json` | Path to markdownlint configuration file |
| `exclude_patterns` | string | `.git/**,node_modules/**,...` | Comma-separated patterns to exclude |
| `use_docker` | boolean | `false` | Use Docker container for more control |
| `fix` | boolean | `false` | Automatically fix fixable issues |

---

## 📋 Usage Patterns

### 1. Documentation-Only Projects

```yaml
name: Docs Quality
on: [push, pull_request]

jobs:
  markdown-lint:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-markdown-lint.yml@v1
    with:
      globs: "docs/**/*.md *.md"
      fix: false
```

### 2. Project with Mixed Content

```yaml
jobs:
  markdown-lint:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-markdown-lint.yml@v1
    with:
      globs: "docs/**/*.md README.md CONTRIBUTING.md"
      exclude_patterns: "node_modules/**,vendor/**,_site/**"
```

### 3. Auto-Fix in Development

```yaml
name: Fix Documentation
on:
  workflow_dispatch:  # Manual trigger

jobs:
  markdown-fix:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-markdown-lint.yml@v1
    with:
      fix: true  # Enable auto-fix
      globs: "**/*.md"
```

### 4. Strict Validation

```yaml
jobs:
  markdown-strict:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-markdown-lint.yml@v1
    with:
      config_file: "_config/.markdownlint-strict.json"
      use_docker: true  # More control over environment
```

---

## 🔧 Configuration Files

### Basic Configuration

Create `_config/.markdownlint.json`:

```json
{
  "default": true,
  "MD013": {
    "line_length": 120,
    "code_blocks": false,
    "tables": false
  },
  "MD033": false,
  "MD041": false
}
```

### Advanced Configuration

Create `_config/.markdownlint.json`:

```json
{
  "default": true,
  "MD001": true,
  "MD003": { "style": "atx" },
  "MD004": { "style": "dash" },
  "MD007": { "indent": 2 },
  "MD013": {
    "line_length": 120,
    "heading_line_length": 120,
    "code_blocks": false,
    "tables": false,
    "headings": false
  },
  "MD022": true,
  "MD025": true,
  "MD026": { "punctuation": ".,;:!" },
  "MD029": { "style": "ordered" },
  "MD033": { "allowed_elements": ["br", "sub", "sup"] },
  "MD036": false,
  "MD041": false,
  "MD046": { "style": "fenced" }
}
```

---

## 📝 Common Rules

### Key Markdownlint Rules

| Rule | Description | Fix |
|------|-------------|-----|
| **MD001** | Heading levels increment by one | Use proper heading hierarchy |
| **MD003** | Heading style consistency | Use consistent `#` or `===` style |
| **MD013** | Line length limits | Break long lines or adjust config |
| **MD022** | Headings surrounded by blank lines | Add blank lines around headings |
| **MD025** | Single top-level heading | Ensure only one H1 per document |
| **MD033** | No inline HTML | Use Markdown syntax instead |
| **MD041** | First line in file should be H1 | Start with main heading |

### Auto-Fixable Issues

When `fix: true` is enabled, these issues are automatically corrected:
- Trailing whitespace
- Missing blank lines
- Inconsistent list markers
- Heading spacing issues

---

## 🛠️ Advanced Scenarios

### Multiple Configuration Files

```yaml
jobs:
  docs-lint:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-markdown-lint.yml@v1
    with:
      config_file: "_config/.markdownlint-docs.json"
      globs: "docs/**/*.md"

  readme-lint:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-markdown-lint.yml@v1
    with:
      config_file: "_config/.markdownlint-readme.json"
      globs: "README.md CONTRIBUTING.md"
```

### Conditional Execution

```yaml
jobs:
  markdown-lint:
    if: contains(github.event.head_commit.message, '[docs]')
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-markdown-lint.yml@v1
```

### Integration with Other Workflows

```yaml
name: Complete Documentation CI
on: [push, pull_request]

jobs:
  markdown-lint:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-markdown-lint.yml@v1
    
  link-check:
    needs: [markdown-lint]
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-linkcheck.yml@v1
    
  build-docs:
    needs: [markdown-lint, link-check]
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-docs-publish.yml@v1
```

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Line too long** | Adjust `MD013` rule or break lines |
| **HTML not allowed** | Use Markdown syntax or allow specific tags in `MD033` |
| **Heading issues** | Follow proper heading hierarchy (H1 → H2 → H3) |
| **List formatting** | Use consistent markers (-, *, +) as configured |

### Debug Tips

1. **Test locally** with markdownlint CLI before pushing
2. **Check configuration** file syntax and location
3. **Review glob patterns** to ensure correct file matching
4. **Use Docker mode** for consistent environment
5. **Enable auto-fix** to see what can be automatically corrected

### Glob Pattern Examples

```yaml
# All markdown files
globs: "**/*.md"

# Specific directories
globs: "docs/**/*.md src/**/*.md"

# Exclude patterns in input
globs: "**/*.md"
exclude_patterns: "node_modules/**,vendor/**"

# Specific files
globs: "README.md CONTRIBUTING.md docs/index.md"
```

---

## 🔗 Related Workflows

- **[Link Check](ru-docs-linkcheck.md)** - Validate links in Markdown files
- **[Documentation Publisher](ru-docs-publish.md)** - Build and deploy documentation
- **[YAML Linting](ru-yaml-lint.md)** - Validate YAML in documentation

---

**📖 [← Back to Documentation Index](index.md)**