---
layout: default
title: "🔧 C++ Linting Tools (Reusable)"
description: "Reusable workflow for C++ code quality and formatting checks using clang-format and clang-tidy"
nav_order: 1
parent: "🔄 Reusable Workflows"
---

# 🔧 C++ Linting Tools (Reusable)

**Workflow:** `ru-cpp-lint.yml` → 🔧 **[RU] C++ Linting Tools**

A comprehensive reusable workflow for automated C++ code quality and formatting checks using industry-standard tools like clang-format and clang-tidy. This workflow provides extensive configuration options and can be easily integrated into any C++ project.

---

## 📋 Overview

This reusable workflow (`ru-cpp-lint.yml`) performs comprehensive code quality checks on C++ codebases and can be called from other repositories. It's designed for maximum flexibility and configurability.

### ✨ **Live CI Example**
👀 See our comprehensive testing workflow: [`ci-cpp-lint.yml`](../.github/workflows/ci-cpp-lint.yml) which demonstrates **all features** of this reusable workflow by testing it against real C++ code with maximum configuration options enabled.

## 📋 Table of Contents

- [Overview](#-overview)
- [Inputs](#-inputs)
- [Outputs](#-outputs)
- [Usage Examples](#-usage-examples)
- [Linting Behavior](#-linting-behavior)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Related Workflows](#-related-workflows)

## 🎯 Overview

**Purpose**: C/C++ code quality enforcement using cpp-linter-action
**Key Features**:
- clang-format for code style
- clang-tidy for static analysis
- PR annotations and comments
- Configurable file extensions
- Configurable exclude paths
- **Direct integration with cpp-linter/cpp-linter-action@v2**

**Use Case**: Code style consistency and quality enforcement

## ⚙️ Inputs

### 🔧 Clang Configuration

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `clang_version` | string | ❌ | `20` | Clang major version |
| `clang_format_config` | string | ❌ | `_config/.clang-format` | Path to clang-format configuration file |
| `clang_tidy_config` | string | ❌ | `_config/.clang-tidy` | Path to clang-tidy configuration file |
| `tidy_checks` | string | ❌ | `""` | clang-tidy checks (comma-separated glob patterns, use - prefix to disable) |

### 📁 File Selection

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `extensions` | string | ❌ | `"c,cpp,cc,cxx,h,hpp"` | File extensions to check (comma-separated) |
| `ignore` | string | ❌ | `"build\|.git"` | Files or directories to exclude from linting (pipe-separated) |
| `files_changed_only` | boolean | ❌ | `false` | Only lint files that have been changed in the pull request |
| `lines_changed_only` | boolean | ❌ | `false` | Only inspect lines that have changed in the pull request |

### 📊 Output Options

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `step_summary` | boolean | ❌ | `true` | Add a summary of linting results to the workflow step summary |
| `file_annotations` | boolean | ❌ | `true` | Display linting errors and warnings as file annotations in the GitHub UI |
| `thread_comments` | boolean | ❌ | `false` | Post a collapsible thread comment in pull requests with linting issues |

## 📤 Outputs

| Output | Description |
|--------|-------------|
| PR annotations | File-level annotations for style issues |
| PR comments | Summary comments with issue counts |
| Step summary | Workflow step summary with linting results |

## 🚀 Usage Examples

### Basic Usage

```yaml
jobs:
  lint:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-cpp-lint.yml@v1
    with:
      clang_version: "20"
```

### Custom File Extensions

```yaml
jobs:
  lint:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-cpp-lint.yml@v1
    with:
      extensions: "c,cpp,h,hpp,cc,cxx"
      clang_version: "18"
```

### Custom Exclude Paths

```yaml
jobs:
  lint:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-cpp-lint.yml@v1
    with:
      ignore: "build|.git|third_party|vendor|test"
      clang_version: "20"
```

### Advanced Configuration

```yaml
jobs:
  lint:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-cpp-lint.yml@v1
    with:
      clang_version: "20"
      tidy_checks: "readability-*,performance-*,modernize-*"  # Specific checks
      extensions: "c,cpp,h,hpp"
      ignore: "build|.git|third_party"
      files_changed_only: true  # Only check changed files in PRs
      thread_comments: true     # Post collapsible thread comments
```

### Performance Optimized for Large Projects

```yaml
jobs:
  lint:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-cpp-lint.yml@v1
    with:
      clang_version: "20"
      files_changed_only: true   # Only lint changed files
      lines_changed_only: true   # Only check changed lines
      ignore: "build|.git|third_party|vendor"  # Exclude more directories
      step_summary: true         # Show summary in workflow
      file_annotations: true     # Show inline annotations
      thread_comments: false     # Disable thread comments for performance
```

## 🔧 Linting Behavior

The workflow provides:

- **Code Style Checking**: clang-format checks for style violations
- **Static Analysis**: clang-tidy performs static analysis checks
- **PR Feedback**: Annotations and comments on pull requests
- **Configurable Scope**: Control which files and paths are checked
- **Performance Options**: Check only changed files/lines for faster runs
- **File Preview**: Prints the list of C/C++ files that will be sent to clang-format and clang-tidy before the action runs
- **File Annotations**: Provides PR annotations for linting issues

### ⚠️ Important Notes

- **Permissions Required**: The workflow needs `pull-requests: write` permission for PR comments
- **File Discovery**: The action automatically discovers C/C++ files in your repository
- **Configuration Files**: Automatically links `clang_format_config` and `clang_tidy_config` into the repository root

## ⚙️ Configuration

### `_config/.clang-format`

Create `_config/.clang-format` to define your formatting style:

```yaml
BasedOnStyle: Google
IndentWidth: 2
ColumnLimit: 100
AccessModifierOffset: -2
```

> Need a different configuration? Point the `clang_format_config` input to any other `.clang-format` file in your repository.

### `_config/.clang-tidy`

Create `_config/.clang-tidy` for static analysis configuration:

```yaml
Checks: '*,readability-*,performance-*,modernize-*'
WarningsAsErrors: ''
HeaderFilterRegex: ''
```

## 🔧 Troubleshooting

### Common Issues

**Style Issues Not Detected**
- Verify `_config/.clang-format` exists and is valid (or adjust `clang_format_config`)
- Check file extensions are included
- Ensure paths match your project structure

**Tidy Checks Not Applied**
- Verify `_config/.clang-tidy` exists (or point `clang_tidy_config` to your config)
- Confirm `tidy_checks` is not overriding the configuration unintentionally

**Clang Version Issues**
- Use supported versions (18, 19, 20)
- Check cpp-linter compatibility

## 📚 Related Workflows

- **[Static Analysis](ru-cpp-analysis.md)** - Security analysis
- **[Documentation](ru-docs-publish.md)** - Documentation generation
- **[Link Check](ru-docs-linkcheck.md)** - Documentation link validation

## 🔗 Related Resources

- [cpp-linter Action](https://github.com/cpp-linter/cpp-linter-action)
- [Clang Format](https://clang.llvm.org/docs/ClangFormat.html)
- [Clang Tidy](https://clang.llvm.org/extra/clang-tidy/)

---

[Next: Static Analysis Workflow →](ru-cpp-analysis.md)

**📚 [All Documentation](index.md)** | **🏠 [Main README](../README.md)**

