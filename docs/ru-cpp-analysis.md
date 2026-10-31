---
layout: default
title: "� C++ Static Analysis (Reusable)"
description: "Reusable workflow for C++ security and bug detection using cppcheck"
nav_order: 2
parent: "🔄 Reusable Workflows"
---

# 🔍 C++ Static Analysis (Reusable)

**Workflow:** `ru-cpp-analysis.yml` → 🔍 **[RU] C++ Static Analysis**

A powerful reusable workflow for comprehensive C++ static analysis using cppcheck to detect security vulnerabilities, bugs, and code quality issues. Designed for easy integration with configurable strictness levels.

---

## 📋 Overview

This reusable workflow (`ru-cpp-analysis.yml`) performs comprehensive static analysis on C++ codebases using cppcheck via Docker. It's designed for maximum flexibility with configurable analysis levels and can be called from any repository.

### ✨ **Live CI Example**
👀 See our comprehensive testing workflow: [`ci-cpp-analysis.yml`](../.github/workflows/ci-cpp-analysis.yml) which demonstrates **all features** of this reusable workflow by testing it against real C++ code with various configuration options.

## 📋 Table of Contents

- [Overview](#-overview)
- [Inputs](#-inputs)
- [Outputs](#-outputs)
- [Usage Examples](#-usage-examples)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Related Workflows](#-related-workflows)

## 🎯 Overview

**Purpose**: Security and quality analysis with cppcheck
**Key Features**:
- Docker-based cppcheck execution
- XML and text output formats
- Configurable strictness levels
- Artifact storage

**Use Case**: Security scanning and bug detection in C/C++ code

## ⚙️ Inputs

### 📁 Analysis Scope

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `paths` | string | ❌ | `src inc examples` | Space-separated directories to analyze |

### ⚙️ Analysis Configuration

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `std` | string | ❌ | `c++17` | C++ standard for analysis |
| `strict` | boolean | ❌ | `false` | Fail job if issues found |

## 📤 Outputs

| Output | Description |
|--------|-------------|
| `cppcheck_report.xml` | XML format analysis report |
| `cppcheck_output.txt` | Human-readable output |
| Artifacts | Uploaded reports for review |

## 🚀 Usage Examples

### Basic Usage

```yaml
jobs:
  static:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-cpp-analysis.yml@v1
    with:
      paths: "src include"
      std: "c++17"
      strict: false
```

### Strict Mode

```yaml
jobs:
  static:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-cpp-analysis.yml@v1
    with:
      paths: "src include"
      std: "c++20"
      strict: true  # Fail on any issues
```

### Custom Paths

```yaml
jobs:
  static:
    uses: hardfoc/hf-general-ci-tools/.github/workflows/ru-cpp-analysis.yml@v1
    with:
      paths: "src lib tests"
      std: "c++14"
      strict: false
```

## ⚙️ Configuration

### cppcheck Configuration

The workflow uses these cppcheck options:

```bash
cppcheck \
  --enable=warning,style,performance,portability \
  --suppress=missingIncludeSystem \
  --inline-suppr \
  --std=c++17 \
  --xml \
  --output-file=cppcheck_report.xml
```

### Suppression Files

Create a `.cppcheck-suppressions` file for false positives:

```cpp
// Suppress specific warnings
// unusedFunction:src/legacy.c
// missingInclude:src/third_party.h
```

## 🔧 Troubleshooting

### Common Issues

**Analysis Fails**
- Verify source directories exist
- Check Docker is available
- Ensure paths are space-separated

**Too Many False Positives**
- Use suppression files
- Adjust enabled checks
- Review cppcheck configuration

**Strict Mode Too Restrictive**
- Set `strict: false` for development
- Review issues before enabling strict mode
- Use suppressions for known false positives

## 📚 Related Workflows

- **[C/C++ Lint](ru-cpp-lint.md)** - Code quality checks
- **[Documentation](ru-docs-publish.md)** - Documentation generation
- **[Link Check](ru-docs-linkcheck.md)** - Documentation link validation

## 🔗 Related Resources

- [cppcheck Documentation](https://cppcheck.sourceforge.io/)
- [cppcheck Docker Image](https://github.com/facthunder/cppcheck)
- [Static Analysis Best Practices](https://en.wikipedia.org/wiki/Static_program_analysis)

---

[← Previous: C/C++ Lint Workflow](ru-cpp-lint.md) | [Next: Documentation Workflow →](ru-docs-publish.md)

**📚 [All Documentation](index.md)** | **🏠 [Main README](../README.md)**

