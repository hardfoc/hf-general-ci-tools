---
layout: default
title: "📝 YAML Linting Tools (Reusable)"
description: "Reusable workflow for YAML file validation and formatting using yamllint"
nav_order: 5
parent: "🔄 Reusable Workflows"
---

# 📝 YAML Linting Tools (Reusable)

**Workflow:** `ru-yaml-lint.yml` → 📝 **[RU] YAML Linting Tools**

A comprehensive reusable workflow for YAML file validation and formatting using yamllint. Ensures proper syntax, formatting, and adherence to best practices across all YAML files in your repository.

---

## 📋 Overview

This reusable workflow (`ru-yaml-lint.yml`) validates YAML files in your repository using yamllint to ensure proper formatting and syntax. It's designed for maximum configurability and can be easily integrated into any project with YAML files.

### ✨ **Live CI Example**
👀 See our comprehensive testing workflow: [`ci-yaml-lint.yml`](../.github/workflows/ci-yaml-lint.yml) which demonstrates **all features** of this reusable workflow by testing it against this repository's YAML files with comprehensive configuration options.

## 📋 Table of Contents

- [Overview](#-overview)
- [Inputs](#-inputs)
- [Outputs](#-outputs)
- [Usage Examples](#-usage-examples)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Related Workflows](#-related-workflows)

## 🎯 Overview

**Purpose**: YAML file validation and formatting
**Key Features**:
- yamllint integration
- Configurable rules
- Flexible path specification
- Exclude patterns support
- Strict mode option
- Detailed reporting

**Use Case**: YAML file quality and consistency enforcement

## ⚙️ Inputs

### 📁 File Selection

| Input | Description | Required | Default | Type |
|-------|-------------|----------|---------|------|
| `paths` | Comma-separated list of paths to check | No | `**/*.yml,**/*.yaml` | string |
| `exclude_patterns` | Comma-separated patterns to exclude | No | `.git/**,node_modules/**,venv/**,.venv/**` | string |

### ⚙️ Configuration

| Input | Description | Required | Default | Type |
|-------|-------------|----------|---------|------|
| `config_file` | Path to yamllint configuration file | No | `_config/.yamllint` | string |
| `strict_mode` | Enable strict mode (fail on warnings) | No | `false` | boolean |

## 📤 Outputs

| Output | Description |
|--------|-------------|
| `result` | YAML lint result (success/failure) |
| `files_checked` | Number of files checked |
| `issues_found` | Number of issues found |

## 🚀 Usage Examples

### Basic Usage

```yaml
name: YAML Lint
on: [push, pull_request]
jobs:
  yamllint:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-yaml-lint.yml@v1
```

### Advanced Usage

```yaml
name: YAML Lint
on: [push, pull_request]
jobs:
  yamllint:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-yaml-lint.yml@v1
    with:
      paths: '.github/workflows/*.yml,docs/*.yml'
      config_file: '_config/.yamllint'
      strict_mode: true
      exclude_patterns: '.git/**,node_modules/**,_site/**'
```

### Workflow-Only Checking

```yaml
name: Workflow YAML Lint
on: [push, pull_request]
jobs:
  yamllint:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-yaml-lint.yml@v1
    with:
      paths: '.github/workflows/*.yml'
      strict_mode: true
```

### Comprehensive Configuration

```yaml
name: Complete YAML Lint
on: [push, pull_request]
jobs:
  yamllint:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-yaml-lint.yml@v1
    with:
      paths: '.github/workflows/*.yml,docs/*.yml,**/*.yaml'
      config_file: '_config/.yamllint'
      strict_mode: true
      exclude_patterns: '.git/**,node_modules/**,venv/**,.venv/**,_site/**'
```

## ⚙️ Configuration

### `_config/.yamllint` Configuration

Create a `_config/.yamllint` file in your project (relative to the repository root):

```yaml
extends: default

rules:
  line-length:
    max: 120
    level: warning
  indentation:
    spaces: 2
  comments:
    min-spaces-from-content: 1
  document-start:
    present: true
  truthy:
    allowed-values: ['true', 'false', 'on', 'off']
```

### Default Rules

The workflow uses yamllint with these default settings:
- Line length: 120 characters (warning)
- Indentation: 2 spaces
- Document start: Required
- Comments: Proper spacing

## 🔧 Troubleshooting

### Common Issues

**YAML Syntax Errors**
- Check for proper indentation (2 spaces)
- Verify YAML syntax is valid
- Ensure proper document structure

**Line Length Issues**
- Adjust line length in `_config/.yamllint` configuration
- Break long lines appropriately
- Use YAML's line continuation features

**Indentation Problems**
- Use consistent 2-space indentation
- Avoid mixing tabs and spaces
- Check for proper nesting

### Debug Mode

Enable debug output by checking the workflow logs in GitHub Actions.

## 📚 Related Workflows

- **[C/C++ Lint](ru-cpp-lint.md)** - Code quality checks
- **[Static Analysis](ru-cpp-analysis.md)** - Security analysis
- **[Documentation](ru-docs-publish.md)** - Documentation generation

## 🔗 Related Resources

- [yamllint Documentation](https://yamllint.readthedocs.io/)
- [YAML Specification](https://yaml.org/spec/)
- [GitHub Actions YAML Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

---

[← Previous: Link Check Workflow](ru-docs-linkcheck.md)

**📚 [All Documentation](index.md)** | **🏠 [Main README](../README.md)**
