---
layout: default
title: "🔄 Reusable Workflows"
description: "Collection of reusable GitHub Actions workflows for CI/CD tasks"
nav_order: 3
has_children: true
permalink: /workflows/
---

# Reusable Workflows

This section contains all the reusable GitHub Actions workflows available in this repository.

## Available Workflows

- **[🔧 C++ Linting Tools](ru-cpp-lint.md)** - Clang-format and clang-tidy for any C++ project
- **[🔍 C++ Static Analysis](ru-cpp-analysis.md)** - Cppcheck security analysis with flexible configuration
- **[📚 Documentation Publisher](ru-docs-publish.md)** - Complete docs pipeline with Doxygen, Jekyll, and GitHub Pages
- **[🔗 Documentation Link Check](ru-docs-linkcheck.md)** - Comprehensive link validation using Lychee
- **[📝 YAML Linting Tools](ru-yaml-lint.md)** - Flexible YAML validation and formatting

## 🚀 Testing & Validation

Each reusable workflow (`ru-*.yml`) has a corresponding comprehensive CI test workflow (`ci-*.yml`) that demonstrates all its features and validates its functionality. See **[CI Workflows & Design Philosophy](ci-workflows.md)** for details on our testing approach.

## Usage

Each workflow is designed to be reusable and can be called from other repositories. See the individual
workflow documentation for detailed usage instructions and parameters.

---

[← Previous: Documentation](index.md) | [Next: CI Workflows & Design →](ci-workflows.md)

**📚 [All Documentation](index.md)** | **🏠 [Main README](../README.md)**
